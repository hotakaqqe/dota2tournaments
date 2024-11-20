document.addEventListener("DOMContentLoaded", function() {
    fetchTournaments();
});

function fetchTournaments() {
    fetch("http://127.0.0.1:5000/api/tournaments")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Tournaments Data:", data);

            const tableBody = document.getElementById("tournament-data");

            if (data.length === 0) {
                const row = document.createElement("tr");
                row.innerHTML = `<td colspan="4">No tournaments available</td>`;
                tableBody.appendChild(row);
            } else {
                data.forEach(tournament => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${tournament.name}</td>
                        <td>${formatDate(tournament.start_date)}</td>
                        <td>${formatDate(tournament.end_date)}</td>
                        <td>$${tournament.prize_pool.toLocaleString()}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching tournaments:", error);
            alert("Failed to load tournament data.");
        });
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options); 
}
