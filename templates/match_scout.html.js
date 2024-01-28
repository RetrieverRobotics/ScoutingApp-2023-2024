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
    //TODO change element colors so that change in mode is more clear
    const matchStealButton = document.getElementById("matchStealButton");
    const matchStolenButton = document.getElementById("matchStolenButton");

    matchStealButton.style.display = "block";
    matchStolenButton.style.display = "block";
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