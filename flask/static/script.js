// This script handles the file upload and data display functionality
// It sends the uploaded CSV file to the server and displays the processed data
function handleFileUpload() {
    const input = document.getElementById('csvFileInput');
    const file = input.files[0];

    if (!file) {
        alert("Please select a CSV file first.");
        return;
    }

    const reader = new FileReader();

    reader.onload = function (e) {
        const text = e.target.result;
        const data = parseCSV(text);  // Parse CSV text to array

        // Update the h3 element with the first row's first cell
        if (data.length > 0 && data[0].length > 0) {
            const firstRow = data[0][0].trim();  // Get the first row's first cell
            const headerElement = document.getElementById('csvHeader');
            headerElement.textContent = firstRow;  // Set the text of the existing h3
        }

        // Strip the first row from the data before sending to the server
        const dataToSend = data.slice(1); // Skip the first row
        const updatedCSV = dataToSend.map(row => row.join(",")).join("\n"); // Convert back to CSV format

        const formData = new FormData();
        const blob = new Blob([updatedCSV], { type: 'text/csv' });
        formData.append('file', blob, 'updated.csv'); // Create a Blob to send

        // for testing
        //console.log("Sending CSV to server...");

        fetch('/upload-csv', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Testing purposes
            //console.log("Received processed data from Flask:", data);
            displayCSVData(data.data);  // Display the processed data
        })
        .catch(error => console.error('Error:', error));
    };

    reader.readAsText(file); // Read the CSV file as text
}

// Function to parse CSV string into a 2D array
function parseCSV(text) {
    const rows = text.split("\n");
    return rows.map(row => row.split(","));
}

// Function to display the CSV data in a table
function displayCSVData(data) {
    const tableHead = document.querySelector('#csvTable thead');
    const tableBody = document.querySelector('#csvTable tbody');

    // Clear the table before adding new data
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';

    // Create table headers from the first row of the remaining data
    if (data.length > 0) {
        // Parse the first row as headers (splitting the string by commas)
        const headers = data[0].split(",");
        const headerRow = document.createElement('tr');

        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header.trim();  // Trim to remove excess spaces
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

        // Create table rows for the rest of the CSV data
        data.slice(1).forEach(row => {
            const rowElement = document.createElement('tr');
            
            // Split the row string into individual cells
            const cells = row.split(",");
            
            cells.forEach((cell, index) => {
                const td = document.createElement('td');
                
                // For the second column (index 1), create an anchor (link)
                if (index === 1) {
                    const link = document.createElement('a');
                    link.href = cell.trim();  // Set the href to the cell content
                    link.textContent = cell.trim();  // Display the same content as the link text
                    link.target = "_blank";  // Optional: open in a new tab
                    td.appendChild(link);  // Append the anchor to the table cell
                } else {
                    td.textContent = cell.trim();  // For other columns, just add text
                }
                
                rowElement.appendChild(td);
            });
            tableBody.appendChild(rowElement);
        });
    }
}


function openDownloadPage() {
    window.open("https://vault.bitwarden.com/#/send/c_KhY70Zy0u5WLIOAW3WAg/pax0MayOpTfDJHwWgS9Shg", "_blank");
}
