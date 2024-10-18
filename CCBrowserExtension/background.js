chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.data) {
      let csvContent = "data:text/csv;charset=utf-8,";
  
      message.data.forEach(rowArray => {
        let row = rowArray.join(",");
        csvContent += row + "\r\n";
      });
  
      // Download the CSV file
      let encodedUri = encodeURI(csvContent);
      chrome.downloads.download({
        url: encodedUri,
        filename: "scraped_data.csv"
      });
    }
  });
  