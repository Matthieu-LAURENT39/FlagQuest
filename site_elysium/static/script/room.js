function toggleEditMode(question_id, edit_mode_enabled) {

    // Edit mode elements
    document.querySelectorAll(`#question_block-${question_id} .question-prompt-edit`)[0].style.display = edit_mode_enabled ? "" : "none"
    document.querySelectorAll(`#question-form-edit-${question_id}`)[0].style.display = edit_mode_enabled ? "" : "none"

    // Display mode elements
    document.querySelectorAll(`#question_block-${question_id} .question-prompt`)[0].style.display = edit_mode_enabled ? "none" : ""
    document.querySelectorAll(`#question_form-${question_id}`)[0].style.display = edit_mode_enabled ? "none" : ""
}

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

    fetch("http://127.0.0.1:5000/api/question/1", requestOptions)
        .then(window.location.reload(true))
    //.then(response => response.text())
    //.then(result => console.log(result))
    //.catch(error => console.log('error', error));
}