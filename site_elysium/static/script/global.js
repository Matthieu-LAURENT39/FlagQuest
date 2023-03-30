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