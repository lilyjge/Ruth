// URL for the game page
const gamePageURL = "http://127.0.0.1:5000/";
const menu_url = "../static/menu.png"
myAudio = new Audio("../static/prologue.mp3");
myAudio.loop = true;

// Function to refresh the URL to avoid caching issues
function refreshURL(image_url) {
    return image_url + "?t=" + new Date().getTime();
}

// Function to set the background image dynamically
function setBackgroundImage(image_url) {
    const img = new Image(); // Create an off-screen image element
    img.src = refreshURL(image_url); // Set the image source with the updated URL

    // Once the image is loaded, apply it as the background
    img.onload = () => {
        document.body.style.backgroundImage = `url(${img.src})`;
    };

    img.onerror = () => {
        console.error("Failed to load background image:", img.src);
    };
}

const saveMenu = document.getElementById("save-menu");
const saveSlotsContainer = document.getElementById("save-slots");
const aboutMenu = document.getElementById("about-menu");
const aboutContent = document.getElementById("about-endings");
const settingsMenu = document.getElementById("settings-menu");
const backButtons = document.getElementsByClassName("back-button")

let saveMode = false; // Tracks whether the menu is in Save mode or Load mode
let saveSlots = []; // Array to hold the state of save slots (filled or empty)

// Event listener for Back button
for(let button of backButtons){
    button.addEventListener("click",  () => toggleMenu(button.parentElement.parentElement.parentElement));
}

function toggleMenu(menu){
    menu.style.display = menu.style.display === "none" ? "flex" : "none";
}

// Fetches the current state of save slots from the backend
async function fetchSaveSlots() {
    try {
        const response = await fetch("/api/slots");
        if (!response.ok) throw new Error("Failed to fetch save slots");
        saveSlots = await response.json(); // Expecting an array of booleans
    } catch (err) {
        console.error(err);
    }
}

// Renders the save slots dynamically based on the state
function renderSaveSlots() {
    saveSlotsContainer.innerHTML = ""; // Clear existing slots
    saveSlots.forEach((slotData, index) => {
        const slot = document.createElement("div");
        slot.className = `save-slot ${slotData.filled ? "filled" : ""}`;
        slot.innerHTML = slotData.filled
            ? `
                <img src="data:image/png;base64,${slotData.thumbnail}" alt="Save Slot Thumbnail">
                <div>Save Slot ${index + 1}</div>
                <div class="slot-info">${new Date(slotData.date)}</div>
            `
            : `<div>Empty Slot</div>`;
        slot.addEventListener("click", () => handleSlotClick(index, slotData.filled));
        saveSlotsContainer.appendChild(slot);
    });
}

// Handles slot clicks based on mode (save or load)
async function handleSlotClick(index, isFilled) {
    // Load mode: Load only if the slot is filled
    if (!isFilled) return;
    try {
        const response = await fetch("/api/load", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ saveindex: index, save: true}),
        });
        if (!response.ok) throw new Error("Failed to load game");
        toggleMenu(saveMenu); // Close menu after loading
        const data = await response.json();
        sessionStorage.setItem("saveData", JSON.stringify(data));
        window.location.href = gamePageURL;
        // Redirect to the game page
    } catch (err) {
        console.error(err);
    }
    
}

// Initializes the save menu when Save or Load is clicked
async function initializeSaveMenu() {
    await fetchSaveSlots(); // Fetch the current state of save slots
    renderSaveSlots(); // Render the slots
    toggleMenu(saveMenu); // Show the save menu
}

async function renderAboutMenu(){
    try {
        const response = await fetch("/api/endings");
        if (!response.ok) throw new Error("Failed to fetch endings");
        
        const data = await response.json();
        const messages = data.messages;

        // Clear existing content
        aboutContent.innerHTML = "";

        // Render messages
        messages.forEach((msg) => {
            const messageEntry = document.createElement("div");
            // messageEntry.className = "about-entry";
            messageEntry.textContent = msg;
            aboutContent.appendChild(messageEntry);
        });

        if(messages.length == 7){
            myAudio.setAttribute("src", "../static/ruth.mp3");
            myAudio.play();
        }
    } catch (err) {
        console.error(err);
    }
    toggleMenu(aboutMenu);
}

async function renderSettingsMenu(){
    const response = await fetch('/api/get-settings');
    let settings = await response.json();

    // Fallback to defaults if no settings are returned
    settings = settings || {
        resolution: 3,   // Medium
        steps: 25,       // Default to 25
        deformity: false,
        volume: 50       // Default to 50%
    };

    // Set slider and toggle values
    document.getElementById('resolution-slider').value = settings.resolution;
    updateResolutionLabel(settings.resolution);

    document.getElementById('steps-slider').value = settings.steps;
    updateStepsLabel(settings.steps);

    document.getElementById('deformity-toggle').checked = settings.deformity;

    document.getElementById('volume-slider').value = settings.volume;
    updateVolumeLabel(settings.volume);

    // Show the settings menu
    toggleMenu(settingsMenu);
}

function updateResolutionLabel(value) {
    const labels = ["Lowest", "Low", "Medium", "High", "Highest"];
    document.getElementById('resolution-label').textContent = labels[value - 1];
}

function updateStepsLabel(value) {
    document.getElementById('steps-label').textContent = value;
}

function updateVolumeLabel(value) {
    document.getElementById('volume-label').textContent = value;
}

async function saveSettings() {
    const settings = {
        resolution: parseInt(document.getElementById('resolution-slider').value),
        steps: parseInt(document.getElementById('steps-slider').value),
        deformity: document.getElementById('deformity-toggle').checked,
        volume: parseInt(document.getElementById('volume-slider').value)
    };

    myAudio.volume = settings.volume / 100;

    // Send the settings to the backend
    await fetch('/api/save-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
    });

    toggleMenu(settingsMenu); // Close the settings menu after saving
}
document.getElementById("cancel-button").addEventListener("click", () => toggleMenu(settingsMenu));

// Event listeners for buttons
document.getElementById("new-game").addEventListener("click", () => {
    // Redirect to the game page to start a new game
    window.location.href = gamePageURL;
});

document.getElementById("load-game").addEventListener("click", () => initializeSaveMenu());

document.getElementById("settings").addEventListener("click", () => renderSettingsMenu());

document.getElementById("about").addEventListener("click", () => renderAboutMenu());

document.body.addEventListener("click", () => {
    if (myAudio.paused|| !myAudio.currentTime) 
        myAudio.play();    
    if (!document.fullscreenElement &&
        !document.mozFullScreenElement &&
        !document.webkitFullscreenElement &&
        !document.msFullscreenElement) {
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen();
        } else if (document.documentElement.msRequestFullscreen) {
            document.documentElement.msRequestFullscreen();
        }
    }
});

async function init_settings(){
    const response = await fetch('/api/get-settings');
    let settings = await response.json();
    myAudio.volume = settings.volume / 100;
    // await fetch('/api/save-settings', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(settings)
    // });
}

// Update background on load
window.onload = () => {
    init_settings();
    setBackgroundImage(menu_url);
}
