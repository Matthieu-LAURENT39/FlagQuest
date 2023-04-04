// notification pop up erreur
function showErrorToast(text) {
    Toastify({
        text: text,
        duration: 7000,

        gravity: "top",
        position: "right",

        stopOnFocus: true,
        close: true,

        style: {
            background: "red",
        }
    }).showToast();
}

var matrixDrawIntervalId = null;
function setupMatrixBackground() {
    // ===== Matrix (https://codepen.io/yaclive/pen/EayLYO) =====
    // Initialising the canvas
    var canvas = document.getElementById("matrix-background")
    if (canvas != null) {
        if (matrixDrawIntervalId != null) {
            clearInterval(matrixDrawIntervalId);
        }

        var ctx = canvas.getContext('2d');

        // Setting the width and height of the canvas
        canvas.width = window.innerWidth;
        canvas.height = document.body.scrollHeight;

        // Setting up the letters
        var letters = 'ABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZABCDEFGHIJKLMNOPQRSTUVXYZ';
        letters = letters.split('');

        // Setting up the columns
        var fontSize = 10,
            columns = canvas.width / fontSize;

        // Setting up the drops
        var drops = [];
        for (var i = 0; i < columns; i++) {
            drops[i] = 1;
        }

        // Setting up the draw function
        function draw() {
            ctx.fillStyle = 'rgba(0, 0, 0, .1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            for (var i = 0; i < drops.length; i++) {
                var text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillStyle = '#0f0';
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                drops[i]++;
                if (drops[i] * fontSize > canvas.height && Math.random() > .95) {
                    drops[i] = 0;
                }
            }
        }

        //* We call the draw functions manually to avoid the starting effect
        for (var i = 0; i < drops.length; i++) {
            for (let j = 0; j < 100; j++) {
                if (drops[i] * fontSize > canvas.height && Math.random() > .95) {
                    drops[i] = 0;
                }
            }
        }


        // Loop the animation, and store the ID so we can stop it later
        matrixDrawIntervalId = setInterval(draw, 33);
    }
}

$(document).ready(function () {
    setupMatrixBackground();
});

$(window).resize(function () {
    setupMatrixBackground();
});