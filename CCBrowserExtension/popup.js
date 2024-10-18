document.getElementById('scrape').addEventListener('click', () => {
    // Send a message to the content script to scrape data
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        files: ['content.js']
      });
    });
  });
  