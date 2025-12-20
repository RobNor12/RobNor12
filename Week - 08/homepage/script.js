// Wait for the entire page (DOM) to load before running the script
document.addEventListener('DOMContentLoaded', function() {

    // --- Helper function to disable all buttons in a question's container ---
    function disableButtons(questionId) {
        document.querySelectorAll(`#${questionId} button`).forEach(btn => {
            btn.disabled = true;
        });
    }

    // --- Free Response Question Logic (Q1, Q3, Q4) ---
    // This function sets up the event listeners for any question with an input field
    function setupFreeResponse(questionNumber, correctAnswer, feedbackElement, inputElement, checkButtonElement) {
        if (checkButtonElement) {
            checkButtonElement.addEventListener('click', function() {
                // Use .toLowerCase() for case-insensitive checking (e.g., 'dog' == 'DOG')
                const answer = inputElement.value.trim().toLowerCase();

                // Check against the expected answer
                if (answer === correctAnswer.toLowerCase() || answer.includes(correctAnswer.toLowerCase())) {
                    inputElement.classList.remove('is-invalid');
                    inputElement.classList.add('is-valid');
                    feedbackElement.innerHTML = `<span class="text-success fw-bold">Correct!</span> The answer is: ${correctAnswer}.`;
                    inputElement.disabled = true;
                    checkButtonElement.disabled = true;
                } else {
                    inputElement.classList.remove('is-valid');
                    inputElement.classList.add('is-invalid');
                    feedbackElement.innerHTML = '<span class="text-danger fw-bold">Incorrect.</span> Check the other pages for a hint!';
                }
            });
        }
    }

    // --- Q1: Dog Breed (Assumed Answer: Golden Retriever) ---
    setupFreeResponse(
        1,
        'Blue Nose Pit',
        document.querySelector('#feedback1'),
        document.querySelector('#input-q1'),
        document.querySelector('#check-q1')
    );

    // --- Q3: State (Assumed Answer: New York) ---
    setupFreeResponse(
        3,
        'louisiana',
        document.querySelector('#feedback3'),
        document.querySelector('#input-q3'),
        document.querySelector('#check-q3')
    );

    // --- Q4: College (Assumed Answer: Pearl River Community College) ---
    setupFreeResponse(
        4,
        'Pearl River Community College',
        document.querySelector('#feedback4'),
        document.querySelector('#input-q4'),
        document.querySelector('#check-q4')
    );


    // --- Q2: Left-handed (Multiple Choice - True) ---
    const q2Correct = document.querySelector('#q2-true');
    const q2Incorrect = document.querySelector('#q2-false');
    const feedback2 = document.querySelector('#feedback2');
    const q2Id = 'question-2';

    if (q2Correct) {
        q2Correct.addEventListener('click', function() {
            q2Correct.classList.remove('btn-outline-primary');
            q2Correct.classList.add('btn-success');
            feedback2.innerHTML = '<span class="text-success fw-bold">Correct!</span> I am left-handed.';
            disableButtons(q2Id);
        });
    }
    if (q2Incorrect) {
        q2Incorrect.addEventListener('click', function() {
            q2Incorrect.classList.remove('btn-outline-primary');
            q2Incorrect.classList.add('btn-danger');
            feedback2.innerHTML = '<span class="text-danger fw-bold">Incorrect.</span> The answer is True.';
            disableButtons(q2Id);
        });
    }

    // --- Q5: Which is NOT a hobby (Multiple Choice - Answer: Reading) ---
    const q5Correct = document.querySelector('#q5-reading');
    const q5Incorrects = document.querySelectorAll('#q5-videogames, #q5-outdoors, #q5-programming');
    const feedback5 = document.querySelector('#feedback5');
    const q5Id = 'question-5';

    if (q5Correct) {
        q5Correct.addEventListener('click', function() {
            q5Correct.classList.remove('btn-outline-primary');
            q5Correct.classList.add('btn-success');
            feedback5.innerHTML = '<span class="text-success fw-bold">Correct!</span> Reading is NOT one of my hobbies.';
            disableButtons(q5Id);
        });
    }

    q5Incorrects.forEach(btn => {
        btn.addEventListener('click', function() {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-danger');
            feedback5.innerHTML = '<span class="text-danger fw-bold">Incorrect.</span> That IS one of my hobbies/interests.';
            document.querySelector('#q5-reading').classList.add('btn-success'); // Highlight the correct answer
            disableButtons(q5Id);
        });
    });

});
