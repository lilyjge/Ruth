// URL for the game page
const gamePageURL = "http://127.0.0.1:5000/";
const menu_url = "../static/menu.png"

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
    // Load mode: Load only if the slot is filled
    if (!isFilled) return;
    try {
        const response = await fetch("/api/load", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ saveindex: index, save: true}),
        });
        if (!response.ok) throw new Error("Failed to load game");
        toggleSaveMenu(); // Close menu after loading
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
    saveMenuTitle.textContent = "Load Game"; // Update the header text
    await fetchSaveSlots(); // Fetch the current state of save slots
    renderSaveSlots(); // Render the slots
    toggleSaveMenu(); // Show the save menu
}

// Event listener for Back button
saveMenuBackButton.addEventListener("click", toggleSaveMenu);

// Event listeners for buttons
document.getElementById("new-game").addEventListener("click", () => {
    // Redirect to the game page to start a new game
    window.location.href = gamePageURL;
});

document.getElementById("load-game").addEventListener("click", () => initializeSaveMenu());

document.getElementById("settings").addEventListener("click", () => {
    alert("Settings functionality coming soon!");
});

document.getElementById("about").addEventListener("click", () => {
    alert("About the game: A fascinating journey awaits!");
});

document.getElementById("quit").addEventListener("click", () => {
    window.close(); // Closes the tab/window (may require browser permission)
});

// Update background on load
window.onload = setBackgroundImage(menu_url);
