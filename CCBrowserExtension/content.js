chrome.storage.sync.get(['toggleState'], function(result) {
  const isEnabled = result.toggleState === undefined ? true : result.toggleState; // Default to 'true' if undefined
  if (isEnabled) {
      console.log("Content script running on: ", window.location.href);
      
      // Function to scrape the class name
      const getClassName = () => {
          const classNameElement = document.querySelector('nav li:nth-child(2) span.ellipsible'); 
          console.log("Class Name Element: ", classNameElement);
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

          const className = getClassName();
          console.log("Retrieved Class Name: ", className);

          const csvData = [[className], ...tableData];

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
              setTimeout(waitForTable, 1000);
          }
      };

      // Start waiting for the table to load
      waitForTable();
  } else {
      console.log("Scraping is disabled.");
  }
});
