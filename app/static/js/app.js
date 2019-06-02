$('#copytoclip').hide();

$('#download').click(function() {
	download($('#result').val(), "result.tex", "text/plain");
});

$(document).ready(function () {

	$('.close').click(function() {
		$('.alert').hide();
	});

	$('#copytoclipbtn').click(function() {
		$('#result').select();
		document.execCommand("copy");
		$('#copytoclip').show();
	});
});
