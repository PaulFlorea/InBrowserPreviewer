from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
# Create your views here.

def_html_input = ('<!DOCTYPE HTML>'+
	'\n<html>'+
	'\n\t<head>'+
	'\n\t</head>'+
	'\n\t<body>'+
	'\n\t\t<h1>Hello World</h1>'+
	'\n\t</body>'+
	'\n</html>')

def_css_input = ('h1{'+
	'\n\tcolor:#007092;'+
	'\n\ttext-align:center;'+
	'\n\tmargin:60px 0px;'+
	'\n}')

@require_http_methods(["POST"])
def save(request):
	session = request.session
	codeDict = dict(request._get_post().iterlists())
	print codeDict['html_code'][0]
	print codeDict['css_code'][0]
	unique_id = request.COOKIES['csrftoken'] + request.COOKIES['sessionid']
	print unique_id

	if 'id' not in session:
		session.set_expiry(0)
		session['id'] = unique_id
	elif session['id'] != unique_id:
		raise Http403("Wrong Session ID")
	
	session['html'] = codeDict['html_code'][0]
	session['css'] = codeDict['css_code'][0]

	return HttpResponse(status=200)

def preview(request):
	return 1

class HomeView(TemplateView):

	template_name = "index.html"

	def get_context_data(self, **kwargs):
		"""
		Populate the context of the template
		with all published entries and all the categories.
		"""
		context = super(HomeView, self).get_context_data(**kwargs)
		context.update(
				{'html_input': def_html_input,
				 'css_input': def_css_input}
		)
		return context



