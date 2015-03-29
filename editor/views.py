from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.generic import TemplateView


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


# Error handling and cookie updating helper
def handle_session(request):
	status = ""

	unique_id = request.COOKIES['csrftoken'] + request.get_host()

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

	# Here is where session data gets added if available
	def get(self, request, *args, **kwargs):

		#Session handling for previous uses
		if "Exist" in handle_session(request):
			if len(request.session.items()) > 2:
				print "Seaching"
				print request.session.items()
				kwargs['html'] = request.session['html']
				kwargs['css'] = request.session['css']

		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

	# Updates template with data -- either session or default
	def get_context_data(self, **kwargs):
		"""
		Populate the context of the template
		with all published entries and all the categories.
		"""
		context = super(HomeView, self).get_context_data(**kwargs)
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



