const HEIGHT_OUTPUT = ["Didn't climb","A","B","C","D","E","F","G","H","I","J"];


window.addEventListener("load", () => {
    const postMatchScoutForm = document.getElementById("postMatchScoutForm");
    const postMatchHeightInput = document.getElementById("postMatchHeightInput");
    const postMatchHeightOutput = document.getElementById("postMatchHeightOutput");

    postMatchScoutForm.addEventListener("submit", (ev) => {
        ev.preventDefault();

        if (!postMatchScoutForm.reportValidity())
            return;

        const data = new FormData(postMatchScoutForm);

        const toStore = {};

        for (const key of data.keys())
            toStore[key] = data.get(key);

        localStorage.setItem("POST_MATCH", JSON.stringify(toStore));
        location.href = "/scout/match/confirm";
    });

    postMatchHeightInput.addEventListener("input", () => {
        postMatchHeightOutput.innerText = HEIGHT_OUTPUT[Math.ceil(postMatchHeightInput.value/10)];
    });
})