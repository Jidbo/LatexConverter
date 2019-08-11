var pdfjsLib = require('pdfjs-dist');
// pdf.js setup
const pdf = document.getElementById('pdf-canvas');
var pdfData = "test";
if (pdf !== null) {
	pdfData = pdf.getAttribute('data');
}
const pdfRaw = atob(pdfData);

pdfjsLib.GlobalWorkerOptions.workerSrc = 'static/dist/pdf.worker.bundle.js';

var pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = 0.8,
    canvas = document.getElementById('pdf-canvas'),
	ctx = null;

if (canvas !== null) {
	ctx = canvas.getContext('2d');
}
/**
 * Get page info from document, resize canvas accordingly, and render page.
 * @param num Page number.
*/
function renderPage(num) {
    pageRendering = true;
    // Using promise to fetch the page
    pdfDoc.getPage(num).then(function(page) {
        var viewport = page.getViewport(scale);
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        // Render PDF page into canvas context
        var renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };
        var renderTask = page.render(renderContext);
        // Wait for rendering to finish
        renderTask.promise.then(function() {
            pageRendering = false;
            if (pageNumPending !== null) {
                // New page rendering is pending
                renderPage(pageNumPending);
                pageNumPending = null;
            }
        });
    });

    // Update page counters
	var pageNum = document.getElementById('page_num');
    pageNum.textContent = num;
}


/**
* If another page rendering in progress, waits until the rendering is
* finised. Otherwise, executes rendering immediately.
*/
function queueRenderPage(num) {
    if (pageRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
}

/**
* Displays previous page.
*/
function onPrevPage() {
    if (pageNum <= 1) {
        return;
    }
    pageNum--;
    queueRenderPage(pageNum);
}
const prevButton = document.getElementById('prev');
if (prevButton !== null) {
	prevButton.addEventListener('click', onPrevPage);
}

/**
* Displays next page.
*/
function onNextPage() {
    if (pageNum >= pdfDoc.numPages) {
        return;
    }
    pageNum++;
    queueRenderPage(pageNum);
}
const nextButton = document.getElementById('next');
if (nextButton !== null) {
	nextButton.addEventListener('click', onNextPage);
}

function createButton(name, onclick, attribute) {
	var listitem = document.createElement('li');
	listitem.classList.add('page-item');
	var button = document.createElement('button');
	if (attribute != null) {
		button.onclick = function() {onclick(attribute)};
	} else {
		button.onclick = onclick;
	}
	button.innerHTML = name;
	button.classList.add('page-link');
	listitem.appendChild(button);
	return listitem;
}

pdfjsLib.getDocument({data: pdfRaw}).promise.then(function(pdfDoc_) {
    pdfDoc = pdfDoc_;
	var page_count = document.getElementById('page_count');
	if (page_count !== null) {
		page_count.textContent = pdfDoc.numPages;
	}
	var buttons = [];
	buttons.push(createButton("&laquo;", onPrevPage, null));
	buttons.push(createButton("&raquo;", onNextPage, null));

	const pagination = document.getElementById('pages');
	if (pagination != null) {
		for (var i = 0; i < buttons.length; i++) {
			pagination.appendChild(buttons[i]);
		}
	}
	
    // Initial/first page rendering
    renderPage(pageNum);
});
