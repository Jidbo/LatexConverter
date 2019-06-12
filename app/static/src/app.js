import './style.css';
import './pdf.js';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import download from 'downloadjs';
import './pdf.js';

$('.close').click(function() {
	$('.alert').hide();
});

$('#copytoclip').hide();

$('#download').click(function() {
	download($('#result').val(), "result.tex", "text/plain");
});

$('#download-pdf').click(function() {
	const pdfData = document.getElementById('pdf-canvas').getAttribute('data');
	download('data:application/pdf;base64,' + pdfData, "result.pdf", "application/pdf");
});

$('#copytoclipbtn').click(function() {
	$('#result').select();
	document.execCommand("copy");
	$('#copytoclip').show();
});
