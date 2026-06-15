---
template: data_waterfall_with_callout
eyebrow: "TEMPLATE: data_waterfall_with_callout"
title: "How NorthBank's FY28 cost base reduces from £1.4B to £1.1B"
subtitle: "Cost waterfall, £M, FY26 actuals → FY28 plan"
callout_label: "WHY IT LANDS"
callout_body: |
  Three of the four levers (1, 2, 4) are operational and don't need policy change.
  Lever 3 (estate) is structural but board-approved.
  Net £286M out by FY28.
kicker: "**The shape of the story.** Front-loaded by operational levers; the structural lever (estate) adds the marginal £62M that gets us under the 1.1B floor."
---

<div class="chart">
  <canvas id="nb_waterfall" width="620" height="340"></canvas>
</div>

<script>
new Chart(document.getElementById('nb_waterfall'), {
  type: 'bar',
  data: {
    labels: ['FY26 base', 'Ops efficiency', 'Workforce flex', 'Estate', 'Procurement', 'FY28 plan'],
    datasets: [{
      data: [1428, -94, -68, -62, -62, 1142],
      backgroundColor: ['#1f4287', '#3a6cc4', '#3a6cc4', '#3a6cc4', '#3a6cc4', '#1f4287']
    }]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true, max: 1500, title: { display: true, text: 'Cost base, £M' } } }
  }
});
</script>
