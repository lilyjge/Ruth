const storyText = document.getElementById('story-text');
const choicesContainer = document.getElementById('choices-container');
const userInputSection = document.getElementById('user-input-section');
const userInput = document.getElementById('user-input');
const submitButton = document.getElementById('submit-button');
const storyInputBox = document.getElementById('story-input-box');
const game_url = '../static/gameplay.png';
const scene_url = '../static/scene.png';
const menuPageURL = "http://127.0.0.1:5000/home"
myAudio = new Audio("../static/interlude.mp3")
myAudio.loop = true;
inDialogue = false; // determines whether to render choices box
inEvent = false; // for event transitions
enableInput = false; // determines story text or user input mode
end = false

function newEvent(){
    inDialogue = false;
    inEvent = false;
    enableInput = false;
    toggleInputMode();
    // Initialize with default choices
    fetch('/api/initialize', {method: 'POST'})
        .then(response => response.json())
        .then(data => updateStory(data))
        .catch(err => console.error('Failed to initialize story:', err));
}

function refreshURL(image_url) {
    return image_url + "?t=" + new Date().getTime();
}

function setBackgroundImage(image_url) {
    const img = new Image(); // Create an off-screen image element
    img.src = refreshURL(image_url); // Set the image source with the updated URL

    // Once the image is loaded, apply it as the background
    img.onload = () => {
        document.body.style.backgroundImage = `url(${img.src})`;
    };
}

// called once at beginning of event
async function sendChoiceToBackend(choice) {
    choicesContainer.style.display = 'none';
    enableInput = false;
    toggleInputMode();
    const response = await fetch('/api/choice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice })
    });
    const data = await response.json();
    setBackgroundImage(game_url);
    inDialogue = true;
    inEvent = true;
    if (data["end"]) { 
        inEvent = false;
    }
    updateStory(data);
}

async function sendUserInputToBackend(input) {
    enableInput = false;
    toggleInputMode();

    const postResponse = await fetch('/api/input-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input }),
    });

    if (!postResponse.ok) {
        console.error('Failed to send input data to backend.');
        return;
    }
    
    const eventSource = new EventSource('/api/input'); // Open the SSE connection
    let storyTextBuffer = '';

    eventSource.onmessage = (event) => {
        const data = event.data;
        // console.log(data)

        if (data === 'END_STREAM') {
            eventSource.close(); // Close the SSE stream
            fetchNonStreamData(); // Fetch the remaining non-stream data
            return;
        }

        // Append streamed text to the story
        storyTextBuffer += data;
        storyText.textContent = storyTextBuffer;
    };

    eventSource.onerror = () => {
        eventSource.close();
        // enableInput = true;
        // toggleInputMode();
    };
}

// Fetch the non-stream data after the story streaming ends
async function fetchNonStreamData() {
    const response = await fetch('/api/input/non-stream-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });

    const data = await response.json();
    setBackgroundImage(game_url);
    updateStory(data); // Update the rest of the game logic
}

function initStoryFromSave(data){
    inDialogue = data["inDialogue"];
    inEvent = !data["end"];
    enableInput = false;
    toggleInputMode();
    if(inDialogue){
        updateChoices(data["choices"]);
        setBackgroundImage(game_url);
    }
    else{
        setBackgroundImage(scene_url);
    }
    updateStory(data);
}

function updateStory(data) {
    if(data["ended"]){ // actually ended, redirect
        window.location.href = menuPageURL;
        return;
    }
    if(data["text"])
        storyText.textContent = data["text"];
    if(data["END"]){ // display ending type
        inEvent = false;
        inDialogue = true;
        return;
    }
    if(data["ending"] || data["beginning"]){ // disable load/save at beginning of ending
        document.querySelector(".game-button:nth-child(3)").disabled = true;
        document.querySelector(".game-button:nth-child(4)").disabled = true;
        document.querySelector(".game-button:nth-child(3)").classList.add("disabled");
        document.querySelector(".game-button:nth-child(4)").classList.add("disabled");
        if(data["ending"]){
            myAudio.setAttribute("src", "../static/epilogue.mp3");
            myAudio.play();
        }
    }
    if(data["middle"]){
        document.querySelector(".game-button:nth-child(3)").disabled = false;
        document.querySelector(".game-button:nth-child(4)").disabled = false;
        document.querySelector(".game-button:nth-child(3)").classList.remove("disabled");
        document.querySelector(".game-button:nth-child(4)").classList.remove("disabled");
    }
    if (data["end"]) { // ended conversation
        inEvent = false;
    }
    if(!inDialogue){
        updateChoices(data["choices"]);
    }
}

// called once at beginning of event
function updateChoices(choices) {
    choicesContainer.style.display = 'block';
    choicesContainer.innerHTML = '';
    if (choices && choices.length > 0) {
        setBackgroundImage(scene_url);
        choices.forEach(choice => {
            const button = document.createElement('button');
            button.textContent = choice;
            button.classList.add('choice-button');
            button.addEventListener('click', () => sendChoiceToBackend(choice));
            choicesContainer.appendChild(button);
        });
    }
}

function toggleInputMode() {
    if (enableInput) {
        if(!inEvent){
            newEvent();
        }
        else{
            storyText.style.display = 'none';
            userInputSection.style.display = 'flex';
            userInput.value = "";
            userInput.focus();
            userInput.setSelectionRange(0, 0); 
        }
    } else {
        storyText.style.display = 'block';
        storyText.textContent = "Loading..."
        userInputSection.style.display = 'none';
        storyInputBox.focus();
    }
}

submitButton.addEventListener('click', () => {
    const input = userInput.value.trim();
    if (input) {
        sendUserInputToBackend(input);
        userInput.value = '';
    }
});

storyInputBox.addEventListener('keypress', (event) => {
    if(!inDialogue){
        return;
    }
    if (event.key === 'Enter') {
        if(enableInput){
            const input = userInput.value.trim();
            if (input) {
                sendUserInputToBackend(input);
                userInput.value = "";
            }
        }
        else{
            enableInput = true;
            toggleInputMode();
        }
    }
});

storyInputBox.addEventListener('click', () => {
    if(!inDialogue){
        return;
    }
    if(!enableInput){
        enableInput = true;
        toggleInputMode();
    }
});


const saveMenu = document.getElementById("save-menu");
const saveSlotsContainer = document.getElementById("save-slots");
const saveMenuTitle = document.getElementById("save-menu-title");

let saveMode = false; // Tracks whether the menu is in Save mode or Load mode
let saveSlots = []; // Array to hold the state of save slots (filled or empty)

const backButtons = document.getElementsByClassName("back-button");
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

// Takes a screenshot of the page under the save menu
async function takeScreenshot() {
    try {
        const canvas = await html2canvas(document.body, {
            ignoreElements: (element) => element.id === "save-menu" // Ignore the save menu itself
        });

        // Scale down the image to a thumbnail size
        const thumbnailCanvas = document.createElement("canvas");
        const context = thumbnailCanvas.getContext("2d");
        const width = 150; // Thumbnail width
        const height = (canvas.height / canvas.width) * width; // Maintain aspect ratio
        thumbnailCanvas.width = width;
        thumbnailCanvas.height = height;

        context.drawImage(canvas, 0, 0, width, height);

        // Convert to base64
        return thumbnailCanvas.toDataURL("image/png").split(",")[1]; // Return base64 string without the prefix
    } catch (err) {
        console.error("Failed to take screenshot:", err);
        throw err;
    }
}

// Handles slot clicks based on mode (save or load)
async function handleSlotClick(index, isFilled) {
    if (saveMode) {
        // Save mode: Always save, even if the slot is filled
        try {
            const screenshotBase64 = await takeScreenshot(); // Take screenshot before saving
            const currentTime = new Date();
            const response = await fetch("/api/save", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ saveindex: index, inDialogue, inEvent, thumbnail: screenshotBase64, date: currentTime })
            });
            if (!response.ok) throw new Error("Failed to save game");
            saveSlots[index] = { filled: true, thumbnail: screenshotBase64, date: currentTime }; // Update local state
            renderSaveSlots(); // Re-render slots
        } catch (err) {
            console.error(err);
        }
    } else {
        // Load mode: Load only if the slot is filled
        if (!isFilled) return;
        try {
            const response = await fetch("/api/load", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ saveindex: index }),
            });
            if (!response.ok) throw new Error("Failed to load game");
            toggleMenu(saveMenu); // Close menu after loading
            const data = await response.json();
            initStoryFromSave(data)
        } catch (err) {
            console.error(err);
        }
    }
}

// Initializes the save menu when Save or Load is clicked
async function initializeSaveMenu(mode) {
    saveMode = mode === "save"; // Determine the mode
    saveMenuTitle.textContent = saveMode ? "Save Game" : "Load Save"; // Update the header text
    await fetchSaveSlots(); // Fetch the current state of save slots
    renderSaveSlots(); // Render the slots
    toggleMenu(saveMenu); // Show the save menu
}

// Event listeners for Save and Load buttons
document.querySelector(".game-button:nth-child(3)").addEventListener("click", () => initializeSaveMenu("save"));
document.querySelector(".game-button:nth-child(4)").addEventListener("click", () => initializeSaveMenu("load"));

const messageHistory = document.getElementById("message-history");
const messageHistoryContent = document.getElementById("message-history-content");

// Fetch and render message history
async function fetchAndRenderMessageHistory() {
    try {
        const response = await fetch("/api/history");
        if (!response.ok) throw new Error("Failed to fetch message history");
        
        const data = await response.json();
        const messages = data.messages;

        // Clear existing content
        messageHistoryContent.innerHTML = "";

        // Render messages
        messages.forEach(({ spk, msg }) => {
            const messageEntry = document.createElement("div");
            messageEntry.className = "message-entry";

            const speakerDiv = document.createElement("div");
            speakerDiv.className = "speaker";
            speakerDiv.textContent = spk;

            const messageDiv = document.createElement("div");
            messageDiv.className = "message";
            messageDiv.textContent = msg;

            messageEntry.appendChild(speakerDiv);
            messageEntry.appendChild(messageDiv);
            messageHistoryContent.appendChild(messageEntry);
        });

        // Scroll to the bottom to show the latest message
        toggleMenu(messageHistory);
        messageHistoryContent.scrollTop = messageHistoryContent.scrollHeight;
    } catch (err) {
        console.error(err);
    }
}

// Event listeners
document.querySelector(".game-button:nth-child(2)").addEventListener("click", () => fetchAndRenderMessageHistory());

const settingsMenu = document.getElementById("settings-menu");
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
document.querySelector(".game-button:nth-child(5)").addEventListener("click", () => renderSettingsMenu());

document.querySelector(".game-button:nth-child(1)").addEventListener("click", () => {
    // Redirect to the game page to start a new game
    window.location.href = menuPageURL;
});

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
    await fetch('/api/save-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
    });
}

// Check if save data is available in session storage
window.onload = () => {
    init_settings();
    const saveData = sessionStorage.getItem("saveData");
    document.querySelector(".game-button:nth-child(3)").disabled = false;
    document.querySelector(".game-button:nth-child(4)").disabled = false;
    document.querySelector(".game-button:nth-child(3)").classList.remove("disabled");
    document.querySelector(".game-button:nth-child(4)").classList.remove("disabled");
    if (saveData) {
        const parsedData = JSON.parse(saveData);
        initStoryFromSave(parsedData); // Call the initStoryFromSave function with the save data
        sessionStorage.removeItem("saveData"); // Clear save data after using it
    }
    else{
        newEvent();
    }
};