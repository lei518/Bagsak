console.log('JavaScript file is loaded and executed!');

// let dataUrl = `${url.endsWith('/') ? url : url + '/'}data`;

// const url = window.location.href;
// console.log(url);

const currentUrl = window.location.href.split('?')[0];  // Remove query parameters
const dataUrl = `${currentUrl.endsWith('/') ? currentUrl : currentUrl + '/'}data`;
const quizBox= document.getElementById('quiz_box')
console.log(dataUrl);  // Ensure the URL is correct



$.ajax({
    type: 'GET',
    url: dataUrl,  // Using the correct URL
    success: function (response) {
        console.log(response);  // Log the entire response to inspect its structure

        // Check if response.data is defined
        if (response.data && Array.isArray(response.data)) {
            data = response.data;

            data.forEach(el => {
                // Loop through each question and its answers
                for (const [question, answers] of Object.entries(el)) {
                   quizBox.innerHTML+= `
                   <hr>
                   <div class="mb-2">  
                    <b> ${question}</b>
                   </div>
                   `
                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        `
                    });


                }
            });
        } else {
            console.log('Unexpected response format:', response);
        }
    },
    error: function (error) {
        console.log('Error:', error);  // Log any errors
    }
});
