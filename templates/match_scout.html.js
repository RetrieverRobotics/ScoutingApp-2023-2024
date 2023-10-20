window.addEventListener("load", () => {
    const matchScoutForm = document.getElementById("matchScoutForm");

    matchScoutForm.addEventListener("submit", (ev) => {
        ev.preventDefault();

        if (!matchScoutForm.reportValidity())
            return;

        const data = new FormData(matchScoutForm);
        //TODO unique data validation

        const toStore = {};

        for (const key of data.keys())
            toStore[key] = data.get(key);

        localStorage.setItem("MATCH", JSON.stringify(toStore));
        location.href = "/scout/match/postmatch";
    });
});