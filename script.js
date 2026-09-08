const questionInput = document.getElementById("question");

const askButton = document.getElementById("askButton");

const clearButton = document.getElementById("clearButton");

const loading = document.getElementById("loading");

const resultSection = document.getElementById("resultSection");

const answer = document.getElementById("answer");

const errorSection = document.getElementById("errorSection");

const errorMessage = document.getElementById("errorMessage");


askButton.addEventListener("click", askQuestion);


clearButton.addEventListener("click", clearPage);


async function askQuestion() {

    const question = questionInput.value.trim();


    if (!question) {

        showError("Please enter a question.");

        return;

    }


    hideError();

    resultSection.classList.add("hidden");

    loading.classList.remove("hidden");

    askButton.disabled = true;


    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        if (!data.success) {

            throw new Error(
                data.error || "Unable to generate answer."
            );

        }


        answer.textContent = data.answer;

        resultSection.classList.remove("hidden");


    } catch (error) {

        showError(error.message);

    } finally {

        loading.classList.add("hidden");

        askButton.disabled = false;

    }

}


function clearPage() {

    questionInput.value = "";

    answer.textContent = "";

    resultSection.classList.add("hidden");

    hideError();

}


function showError(message) {

    errorMessage.textContent = message;

    errorSection.classList.remove("hidden");

}


function hideError() {

    errorSection.classList.add("hidden");

}