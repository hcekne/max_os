---
template: chart_with_stat_callouts
eyebrow: "TEMPLATE: chart_with_stat_callouts"
exhibit_label: "EXHIBIT 4"
title: "Adoption is real but uneven across regions"
subtitle: "More than half of operations have at least one agent in production, yet value capture lags deployment."
source: "Source: Illustrative survey of operations leaders, n=240. Fictional example, not real client data."
footer_left: "Confidential draft"
footer_right: "Vanta Logistics"
---

<div class="chart-stat__chart">
<div class="chart">
<canvas id="vanta_adopt" width="560" height="340"></canvas>
<div class="chart-caption">Share of sites running at least one production agent, by region</div>
</div>
</div>

<div class="chart-stat__rail">
<div class="stat-callout">
<span class="stat-callout__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17l6-6 4 4 8-8"/></svg></span>
<div class="stat-callout__body">
<div class="stat-callout__num">58%</div>
<div class="stat-callout__caption">of sites have an agent live, up from 19% a year ago</div>
</div>
</div>
<div class="stat-callout">
<span class="stat-callout__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span>
<div class="stat-callout__body">
<div class="stat-callout__num">11 wks</div>
<div class="stat-callout__caption">median time from pilot to first production workflow</div>
</div>
</div>
<div class="stat-callout">
<span class="stat-callout__icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M5 9l7-7 7 7"/></svg></span>
<div class="stat-callout__body">
<div class="stat-callout__num">2.3x</div>
<div class="stat-callout__caption">throughput gain at the most mature sites versus baseline</div>
</div>
</div>
</div>

<script>
new Chart(document.getElementById('vanta_adopt'), {
  type: 'bar',
  data: {
    labels: ['North America','UK & Ireland','Western Europe','Nordics','APAC'],
    datasets: [{ label: 'Sites with a live agent', data: [71, 58, 52, 47, 33], backgroundColor: '#1f4287' }]
  },
  options: {
    responsive: false,
    indexAxis: 'y',
    plugins: { legend: { display: false } },
    scales: {
      x: { beginAtZero: true, max: 100, title: { display: true, text: '% of sites', font: { size: 11 } }, grid: { color: '#ededed' } },
      y: { grid: { display: false } }
    }
  }
});
</script>
