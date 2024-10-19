console.log("Content script running on: ", window.location.href);

const waitForTable = () => {
  const tables = document.querySelectorAll('table');
  if (tables.length > 0) {
    scrapeTableData(tables);
  } else {
    setTimeout(waitForTable, 1000); // Retry after 1 second
  }
};

const scrapeTableData = (tables) => {
  let tableData = [];
  tables.forEach(table => {
    table.querySelectorAll('tr').forEach(row => {
      let rowData = [];
      row.querySelectorAll('td').forEach(cell => rowData.push(cell.innerText));
      tableData.push(rowData);
    });
  });

  // Send scraped data
  if (tableData.length > 0) {
    chrome.runtime.sendMessage({ data: tableData });
  } else {
    chrome.runtime.sendMessage({ noData: true });
  }
};

waitForTable();


