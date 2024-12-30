const storyText = document.getElementById('story-text');
const choicesContainer = document.getElementById('choices-container');
const userInputSection = document.getElementById('user-input-section');
const userInput = document.getElementById('user-input');
const submitButton = document.getElementById('submit-button');
const storyInputBox = document.getElementById('story-input-box');
const game_url = '../static/gameplay.png';
const scene_url = '../static/scene.png';
const menuPageURL = "http://127.0.0.1:5000/home"
inDialogue = false; // determines whether to render choices box
inEvent = false; // for event transitions
enableInput = false; // determines story text or user input mode

function newEvent(){
    inDialogue = false;
    inEvent = false;
    enableInput = false;
    toggleInputMode();
    // Initialize with default choices
    fetch('/api/initialize')
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
    updateStory(data);
}

async function sendUserInputToBackend(input) {
    enableInput = false;
    toggleInputMode();
    const response = await fetch('/api/input', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input })
    });

    const data = await response.json();
    setBackgroundImage(game_url);
    updateStory(data);
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
    storyText.textContent = data["text"];
    if (data["end"]) { 
        // newEvent();
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
            userInput.focus();
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
                userInput.value = '';
            }
        }
        else{
            enableInput = true;
            toggleInputMode();
        }
    }
});


const saveMenu = document.getElementById("save-menu");
const saveSlotsContainer = document.getElementById("save-slots");
const saveMenuBackButton = document.getElementById("save-menu-back-button");
const saveMenuTitle = document.getElementById("save-menu-title");

let saveMode = false; // Tracks whether the menu is in Save mode or Load mode
let saveSlots = []; // Array to hold the state of save slots (filled or empty)

// Toggles the visibility of the save menu
function toggleSaveMenu() {
    saveMenu.style.display = saveMenu.style.display === "none" ? "flex" : "none";
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
    saveSlots.forEach((isFilled, index) => {
        const slot = document.createElement("div");
        slot.className = `save-slot ${isFilled ? "filled" : ""}`;
        slot.textContent = isFilled ? `Save Slot ${index + 1}` : "Empty Slot";
        slot.addEventListener("click", () => handleSlotClick(index, isFilled));
        saveSlotsContainer.appendChild(slot);
    });
}

// Handles slot clicks based on mode (save or load)
async function handleSlotClick(index, isFilled) {
    if (saveMode) {
        // Save mode: Always save, even if the slot is filled
        try {
            const response = await fetch("/api/save", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ saveindex: index, inDialogue, inEvent}),
            });
            if (!response.ok) throw new Error("Failed to save game");
            saveSlots[index] = true; // Update local state
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
            toggleSaveMenu(); // Close menu after loading
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
    toggleSaveMenu(); // Show the save menu
}

// Event listeners for Save and Load buttons
document.querySelector(".game-button:nth-child(3)").addEventListener("click", () => initializeSaveMenu("save"));
document.querySelector(".game-button:nth-child(4)").addEventListener("click", () => initializeSaveMenu("load"));

// Event listener for Back button
saveMenuBackButton.addEventListener("click", toggleSaveMenu);


const messageHistory = document.getElementById("message-history");
const messageHistoryContent = document.getElementById("message-history-content");
const messageHistoryBackButton = document.getElementById("message-history-back-button");

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
        messageHistoryContent.scrollTop = messageHistoryContent.scrollHeight;
    } catch (err) {
        console.error(err);
    }
}

// Show the message history
function showMessageHistory() {
    messageHistory.style.display = "flex";
    fetchAndRenderMessageHistory();
}

// Hide the message history
function hideMessageHistory() {
    messageHistory.style.display = "none";
}

// Event listeners
document.querySelector(".game-button:nth-child(2)").addEventListener("click", showMessageHistory);
messageHistoryBackButton.addEventListener("click", hideMessageHistory);

document.querySelector(".game-button:nth-child(1)").addEventListener("click", () => {
    // Redirect to the game page to start a new game
    window.location.href = menuPageURL;
});

// Check if save data is available in session storage
window.onload = () => {
    const saveData = sessionStorage.getItem("saveData");
    if (saveData) {
        const parsedData = JSON.parse(saveData);
        initStoryFromSave(parsedData); // Call the initStoryFromSave function with the save data
        sessionStorage.removeItem("saveData"); // Clear save data after using it
    }
    else{
        newEvent();
    }
};