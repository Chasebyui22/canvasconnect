// Function to load the toggle state from storage
function loadToggleState() {
    chrome.storage.sync.get(['toggleState'], function(result) {
        const toggleSwitch = document.getElementById('toggleSwitch');
        toggleSwitch.checked = result.toggleState === undefined ? true : result.toggleState; // Default to 'true' if undefined
    });
}

// Function to save the toggle state to storage
function saveToggleState(isOn) {
    chrome.storage.sync.set({ toggleState: isOn }, function() {
        console.log(`Toggle state saved: ${isOn}`);
    });
}

// Event listener for the toggle switch
document.getElementById('toggleSwitch').addEventListener('change', function() {
    const isOn = this.checked;
    saveToggleState(isOn);
});

// Load the toggle state when the popup is opened
loadToggleState();
