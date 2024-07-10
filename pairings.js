let addedPlayers = new Set();

document.getElementById('chessaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const cid = document.getElementById('cid').value;
    const name = document.getElementById('name').value;

    const formData = new URLSearchParams();
    formData.append('cid', cid);
    formData.append('name', name);

    fetch('/add_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    })
    .then(response => response.text())
    .then(text => {
        console.log('Server response:', text);
        try {
            const data = JSON.parse(text);
            if (data.error) {
                alert(data.error);
            } else {
                if (!addedPlayers.has(data.cid)) {
                    addPlayerToTable(data);
                    addedPlayers.add(data.cid);
                } else {
                    alert('Player is already added.');
                }
            }
        } catch (error) {
            console.error('Error parsing JSON:', error, 'Response text:', text);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function addPlayerToTable(player) {
    const table = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    const sRankCell = newRow.insertCell(0);
    const nameCell = newRow.insertCell(1);
    const sexCell = newRow.insertCell(2);
    const ratingCell = newRow.insertCell(3);
    const removeCell = newRow.insertCell(4);

    let lastName = '';
    let firstNameInitials = '';

    if (player.name.includes(',')) {
        const nameParts = player.name.split(',');
        lastName = nameParts[0].trim().toUpperCase();
        firstNameInitials = nameParts[1].trim().toUpperCase();
    } else if (player.name.includes(' ')) {
        const nameParts = player.name.split(' ');
        lastName = nameParts[0].trim().toUpperCase();
        firstNameInitials = nameParts.slice(1).map(part => part[0].toUpperCase()).join('');
    } else {
        lastName = player.name.trim().toUpperCase();
        firstNameInitials = '';
    }
    

    const fullName = `${lastName}, ${firstNameInitials}`;
    const sex = player.sex ? player.sex.toUpperCase() : 'N/A';

    sRankCell.textContent = ''; // This needs to be calculated or set later
    nameCell.textContent = fullName;
    sexCell.textContent = sex;
    ratingCell.textContent = player.official_published_rating;
    removeCell.innerHTML = '<button onclick="removePlayer(this)">X</button>';
    newRow.cells[0].dataset.cid = player.cid;

    sortTableByRating();
    updateRanks();
}

function removePlayer(button) {
    const row = button.parentNode.parentNode;
    const table = row.parentNode;
    const cid = row.cells[0].dataset.cid;
    addedPlayers.delete(cid);
    table.removeChild(row);
    updateRanks();
}

function sortTableByRating() {
    const table = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    const rows = Array.from(table.rows);

    rows.sort((a, b) => {
        const ratingA = parseFloat(a.cells[3].textContent);
        const ratingB = parseFloat(b.cells[3].textContent);
        return ratingB - ratingA;
    });

    rows.forEach(row => table.appendChild(row));
}

function updateRanks() {
    const table = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    const rows = Array.from(table.rows);

    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

function savePlayers() {
    // Redirect to the pairing options page
    window.location.href = '/pairing_options';
}
