---
template: data_small_multiples_2x2
eyebrow: "TEMPLATE: data_small_multiples_2x2"
title: "Lumera site-build pipeline — capacity, cost, and time-to-permit, by region"
subtitle: "FY26 actuals against the FY28 ambition (four regions, same y-scale within each panel)"
sm1_label: "REGION A — NORTH SEA"
sm1_body: |
  <div class="chart"><canvas id="sm_a" width="380" height="110"></canvas></div>
  <script>
  new Chart(document.getElementById('sm_a'), { type: 'bar', data: { labels: ['Capacity (GW)','Cost (£/MWh)','Permit (mo)'], datasets: [{ label: 'FY26', data: [0.5, 64, 38], backgroundColor: '#1f4287' }, { label: 'FY28 target', data: [1.1, 52, 22], backgroundColor: '#c9a96e' }] }, options: { responsive: false, plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { y: { beginAtZero: true } } } });
  </script>
sm2_label: "REGION B — IBERIAN PENINSULA"
sm2_body: |
  <div class="chart"><canvas id="sm_b" width="380" height="110"></canvas></div>
  <script>
  new Chart(document.getElementById('sm_b'), { type: 'bar', data: { labels: ['Capacity (GW)','Cost (£/MWh)','Permit (mo)'], datasets: [{ label: 'FY26', data: [0.3, 58, 24], backgroundColor: '#1f4287' }, { label: 'FY28 target', data: [0.9, 46, 18], backgroundColor: '#c9a96e' }] }, options: { responsive: false, plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { y: { beginAtZero: true } } } });
  </script>
sm3_label: "REGION C — BALTIC"
sm3_body: |
  <div class="chart"><canvas id="sm_c" width="380" height="110"></canvas></div>
  <script>
  new Chart(document.getElementById('sm_c'), { type: 'bar', data: { labels: ['Capacity (GW)','Cost (£/MWh)','Permit (mo)'], datasets: [{ label: 'FY26', data: [0.2, 71, 44], backgroundColor: '#1f4287' }, { label: 'FY28 target', data: [0.6, 58, 28], backgroundColor: '#c9a96e' }] }, options: { responsive: false, plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { y: { beginAtZero: true } } } });
  </script>
sm4_label: "REGION D — UK ONSHORE"
sm4_body: |
  <div class="chart"><canvas id="sm_d" width="380" height="110"></canvas></div>
  <script>
  new Chart(document.getElementById('sm_d'), { type: 'bar', data: { labels: ['Capacity (GW)','Cost (£/MWh)','Permit (mo)'], datasets: [{ label: 'FY26', data: [0.4, 49, 19], backgroundColor: '#1f4287' }, { label: 'FY28 target', data: [0.8, 44, 14], backgroundColor: '#c9a96e' }] }, options: { responsive: false, plugins: { legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { y: { beginAtZero: true } } } });
  </script>
kicker: "**Where the gap is biggest.** Permit time in Baltic is twice the ambition; that's the bottleneck for the FY28 case."
---
