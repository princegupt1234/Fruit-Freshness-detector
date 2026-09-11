const historyList = document.getElementById('history-list');

function formatConfidence(value) {
  const numeric = Number(value ?? 0);
  if (Number.isNaN(numeric)) return '0%';
  return `${(numeric * 100).toFixed(1)}%`;
}

function renderHistory(items) {
  if (!items || items.length === 0) {
    historyList.innerHTML = '<div class="empty-state">No prediction records yet. Submit an image to create the first history entry.</div>';
    return;
  }

  historyList.innerHTML = items.map((entry) => `
    <div class="history-item">
      <div>
        <span class="history-title">${entry.produce_name || 'Unknown'}</span>
        <small>${entry.produce_category || 'Unknown category'}</small>
      </div>
      <div>
        <span class="badge-pill">${entry.freshness_status || 'Unknown'}</span>
      </div>
      <div>
        <strong>${formatConfidence(entry.confidence)}</strong>
      </div>
    </div>
  `).join('');
}

async function loadHistory() {
  try {
    const response = await fetch('http://localhost:8000/api/history');
    const data = await response.json();
    renderHistory(data.history || []);
  } catch (error) {
    historyList.innerHTML = '<div class="empty-state">Unable to load history right now. Please check the backend server.</div>';
  }
}

loadHistory();
