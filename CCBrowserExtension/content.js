// Example of scraping table data
let tableData = [];
document.querySelectorAll('table tr').forEach(row => {
  let rowData = [];
  row.querySelectorAll('td').forEach(cell => rowData.push(cell.innerText));
  tableData.push(rowData);
});

// Send the scraped data to the background script for downloading
chrome.runtime.sendMessage({ data: tableData });
