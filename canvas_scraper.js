// Canvas Scraper Chrome Extension

// Function to scrape user data from Canvas
function scrapeCanvasUsers() {
    const users = [];
    const userElements = document.querySelectorAll('.roster_user_name');
    
    userElements.forEach(element => {
        const name = element.textContent.trim();
        const email = element.getAttribute('href').split(':')[1];
        const role = element.closest('tr').querySelector('.roster_user_role').textContent.trim();
        
        users.push({ name, email, role });
    });
    
    return users;
}

// Function to download data as CSV
function downloadCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," 
        + "Name,Email,Role\n"
        + data.map(row => `${row.name},${row.email},${row.role}`).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
}

// Add a button to the Canvas page
function addScraperButton() {
    const button = document.createElement('button');
    button.textContent = 'Download Canvas Users';
    button.style.position = 'fixed';
    button.style.top = '10px';
    button.style.right = '10px';
    button.style.zIndex = '9999';
    
    button.addEventListener('click', () => {
        const users = scrapeCanvasUsers();
        downloadCSV(users, 'canvas_users.csv');
    });
    
    document.body.appendChild(button);
}

// Run the script when the page is loaded
window.addEventListener('load', addScraperButton);
