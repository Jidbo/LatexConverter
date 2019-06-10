import './style.css';
const download = require("downloadjs");
var bootstrap = require('bootstrap3');
require('bootstrap3/dist/css/bootstrap.css');


$('#copytoclip').hide();

$('#download').click(function() {
	download($('#result').val(), "result.tex", "text/plain");
});

$('#download-pdf').click(function() {
    download($('#download-pdf').attr("data"), "result.pdf", "application/pdf");
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
