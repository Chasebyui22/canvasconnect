console.log("Content script running on: ", window.location.href);

// Function to scrape the class name
const getClassName = () => {
  // Select the element containing the class name
  const classNameElement = document.querySelector('nav li:nth-child(2) span.ellipsible'); // Use the appropriate selector
  console.log("Class Name Element: ", classNameElement); // Log the selected element
  return classNameElement ? classNameElement.innerText.trim() : 'Class Name Not Found';
};

// Function to scrape table data
const scrapeTableData = () => {
  let tableData = [];
  const tables = document.querySelectorAll('table');

  tables.forEach(table => {
    table.querySelectorAll('tr').forEach(row => {
      let rowData = [];
      row.querySelectorAll('td').forEach(cell => rowData.push(cell.innerText));
      tableData.push(rowData);
    });
  });

  // Get the class name
  const className = getClassName();
  console.log("Retrieved Class Name: ", className); // Log the retrieved class name

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
  }
};

// Start waiting for the table to load
waitForTable();
