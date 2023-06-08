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

function toSnakeCase(str) {
    return str
        .toLowerCase()
        // Normalise accents, eg: à -> a
        .normalize("NFD")
        .replace(/\s+/g, '_')
        .replace(/[^a-z0-9_]/g, '')
        // Remove consecutive underscores
        .replace(/_+/g, '_')
        .replace(/^_|_$/g, '');
}

// Show the introduction when ? is pressed
document.addEventListener("keydown", function (event) {
    if (event.key === "F1") {
        event.preventDefault();

        // Start the introduction if one exists
        if (typeof driver !== 'undefined') {
            driver.start();
        } else {
            showErrorToast("Pas d'aide disponible pour cette page.");
        }
    }
});