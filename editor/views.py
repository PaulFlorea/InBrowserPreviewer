import os
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import patch_cache_control
from django.utils.decorators import method_decorator
from functools import wraps

from django.views.generic import TemplateView

from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError



# Default code for a new session
def_html_code = ('<!DOCTYPE HTML>'+
	'\n<html>'+
	'\n\t<head>'+
	'\n\t</head>'+
	'\n\t<body>'+
	'\n\t\t<h1>Hello World</h1>'+
	'\n\t</body>'+
	'\n</html>')

def_css_code = ('h1{'+
	'\n\tcolor:#007092;'+
	'\n\ttext-align:center;'+
	'\n\tmargin:60px 0px;'+
	'\n}')


def never_ever_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-axe=0 Firefox returns cached results
    of GET calls when it is restarted.
    """
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response
    return wrapper

# Error handling and cookie updating helper
def handle_session(request):
	status = ''

	unique_id = ''
	if os.getenv('ENV') == 'PROD':
		unique_id += request.META['HTTP_X_FORWARDED_FOR']
	unique_id += request.META['HTTP_USER_AGENT'] 

	#Session validation	
	if 'id' not in request.session:
		status = "New session"
		request.session.set_expiry(60*30)
		request.session['id'] = unique_id
	elif request.session['id'] != unique_id:
		status = "Invalid session, remaking"
		request.session.flush()
		request.session['id'] = unique_id
	else:
		status = "Existing session"

	return status


# Saves the html and css code in the main page
@require_http_methods(["POST"])
def save(request):
	#Validates the session before saving data -- mostly for debug
	status = handle_session(request)

	codeDict = dict(request._get_post().iterlists())
	request.session['html'] = codeDict['html_code'][0]
	request.session['css'] = codeDict['css_code'][0]

	return HttpResponse(status)


# Puts the two code snippets together and presents them 
# as a single page to the user
def preview(request):
	#Error handling for random improper saving of data
	if not "Exist" in handle_session(request):
		return HttpResponseServerError("Files were improperly saved")
	
	#Concatenates the two files and displays them as one page
	html_code = request.session['html']
	css_code = request.session['css']

	#Finds where the head section of the html ends to insert
	# the stylesheet
	head_end_i = html_code.find('</head>')
	insert_css = '\n<style>\n'+css_code+'\n</style>\n'

	#Creates the page and returns it
	new_page = html_code[:head_end_i]+insert_css+html_code[head_end_i:]
	return HttpResponse(new_page)


# The main code editing page
class HomeView(TemplateView):

	# Template is stored in static folder
	template_name = "index.html"

	def dispatch(self, *args, **kwargs):
		""" Only used for applying decorators """
		return super(HomeView, self).dispatch(*args, **kwargs)

	# Here is where session data gets added if available
	@method_decorator(never_ever_cache)
	def get(self, request, *args, **kwargs):

		#Session handling for previous uses
		if "Exist" in handle_session(request):
			if len(request.session.items()) > 2:
				print "Seaching"
				print request.session.items()
				kwargs['html'] = request.session['html']
				kwargs['css'] = request.session['css']

		context = self.get_context_data(**kwargs)
		# Prevents caching in the main page to always ensure cookie use
		response = self.render_to_response(context)
		return response

	# Updates template with data -- either session or default
	def get_context_data(self, **kwargs):
		"""
		Populate the context of the template
		with all published entries and all the categories.
		"""
		context = super(HomeView, self).get_context_data(**kwargs)
		# Updates session data if available
		if len(kwargs) > 0:
			context.update(
					{'html_input': kwargs['html'],
					 'css_input': kwargs['css']}
			)
		else:	
			context.update(
					{'html_input': def_html_code,
					 'css_input': def_css_code}
			)
		return context



