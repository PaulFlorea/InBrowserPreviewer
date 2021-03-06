var html_editor ='';
var css_editor = '';


$(document).ready(function(){

	$('#save_code').click(save_code);
	$('#preview').click(preview);

	html_editor = ace.edit("html_editor");
	html_editor.setTheme("ace/theme/cobalt");
	html_editor.getSession().setMode("ace/mode/html");
	html_editor.on('change',function(){$('#save_code').html('Save')});

	css_editor = ace.edit("css_editor");
	css_editor.setTheme("ace/theme/cobalt");
	css_editor.getSession().setMode("ace/mode/css");
	css_editor.on('change',function(){$('#save_code').html('Save')});
});

function preview(){
	var formData = new FormData();
	formData.append('html_code',html_editor.getValue());
	formData.append('css_code',css_editor.getValue());

	$.ajax({
		url: 'save/',
		type: 'POST',
		data: formData,
		processData: false,
		contentType: false,
		success:function(data){code_uploaded(data,$object)}
	});	
	
	location.href='/preview';
}

function save_code(){
	$object = $(this);
	$object.prop('disabled',true).html('Saving');

	var formData = new FormData();
	formData.append('html_code',html_editor.getValue());
	formData.append('css_code',css_editor.getValue());

	$.ajax({
		url: 'save/',
		type: 'POST',
		data: formData,
		processData: false,
		contentType: false,
		success:function(data){code_uploaded(data,$object)}
	});	
}

var code_uploaded = function(data,object){
	console.log(data);
	object.html('Saved');
}