var canvas = document.getElementById("emojiCanvas");
var ctx = canvas.getContext("2d");

var fallingEmojis = []; // Array to hold the falling emojis
var emoji = ''; // The emoji to fall
var releaseInterval = 2000; // Interval in milliseconds after which a new emoji is released

let animationDuration = 10000; 
let startTime = null;

function fetchEmoji() {
  fetch('/get_emoji')
  .then(response => response.text())
  .then(data => {
      emoji = data; // Update the emoji directly from the plain text response
  })
  .catch(error => console.error('Error fetching emoji:', error));
}

function addFallingEmojis() {
  fallingEmojis.push({
    x: Math.random() * canvas.width, // Random x position
    y: 0, // Start at the top of the canvas
    speed: 2 // Random speed between 1 and 3
  });
}

function drawEmojis() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
  if (emoji !== ''){
    fallingEmojis.forEach(function(emojiObj) {
      ctx.font = '30px serif'; // Set the font size and style
      ctx.fillText(emoji, emojiObj.x, emojiObj.y); // Draw the emoji
      emojiObj.y += emojiObj.speed; // Update the y position by the speed
      if (emojiObj.y > canvas.height) {
        emojiObj.y = 0; // Reset to the top of the canvas
        emojiObj.x = Math.random() * canvas.width; // Assign a new random x position
      }
    });
  }
}

// Start releasing emojis at intervals
setInterval(addFallingEmojis, releaseInterval);

function animate() {
  drawEmojis(); 
  requestAnimationFrame(animate); 
}

animate(); 

