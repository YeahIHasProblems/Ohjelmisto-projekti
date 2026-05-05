let isPaused = false;

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        togglePause();
    }
});

function togglePause() {
    const menu = document.getElementById('pause-menu');
    if (!menu) return;
    isPaused = !isPaused;
    if (isPaused) {
        menu.style.display = 'flex';
        updatePauseStats();
    } else {
        menu.style.display = 'none';
    }
}

async function updatePauseStats() {
    try {
        const response = await fetch('/get_stats');
        const data = await response.json();
        document.getElementById('p-name').innerText = data.name || "---";
        document.getElementById('p-money').innerText = data.money || 0;
        document.getElementById('p-goal').innerText = data.goal || 0;
    } catch(e) {
        console.error("Stats update failed", e);
    }
}

async function saveGame() {
    try {
        const response = await fetch('/save', { method: 'POST' });
        if (response.ok) alert("Peli tallennettu!");
    } catch(e) {
        alert("Tallennus epäonnistui.");
    }
}