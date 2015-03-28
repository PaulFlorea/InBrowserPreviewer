

var html_editor ='';
var css_editor = '';
$(document).ready(function(){
	html_editor = ace.edit("html_editor");
	html_editor.setTheme("ace/theme/clouds");
	html_editor.getSession().setMode("ace/mode/html");

	css_editor = ace.edit("css_editor");
	css_editor.setTheme("ace/theme/clouds");
	css_editor.getSession().setMode("ace/mode/css");
});