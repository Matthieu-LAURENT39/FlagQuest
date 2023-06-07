/**
 * retire l'affichage de l'input d'affichage de la question
 * affiche l'input de modif de la question
 * @param { int } question_id 
 * @param { boolean } edit_mode_enabled 
 */
function toggleQuestionEditMode(question_id, edit_mode_enabled) {
    // Switch the button to trigger the other mode
    document.querySelectorAll(`#question_block-${question_id} button`)[0].onclick = function () { toggleQuestionEditMode(question_id, !edit_mode_enabled) }

    // Switch the styling of the question
    let question_div = document.getElementById(`question_block-${question_id}`);
    question_div.classList.remove(edit_mode_enabled ? "bg-light" : "bg-dark-subtle")
    question_div.classList.add(edit_mode_enabled ? "bg-dark-subtle" : "bg-light");

    // le [0] - accède au 1er element trouvé du querySelectorAll

    // Edit mode elements
    // comme c'est true - on met display: ""; c'est à dire block par défaut
    document.querySelectorAll(`#question_block-${question_id} .question-prompt-edit`)[0].style.display = edit_mode_enabled ? "" : "none"
    document.querySelectorAll(`#question-form-edit-${question_id}`)[0].style.display = edit_mode_enabled ? "" : "none"

    // Display mode elements
    // comme c'est true - on met display: "none"; (donc plus affiché)
    document.querySelectorAll(`#question_block-${question_id} .question-prompt`)[0].style.display = edit_mode_enabled ? "none" : ""
    document.querySelectorAll(`#question_form-${question_id}`)[0].style.display = edit_mode_enabled ? "none" : ""
    document.querySelectorAll(`#question_block-${question_id} .question-widget-points`)[0].style.display = edit_mode_enabled ? "none" : ""
}

/**
 * enregistre la modification apportée à la question
 * @param { int } question_id 
 */
function saveQuestion(question_id) {
    let new_prompt = document.querySelectorAll(`#question_block-${question_id} .question-prompt-edit textarea`)[0].value
    let new_answer = document.querySelectorAll(`#question-form-edit-${question_id} .question-answer-edit`)[0].value
    let new_points = document.querySelectorAll(`#question-form-edit-${question_id} .question-points-edit`)[0].value

    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var body = JSON.stringify({
        "prompt": new_prompt,
        "answer": new_answer,
        "points": new_points
    });

    var requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: body,
    };

    fetch(`/api/question/${question_id}`, requestOptions)
        .then(response => { window.location.reload(true) })
        //.then(response => response.text())
        //.then(result => console.log(result))
        .catch(error => {
            console.error(`Error saving question ${question_id}: `, error)
            showErrorToast("Erreur lors de l'enregistrement des modifications.")
        })
}

/**
 * supprime la question
 * @param { int } question_id 
 */
function deleteQuestion(question_id) {
    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        body: "",
    };

    fetch(`/api/question/${question_id}`, requestOptions)
        .then(response => window.location.reload(true))
        .catch(error => {
            console.error(`Error deleting question ${question_id}: `, error)
            showErrorToast("Erreur lors de la suppression de la question.")
        })
}

/**
 * retire l'affichage de la room
 * affiche l'input de modif de la room
 * @param { boolean } edit_mode_enabled 
 */
function toggleRoomEditMode(edit_mode_enabled) {
    // Switch the button to trigger the other mode
    document.getElementById(`editRoomButton`).onclick = function () { toggleRoomEditMode(!edit_mode_enabled) }

    // Switch the styling of the room info
    let room_div = document.getElementById("roomInfoWidget");
    room_div.classList.remove(edit_mode_enabled ? "bg-light" : "bg-dark-subtle")
    room_div.classList.add(edit_mode_enabled ? "bg-dark-subtle" : "bg-light");

    // Edit mode elements
    document.getElementById("roomInfoEditForm").style.display = edit_mode_enabled ? "" : "none"

    // Display mode elements
    document.getElementById("roomInfoDisplay").style.display = edit_mode_enabled ? "none" : ""
}

function deleteRoom(room_url_name) {
    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        body: "",
    };

    fetch(`/api/room/${room_url_name}`, requestOptions)
        .then(response => window.location.href = "/")
        .catch(error => {
            console.error(`Error deleting room ${room_url_name}: `, error)
            showErrorToast("Erreur lors de la suppression de la room.")
        })
}

/**
 * enregistre la modification apportée à la room
 * @param { str } room_url_name 
 */
function saveRoom(room_url_name) {
    let new_name = document.getElementById("room-name-edit").value
    let new_url_name = document.getElementById("room-url_name-edit").value
    let new_instructions = document.getElementById("room-instructions-edit").value
    let new_description = document.getElementById("room-description-edit").value
    let new_victim_vm_ids = document.getElementById("room-victim_vm_ids-edit").value.trim()

    var regex = /^(\d+(;\s*\d+)*)?$/; // Regular expression to match comma-separated integers
    if (!regex.test(new_victim_vm_ids)) {
        showErrorToast("La liste des id de VM victimes n'est pas une liste d'entiers séparé par des points-virgules.")
        return
    }

    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var body = JSON.stringify({
        "instructions": new_instructions,
        "description": new_description,
        "url_name": new_url_name,
        "_victim_vm_ids": new_victim_vm_ids,
        "name": new_name
    });

    var requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: body,
    };

    fetch(`/api/room/${room_url_name}`, requestOptions)
        .then((response) => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Status not ok');
        })
        .then(data => { window.location.href = `/room/${data.url_name}` })
        //.then(response => response.text())
        //.then(result => console.log(result))
        .catch(error => {
            console.error(`Error saving room`, error)
            showErrorToast("Erreur lors de l'enregistrement des modifications de la room.")
        })
}