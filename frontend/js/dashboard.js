const DEFAULT_STATS = {
  total_predictions: 0,
  fresh_predictions: 0,
  moderately_fresh_predictions: 0,
  rotten_predictions: 0,
  unknown_predictions: 0,
  average_confidence: 0,
};

let freshnessChart;
let categoryChart;
let confidenceChart;
let activityChart;

function updateStats(stats) {
  document.getElementById('total-predictions').textContent = stats.total_predictions || 0;
  document.getElementById('fresh-count').textContent = stats.fresh_predictions || 0;
  document.getElementById('moderate-count').textContent = stats.moderately_fresh_predictions || 0;
  document.getElementById('rotten-count').textContent = stats.rotten_predictions || 0;
  document.getElementById('unknown-count').textContent = stats.unknown_predictions || 0;
  document.getElementById('avg-confidence').textContent = `${Number(stats.average_confidence || 0).toFixed(1)}%`;
}

function drawCharts(stats) {
  if (freshnessChart) freshnessChart.destroy();
  if (categoryChart) categoryChart.destroy();
  if (confidenceChart) confidenceChart.destroy();
  if (activityChart) activityChart.destroy();

  freshnessChart = new Chart(document.getElementById('freshnessChart'), {
    type: 'doughnut',
    data: {
      labels: ['Fresh', 'Moderately Fresh', 'Rotten', 'Unknown'],
      datasets: [{
        data: [
          stats.fresh_predictions || 0,
          stats.moderately_fresh_predictions || 0,
          stats.rotten_predictions || 0,
          stats.unknown_predictions || 0,
        ],
        backgroundColor: ['#16a34a', '#f59e0b', '#dc2626', '#64748b'],
      }],
    },
  });

  categoryChart = new Chart(document.getElementById('categoryChart'), {
    type: 'bar',
    data: {
      labels: ['Fruit', 'Vegetable'],
      datasets: [{
        label: 'Counts',
        data: [stats.fresh_predictions || 0, stats.rotten_predictions || 0],
        backgroundColor: ['#1f6feb', '#0ea5e9'],
      }],
    },
  });

  confidenceChart = new Chart(document.getElementById('confidenceChart'), {
    type: 'line',
    data: {
      labels: ['0%', '25%', '50%', '75%', '100%'],
      datasets: [{
        label: 'Confidence',
        data: [0, 0, 0, 0, stats.average_confidence || 0],
        borderColor: '#1f6feb',
        fill: false,
      }],
    },
  });

  activityChart = new Chart(document.getElementById('activityChart'), {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Predictions',
        data: [0, 0, 0, 0, 0, stats.total_predictions || 0],
        backgroundColor: '#14b8a6',
      }],
    },
  });
}

async function loadDashboard() {
  try {
    const response = await fetch('http://localhost:8000/api/dashboard/statistics');
    const data = await response.json();
    const stats = { ...DEFAULT_STATS, ...data };
    updateStats(stats);
    drawCharts(stats);
  } catch (error) {
    updateStats(DEFAULT_STATS);
    drawCharts(DEFAULT_STATS);
  }
}

loadDashboard();
