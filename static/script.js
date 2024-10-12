function search() {
    const query = document.getElementById('search-input').value;
    const dataset = document.getElementById('dataset').value;
    if (!query) {
        alert('Please enter a query.');
        return;
    }

    // Clear results and show loading animation
    document.getElementById('results').innerHTML = '';
    document.getElementById('loading').style.display = 'block';

    fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}&d=${encodeURIComponent(dataset)}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading animation
            document.getElementById('loading').style.display = 'none';
            displayResults(data);
        })
        .catch(error => {
            // Hide loading animation
            document.getElementById('loading').style.display = 'none';
            console.error('Error fetching data:', error);
        });
}



function displayResults(results) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    if (Object.keys(results).length === 0) {
        const noResults = document.createElement('div');
        noResults.id = 'no-results';
        noResults.textContent = 'No results found!';
        resultsContainer.appendChild(noResults);
        return;
    }

    let delay = 0;
    for (const key in results) {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';

        const title = document.createElement('h3');
        title.textContent = results[key];
        resultItem.appendChild(title);

        const body = document.createElement('p');
        body.textContent = `Document ID: ${key}`;
        resultItem.appendChild(body);

        resultItem.style.animationDelay = `${delay}s`;
        delay += 0.2;

        resultsContainer.appendChild(resultItem);
    }
}
