const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capture');

// to enable webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => console.error('Cannot access camera: ', err));

captureButton.addEventListener('click', function() {
    context.drawImage(video, 0, 0, 640, 480);
    const imageDataURL = canvas.toDataURL('image/jpeg');
    sendImage(imageDataURL);
});

function sendImage(imageDataURL) {
    // send image data to flask app
    fetch('http://localhost:5002/process_img', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageDataURL })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Server responded with a status: ' + response.status);
        }
    })    
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}