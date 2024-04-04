// Get the header element with the id "BTCPrice"
const header = document.getElementById("BTCPrice");


// The data you want to send to the Python function
const data = {
    key: 'value'
};

function fetchBTCPrice(){
    // Make the API call
    fetch('http://127.0.0.1:5001/btc_Price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Convert the data to a string so it can be inserted into the HTML
        const dataString = JSON.stringify(data, null, 2);

        // Insert the data into the element
        header.textContent = `BTC: $${dataString}`;
    })
    .catch(error => console.error('Error:', error));
}

fetchBTCPrice();
setInterval(fetchBTCPrice, 15000);