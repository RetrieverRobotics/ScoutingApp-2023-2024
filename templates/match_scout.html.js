let endAuto = null;
const inputs = {};

function getNow() {
    return (new Date()).toISOString();
}

window.addEventListener("load", () => {
    const matchScoutForm = document.getElementById("matchScoutForm");
    /** @type {HTMLButtonElement} */
    const matchEndButton = document.getElementById("matchEndButton");

    matchScoutForm.addEventListener("submit", (ev) => {
        ev.preventDefault();

        const data = new FormData();

        inputs["end-auto"] = endAuto;
        inputs["end"] = getNow();

        localStorage.setItem("MATCH", JSON.stringify(inputs));
        location.href = "/scout/match/postmatch";
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