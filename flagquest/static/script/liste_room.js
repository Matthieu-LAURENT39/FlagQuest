/**
 * Créer une nouvelle room
 */
function createRoom() {
    let name = randomString(15)
    let url_name = toSnakeCase(name);

    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var body = JSON.stringify({
        "name": name,
        "url_name": url_name,
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: body,
    };

    fetch(`/api/room/${url_name}`, requestOptions)
        .then(response => response.json())
        .then(data => { window.location.href = `/room/${data.url_name}` })
        .catch(error => {
            console.error(`Error creating room`, error)
            showErrorToast("Erreur lors de la création d'une room.")
        })
}