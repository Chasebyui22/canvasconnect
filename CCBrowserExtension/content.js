// Function to scrape the class name
const getClassName = () => {
  const classNameElement = document.querySelector('nav li:nth-child(2) span.ellipsible');
  return classNameElement ? classNameElement.innerText.trim() : 'Class Name Not Found';
};

// Function to scrape table data
const scrapeTableData = () => {
  let tableData = [];
  const tables = document.querySelectorAll('table');

  tables.forEach(table => {
    table.querySelectorAll('tr').forEach(row => {
      let rowData = [];
      
      // Only scrape from the 2nd <td> onward to avoid initials (assuming the initials are in the first column)
      row.querySelectorAll('td').forEach((cell, index) => {
        if (index > 0) { // Skip the first cell (index 0)
          rowData.push(cell.innerText.trim());
        }
      });

      if (rowData.length > 0) {
        tableData.push(rowData);
      }
    });
  });

  // Get the class name
  const className = getClassName();

  // Prepend the class name to the data
  const csvData = [[className], ...tableData]; // Add class name as the first row

  // Send scraped data
  if (csvData.length > 0) {
    chrome.runtime.sendMessage({ data: csvData });
  } else {
    chrome.runtime.sendMessage({ noData: true });
  }
};

// Function to wait for the table to load
const waitForTable = () => {
  const tables = document.querySelectorAll('table');
  if (tables.length > 0) {
    scrapeTableData();
  } else {
    setTimeout(waitForTable, 1000); // Retry after 1 second
};
}

// Start waiting for the table to load
waitForTable();
