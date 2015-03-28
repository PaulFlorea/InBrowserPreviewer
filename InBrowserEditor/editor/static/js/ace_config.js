var html_editor ='';
var css_editor = '';
$(document).ready(function(){

	$('#save_code').click(save_code);
	$('#preview').click(function(){location.href=base_url+'preview'});

	html_editor = ace.edit("html_editor");
	html_editor.setTheme("ace/theme/clouds");
	html_editor.getSession().setMode("ace/mode/html");
	html_editor.on('change',function(){$('#save_code').html('Save')});

	css_editor = ace.edit("css_editor");
	css_editor.setTheme("ace/theme/clouds");
	css_editor.getSession().setMode("ace/mode/css");
	css_editor.on('change',function(){$('#save_code').html('Save')});
});

function save_code(){
	$object = $(this);
	$object.prop('disabled',true).html('Saving');

	var formData = new FormData();
	formData.append('html_code',html_editor.getValue());
	formData.append('css_code',css_editor.getValue());

	$.ajax({
		url: base_url+'upload_code/',
		type: 'POST',
		data: formData,
		processData: false,
		contentType: false,
		success:function(data){code_uploaded(data,$object)},
		error:std__error
	});
}