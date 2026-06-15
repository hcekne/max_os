---
template: compare_mirror_bars
eyebrow: "TEMPLATE: compare_mirror_bars"
title: "Cost-to-serve gap: NorthBank trails peer median in five of six categories"
subtitle: "Annualised PCA servicing cost per active account, £, FY26"
left_label: "NORTHBANK"
right_label: "PEER MEDIAN"
kicker: "**Where the gap concentrates.** Branch + call-centre alone account for 64% of the variance — those are the two we're prioritising."
---

<div class="chart">
  <canvas id="mirror_cost" width="980" height="260"></canvas>
</div>

<script>
new Chart(document.getElementById('mirror_cost'), {
  type: 'bar',
  data: {
    labels: ['Branch servicing','Call centre','Digital channel','Fraud ops','Statements & post','Other ops'],
    datasets: [
      { label: 'NorthBank', data: [-86, -54, -12, -18, -9, -15], backgroundColor: '#1f4287' },
      { label: 'Peer median', data: [52, 38, 14, 12, 6, 11], backgroundColor: '#c9a96e' }
    ]
  },
  options: {
    indexAxis: 'y',
    responsive: false,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        stacked: false,
        ticks: { callback: v => '£' + Math.abs(v) },
        grid: { display: true }
      },
      y: { stacked: true }
    }
  }
});
</script>
