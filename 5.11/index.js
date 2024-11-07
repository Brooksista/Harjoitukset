const baseUrl = 'http://localhost:8000';

// Fetch and display initial data
document.addEventListener('DOMContentLoaded', () => {
    getTilatData();
    getVaraajatData();
    getVarauksetData();
});

function createList(items, listId, deleteFunction) {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';  // Clear the list
    for (let item of items) {
        const el = document.createElement('li');
        el.innerHTML = `${item.id}: ${item.name || item.varauspaiva || ''}`;
        el.innerHTML += ` <button onclick="${deleteFunction}(${item.id})">Delete</button>`;
        listEl.appendChild(el);
    }
}

// Fetch functions
function getTilatData() {
    axios.get(`${baseUrl}/tilat`)
        .then(response => createList(response.data.data, 'tilat-list', 'deleteTilat'))
        .catch(error => console.error('Error fetching Tilat:', error));
}

function getVaraajatData() {
    axios.get(`${baseUrl}/varaajat`)
        .then(response => createList(response.data.data, 'varaajat-list', 'deleteVaraaja'))
        .catch(error => console.error('Error fetching Varaajat:', error));
}

function getVarauksetData() {
    axios.get(`${baseUrl}/varaukset`)
        .then(response => createList(response.data.data, 'varaukset-list', 'deleteVaraus'))
        .catch(error => console.error('Error fetching Varaukset:', error));
}

// Add functions
function addTilat() {
    const name = document.getElementById('tilat-name').value;
    if (name) {
        axios.post(`${baseUrl}/tilat`, { name })
            .then(() => {
                getTilatData();
                document.getElementById('tilat-name').value = '';  // Clear input field
            })
            .catch(error => console.error('Error adding Tilat:', error));
    }
}

function addVaraajat() {
    const name = document.getElementById('varaajat-name').value;
    if (name) {
        axios.post(`${baseUrl}/varaajat`, { name })
            .then(() => {
                getVaraajatData();
                document.getElementById('varaajat-name').value = '';  // Clear input field
            })
            .catch(error => console.error('Error adding Varaaja:', error));
    }
}

function addVaraus() {
    const tilaId = document.getElementById('varaukset-tila-id').value;
    const varaajaId = document.getElementById('varaukset-varaaja-id').value;
    const date = document.getElementById('varaukset-date').value;
    if (tilaId && varaajaId && date) {
        axios.post(`${baseUrl}/varaukset`, { tila_id: tilaId, varaaja_id: varaajaId, varauspaiva: date })
            .then(() => {
                getVarauksetData();
                document.getElementById('varaukset-tila-id').value = '';
                document.getElementById('varaukset-varaaja-id').value = '';
                document.getElementById('varaukset-date').value = '';
            })
            .catch(error => console.error('Error adding Varaus:', error));
    }
}

// Delete functions
function deleteTilat(id) {
    axios.delete(`${baseUrl}/tilat/${id}`)
        .then(() => getTilatData())
        .catch(error => console.error('Error deleting Tilat:', error));
}

function deleteVaraaja(id) {
    axios.delete(`${baseUrl}/varaajat/${id}`)
        .then(() => getVaraajatData())
        .catch(error => console.error('Error deleting Varaaja:', error));
}

function deleteVaraus(id) {
    axios.delete(`${baseUrl}/varaukset/${id}`)
        .then(() => getVarauksetData())
        .catch(error => console.error('Error deleting Varaus:', error));
}
