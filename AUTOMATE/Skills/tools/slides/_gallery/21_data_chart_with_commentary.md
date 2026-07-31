---
template: data_chart_with_commentary
eyebrow: "TEMPLATE: data_chart_with_commentary"
title: "Vanta Logistics — service-level erosion has accelerated since Q3"
subtitle: "Same-day SLA performance, four-week rolling average"
commentary_label: "WHAT THE CHART SHOWS"
commentary: |
  - The 94% promised SLA held until the Q3 carrier mix change
  - Drop is sharper on the West-coast network than on the East
  - October recovery is real but partial — still 5 pts below promise
kicker: "**The implication.** The fall is not seasonal noise — it lines up with the carrier transition, which means it's fixable by operational redesign."
---

<div class="chart">
  <canvas id="vanta_sla" width="640" height="320"></canvas>
</div>

<script>
new Chart(document.getElementById('vanta_sla'), {
  type: 'line',
  data: {
    labels: ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr'],
    datasets: [
      { label: 'Same-day SLA', data: [94,94,93,94,93,92,90,87,86,85,86,88,89], borderColor: '#1f4287', backgroundColor: 'rgba(31,66,135,0.08)', tension: 0.25, fill: true, borderWidth: 2.5, pointRadius: 0 },
      { label: 'Promise (94%)', data: Array(13).fill(94), borderColor: '#c9a96e', borderDash: [4,4], borderWidth: 1.5, pointRadius: 0 }
    ]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } },
    scales: { y: { beginAtZero: false, min: 80, max: 100, title: { display: true, text: '% same-day SLA', font: { size: 11 } } } }
  }
});
</script>
