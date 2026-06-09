---
template: data_chart_full_width
eyebrow: "TEMPLATE: data_chart_full_width"
title: "Group revenue trajectory under the three scenarios"
subtitle: "FY22 actuals through FY28 forecast, indexed to FY22 = 100"
kicker: "**Why the upside case is plausible.** It needs only one of the three growth pockets to land — not all three."
---

<div class="chart">
  <canvas id="rev_trajectory" width="980" height="320"></canvas>
</div>

<script>
new Chart(document.getElementById('rev_trajectory'), {
  type: 'line',
  data: {
    labels: ['FY22','FY23','FY24','FY25','FY26','FY27','FY28'],
    datasets: [
      { label: 'Actual', data: [100,108,112,115,null,null,null], borderColor: '#111111', borderWidth: 3, tension: 0.15, pointRadius: 4 },
      { label: 'Plan-of-record', data: [null,null,null,115,119,124,128], borderColor: '#1f4287', borderDash: [6,4], borderWidth: 2.5, tension: 0.15, pointRadius: 4 },
      { label: 'Upside (with all three growth pockets)', data: [null,null,null,115,121,131,142], borderColor: '#c9a96e', borderWidth: 2.5, tension: 0.15, pointRadius: 4 }
    ]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 14, font: { size: 12 } } } },
    scales: { y: { beginAtZero: false, min: 95, title: { display: true, text: 'Revenue, indexed FY22 = 100' } } }
  }
});
</script>
