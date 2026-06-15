---
template: data_chart_with_milestones
eyebrow: "TEMPLATE: data_chart_with_milestones"
title: "Brightline paywall conversion rate — what each intervention did"
subtitle: "Monthly conversion %, dotted lines mark interventions"
legend: "**A** Free tier removed · **B** Paywall meter dropped to 3 · **C** Email re-engagement launched · **D** Pricing test ended"
kicker: "**The lesson.** A and B were structural and stuck; C lifted but reverted; D moved the line in the wrong direction and got reversed."
---

<div class="chart">
  <canvas id="brightline_paywall" width="900" height="240"></canvas>
</div>

<script>
new Chart(document.getElementById('brightline_paywall'), {
  type: 'line',
  data: {
    labels: ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'],
    datasets: [{
      label: 'Conversion %',
      data: [2.1, 2.2, 2.6, 2.5, 2.8, 3.1, 3.0, 3.4, 3.3, 3.5, 3.1, 3.2],
      borderColor: '#1f4287',
      backgroundColor: 'rgba(31,66,135,0.10)',
      borderWidth: 2.5,
      tension: 0.3,
      fill: true,
      pointRadius: 3
    }]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, max: 4, title: { display: true, text: '% of meter-blocked sessions converting' } } }
  }
});
</script>
