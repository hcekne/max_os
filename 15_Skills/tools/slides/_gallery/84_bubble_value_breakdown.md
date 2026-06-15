---
template: bubble_value_breakdown
eyebrow: "TEMPLATE: bubble_value_breakdown"
title: "Where the value at stake sits, by function"
subtitle: "Claims and underwriting hold two thirds of the addressable pool; service is large but lower-margin."
source: "Source: Illustrative value-at-stake sizing for template demonstration. Fictional example, not real client data."
footer_left: "Confidential draft"
footer_right: "Orenda Health"
---

<div class="bubble-value__chart">
<div class="chart">
<canvas id="orenda_value" width="560" height="360"></canvas>
<div class="chart-caption">Bubble area is proportional to annual value at stake (GBP m)</div>
</div>
</div>

<div class="bubble-value__legend">
<div class="bubble-value__item"><span class="bubble-value__dot"></span><span><span class="bubble-value__val">£82m</span> <span class="bubble-value__label">Claims automation</span></span></div>
<div class="bubble-value__item"><span class="bubble-value__dot"></span><span><span class="bubble-value__val">£64m</span> <span class="bubble-value__label">Underwriting</span></span></div>
<div class="bubble-value__item"><span class="bubble-value__dot bubble-value__dot--muted"></span><span><span class="bubble-value__val">£48m</span> <span class="bubble-value__label">Member service</span></span></div>
<div class="bubble-value__item"><span class="bubble-value__dot bubble-value__dot--muted"></span><span><span class="bubble-value__val">£29m</span> <span class="bubble-value__label">Fraud detection</span></span></div>
<div class="bubble-value__item"><span class="bubble-value__dot bubble-value__dot--muted"></span><span><span class="bubble-value__val">£17m</span> <span class="bubble-value__label">Provider network</span></span></div>
</div>

<script>
new Chart(document.getElementById('orenda_value'), {
  type: 'bubble',
  data: {
    datasets: [
      { label: 'Claims automation', data: [{x: 22, y: 70, r: 46}], backgroundColor: 'rgba(31,66,135,0.85)' },
      { label: 'Underwriting',      data: [{x: 58, y: 64, r: 40}], backgroundColor: 'rgba(31,66,135,0.85)' },
      { label: 'Member service',    data: [{x: 80, y: 38, r: 35}], backgroundColor: 'rgba(185,185,185,0.85)' },
      { label: 'Fraud detection',   data: [{x: 38, y: 28, r: 27}], backgroundColor: 'rgba(185,185,185,0.85)' },
      { label: 'Provider network',  data: [{x: 70, y: 18, r: 21}], backgroundColor: 'rgba(185,185,185,0.85)' }
    ]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { min: 0, max: 100, display: false, grid: { display: false } },
      y: { min: 0, max: 90, display: false, grid: { display: false } }
    }
  }
});
</script>
