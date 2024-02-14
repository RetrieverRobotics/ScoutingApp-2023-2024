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
        if (elm.type == "checkbox") {
            /** @type {string} */
            const key = elm.name;
            inputs[key] = false;

            elm.addEventListener("input", () => {
                inputs[key] = elm.checked;
                console.log("input");
            });

            elm.parentElement.addEventListener("click", (ev) => {
                if (ev.target == elm || ev.button != 0) return;
                elm.checked = !elm.checked;
                console.log("click")
            })
        }
        else {
            const key = elm.innerText.toLowerCase();
            inputs[key] = [];
            elm.addEventListener("click", () => {
                inputs[key].push(getNow());
            });
        }
    });
}