from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):

	html_input = ('<!DOCTYPE HTML>'+
		'\n<html>'+
		'\n\t<head>'+
		'\n\t</head>'+
		'\n\t<body>'+
		'\n\t\t<h1>Hello World</h1>'+
		'\n\t</body>'+
		'\n</html>')

	css_input = ('h1{'+
		'\n\tcolor:#007092;'+
		'\n\ttext-align:center;'+
		'\n\tmargin:60px 0px;'+
		'\n}')

	template_name = "index.html"

	def get_context_data(self, **kwargs):
		  """
		  Populate the context of the template
		  with all published entries and all the categories.
		  """
		  context = super(HomeView, self).get_context_data(**kwargs)
		  context.update(
				{'html_input': HomeView.html_input,
				 'css_input': HomeView.css_input}
		  )
		  return context

