
// wait for the content of the window element
// to load, then performs the operations.
// This is considered best practice.
window.addEventListener('load', ()=>{
	//resize(); // Resizes the canvas once the window loads
	document.addEventListener('mousedown', startPainting);
	document.addEventListener('mouseup', stopPainting);
	document.addEventListener('mousemove', sketch);
	window.addEventListener('resize', resize);
});

const canvas = document.querySelector('#canvas');

var xhr = new XMLHttpRequest();

// Context for the canvas for 2 dimensional operations
const ctx = canvas.getContext('2d');

// bind event handler to clear button
document.getElementById('clear').addEventListener('click', function()
    {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    }, false);

// bind event handler to save button

xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        document.write(xhr.responseText);
    }
}

document.getElementById('save').addEventListener('click', function()
    {
    let dataURL = canvas.toDataURL();
    //xhr.open('GET', '/numbers/?data='+dataURL, true);
    xhr.open('POST', '/numbers/draw', true);
    xhr.send(dataURL);
    //xhr.send();
    //let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    //let dataURL = ctx.toDataURL();
    console.log(post);
    }, false);





// Resizes the canvas to the available size of the window.
function resize(){
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;
}

// Stores the initial position of the cursor
let coord = {x:0 , y:0};

// This is the flag that we are going to use to
// trigger drawing
let paint = false;

// Updates the coordianates of the cursor when
// an event e is triggered to the coordinates where
// the said event is triggered.
function getPosition(event){
rect = canvas.getBoundingClientRect()
coord.x = event.clientX - rect.x;
coord.y = event.clientY - rect.y;
//coord.x = event.clientX - canvas.offsetLeft;
//coord.y = event.clientY - canvas.offsetTop;
}

// The following functions toggle the flag to start
// and stop drawing
function startPainting(event){
paint = true;
getPosition(event);
}
function stopPainting(){
paint = false;
}

function sketch(event){
if (!paint) return;
ctx.beginPath();

ctx.lineWidth = 50;

// Sets the end of the lines drawn
// to a round shape.
ctx.lineCap = 'round';

ctx.strokeStyle = 'black';

// The cursor to start drawing
// moves to this coordinate
ctx.moveTo(coord.x, coord.y);

// The position of the cursor
// gets updated as we move the
// mouse around.
getPosition(event);

// A line is traced from start
// coordinate to this coordinate
ctx.lineTo(coord.x , coord.y);

// Draws the line.
ctx.stroke();


}