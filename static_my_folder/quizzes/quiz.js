document.addEventListener('DOMContentLoaded', function () {
    console.log('JavaScript file is loaded and executed!');

    const currentUrl = window.location.href.split('?')[0];  // Remove query parameters
    const dataUrl = `${currentUrl.endsWith('/') ? currentUrl : currentUrl + '/'}data`;
    const dataUrl_save = `${currentUrl.endsWith('/') ? currentUrl : currentUrl + '/'}save`;
    const quizBox = document.getElementById('quiz_box');
    console.log(dataUrl);  // Ensure the URL is correct

    $.ajax({
        type: 'GET',
        url: dataUrl,  // Using the correct URL
        success: function (response) {
            console.log(response);  // Log the entire response to inspect its structure

            if (response.data && Array.isArray(response.data)) {
                data = response.data;

                data.forEach(el => {
                    for (const [question, answers] of Object.entries(el)) {
                        quizBox.innerHTML += `
                        <hr>
                        <div class="mb-2">  
                            <b> ${question}</b>
                        </div>
                        `;
                        answers.forEach(answer => {
                            quizBox.innerHTML += `
                            <div>
                                <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}">${answer}</label>
                            </div>
                            `;
                        });
                    }
                });
            } else {
                console.log('Unexpected response format:', response);
            }
        },
        error: function (error) {
            console.log('Error:', error);
        }
    });

    // Check if the form exists
    const quizForm = document.getElementById('quiz_form');
    console.log('quizForm:', quizForm);  // Debug: Log quizForm

    if (quizForm) {
        const csrf = document.getElementsByName('csrfmiddlewaretoken');

        const sendData = () => {
            const elements = [...document.getElementsByClassName('ans')];
            const data = {};
            data['csrfmiddlewaretoken'] = csrf[0].value;

            elements.forEach(el => {
                if (el.checked) {
                    data[el.name] = el.value;
                } else {
                    if (!data[el.name]) {
                        data[el.name] = null;
                    }
                }
            });

            $.ajax({
                type: 'POST',
                url: dataUrl_save,
                data: data,
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        };

        quizForm.addEventListener('submit', e => {
            e.preventDefault();
            sendData();
        });
    } else {
        console.error('quizForm element not found in the DOM!');
    }
});
