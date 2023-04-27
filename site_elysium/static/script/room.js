/**
 * retire l'affichage de l'input d'affichage de la question
 * affiche l'input de modif de la question
 * @param { int } question_id 
 * @param { boolean } edit_mode_enabled 
 */
function toggleEditMode(question_id, edit_mode_enabled) {
    // Switch the button to trigger the other mode
    document.querySelectorAll(`#question_block-${question_id} button`)[0].onclick = function () { toggleEditMode(question_id, !edit_mode_enabled) }

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

    // Save the values to the server
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var body = JSON.stringify({
        "prompt": new_prompt,
        "answer": new_answer
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: body,
    };

    fetch(`/api/question/${question_id}`, requestOptions)
        .then(window.location.reload(true))
    //.then(response => response.text())
    //.then(result => console.log(result))
    //.catch(error => console.log('error', error));
}