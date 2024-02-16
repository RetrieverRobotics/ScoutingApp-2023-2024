NEXT_DESTINATION = "/scout/match/during";

window.addEventListener("load", () => {
    const teamForm = document.getElementById("teamForm");
    const preMatchForm = document.getElementById("preMatchForm");
    const datePreMatch = document.getElementById("datePreMatch");

    teamForm.addEventListener("submit", async (ev) => {
        ev.preventDefault();

        if (!teamForm.reportValidity())
            return;
    
        const data = new FormData(teamForm);

        const urlStr = `${location.origin}/scout/pit/get/robots`;
        const url = new URL(urlStr);
        url.searchParams.set("team", data.get("team"));

        const resp = await fetch(url);
        const names = resp.ok ? await resp.json() : [];
        setRobots(data.get("team"), names);
    });

    const now = new Date();
    datePreMatch.value = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;

    preMatchForm.addEventListener("submit", (ev) => {
        ev.preventDefault();

        if (!preMatchForm.reportValidity())
            return;

        const data = new FormData(preMatchForm);
        if (!data.has("robot")) {
            alert("Must enter a team to select a robot from.");
            return;
        }
        const toStore = {};

        for (const key of data.keys())
            toStore[key] = data.get(key);

        localStorage.setItem("PRE_MATCH", JSON.stringify(toStore));
        location.href = NEXT_DESTINATION;
    });

    setValues(preMatchForm, "PRE_MATCH");
});


/**
 * @param {string} team
 * @param {string[]} names 
 */
function setRobots(team, names) {
    const teamPreMatch = document.getElementById("teamPreMatch");
    const robotRadios = document.getElementById("robotRadios");

    teamPreMatch.value = team;

    while (robotRadios.children.length)
        robotRadios.removeChild(robotRadios.children[0]);

    for (const name of names) {
        const wrapper = document.createElement("p");
        const label = document.createElement("label");
        const image = document.createElement("img");
        const radio = document.createElement("input");

        label.innerText = `${team}-${name}`;

        const urlStr = `${location.origin}/scout/pit/get/image`;
        const url = new URL(urlStr);
        url.searchParams.set("team", team);
        url.searchParams.set("designation", name);

        image.src = url.toString();
        image.alt = `${team}-${name}`;
        image.style.maxWidth = "100px";
        image.style.width = image.style.height = "auto";

        radio.type = "radio";
        radio.name = "robot";
        radio.value = name;
        radio.required = true;

        wrapper.appendChild(radio);
        wrapper.appendChild(label);
        wrapper.appendChild(image);
        robotRadios.appendChild(wrapper);
    }

    //final option: robot not listed
    const fwrapper = document.createElement("p");
    const flabel = document.createElement("label")
    const fradio = document.createElement("input");

    flabel.innerText = "Robot not listed / Unsure (explain in comments)";

    fradio.type = "radio";
    fradio.name = "robot";
    fradio.value = "?"
    fradio.required = true;

    fwrapper.appendChild(fradio);
    fwrapper.appendChild(flabel);
    robotRadios.appendChild(fwrapper);
}