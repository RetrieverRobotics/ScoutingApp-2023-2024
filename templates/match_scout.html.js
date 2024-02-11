let endAuto = null;
const inputs = {};

NEXT_DESTINATION = "/scout/match/postmatch";

function getNow() {
    return (new Date()).toISOString();
}

window.addEventListener("load", () => {
    const start = getNow();
    const matchScoutForm = document.getElementById("matchScoutForm");
    /** @type {HTMLButtonElement} */
    const matchEndButton = document.getElementById("matchEndButton");

    matchScoutForm.addEventListener("submit", (ev) => {
        ev.preventDefault();

        inputs["start"] = start;
        inputs["end-auto"] = endAuto;
        inputs["end"] = getNow();

        localStorage.setItem("MATCH", JSON.stringify(inputs));
        location.href = NEXT_DESTINATION;
    });

    matchEndButton.addEventListener("click", (ev) => {
        if (ev.button != 0) return;
        else if (endAuto == null) {
            endAuto = getNow();
            matchEndButton.innerText = "End Match";
            changeMatchStyle();
            setTimeout(() => matchEndButton.type = "submit", 100);

        }
    });

    initInputs();
});

function changeMatchStyle() {
    document.querySelectorAll(".toggle-visibility").forEach((elm) => {
        elm.classList.toggle("input-hide");
    });
}

function initInputs() {
    document.querySelectorAll(".scout-input").forEach((elm) => {
        const key = elm.innerText.toLowerCase();
        inputs[key] = [];
        elm.addEventListener("click", () => {
            inputs[key].push(getNow());
        });
    });
}