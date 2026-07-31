---
template: data_paired_charts_compare
eyebrow: "TEMPLATE: data_paired_charts_compare"
title: "Halcyon Retail — share of revenue by channel, before and after"
subtitle: "FY22 vs FY26, % of group revenue"
left_label: "FY22"
right_label: "FY26"
left_body: |
  <div class="chart"><canvas id="hal_fy22" width="380" height="300"></canvas></div>
  <script>
  new Chart(document.getElementById('hal_fy22'), {
    type: 'doughnut',
    data: { labels: ['Stores','.com','Wholesale','Resale'], datasets: [{ data: [62, 24, 13, 1], backgroundColor: ['#1f4287','#3a6cc4','#7da0d6','#c9a96e'] }] },
    options: { responsive: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } } }
  });
  </script>
right_body: |
  <div class="chart"><canvas id="hal_fy26" width="380" height="300"></canvas></div>
  <script>
  new Chart(document.getElementById('hal_fy26'), {
    type: 'doughnut',
    data: { labels: ['Stores','.com','Wholesale','Resale'], datasets: [{ data: [44, 38, 11, 7], backgroundColor: ['#1f4287','#3a6cc4','#7da0d6','#c9a96e'] }] },
    options: { responsive: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } } }
  });
  </script>
kicker: "**What's moved.** .com climbed 14 pts, stores fell 18 pts, resale crossed 5% for the first time."
---
