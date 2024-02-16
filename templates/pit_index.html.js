window.addEventListener("load", () => {
    const teamForm = document.getElementById("teamForm");
    const addRobot = document.getElementById("addRobot");

    teamForm.addEventListener("submit", async (ev) => {
        ev.preventDefault();

        if (!teamForm.reportValidity())
            return;

        const data = new FormData(teamForm);
        
        const urlStr = `${location.protocol}//${location.origin}/scout/pit/get/robots`;
        const url = new URL(urlStr);
        url.searchParams.set("team", data.get("team"));

        const resp = await fetch(url);
        const names = resp.ok ? await resp.json() : [];
        setRobots(data.get("team"), names);
    });

    addRobot.addEventListener("submit", async (ev) => {
        ev.preventDefault();

        const data = new FormData(addRobot);
        const resp = await fetch("/scout/pit/submit", {
            method: "POST",
            body: data
        });
        if (resp.ok)
            location.reload();
        else
            alert(`Submission Failed (${resp.status})`);
    });
});

/**
 * @param {string} team
 * @param {string[]} names 
 */
function setRobots(team, names) {
    const addRobotTeam = document.getElementById("addRobotTeam");
    const robots = document.getElementById("robots");

    addRobotTeam.value = team;

    while (robots.children.length)
        robots.removeChild(robots.children[0]);

    for (const name of names) {
        const wrapper = document.createElement("p");
        const label = document.createElement("p");
        const image = document.createElement("img");

        label.innerText = `${team}-${name}`;

        const urlStr = `${location.protocol}//${location.origin}/scout/pit/get/image`;
        const url = new URL(urlStr);
        url.searchParams.set("team", team);
        url.searchParams.set("designation", name);

        image.style.maxWidth = "100px";
        image.style.width = image.style.height = "auto";
        image.src = url.toString();
        image.alt = `${team}-${name}`;

        wrapper.appendChild(label);
        wrapper.appendChild(image);
        robots.appendChild(wrapper);
    }
}