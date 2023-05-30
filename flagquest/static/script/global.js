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

function randomString(len) {
    var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz, randomPoz + 1);
    }
    return randomString;
}