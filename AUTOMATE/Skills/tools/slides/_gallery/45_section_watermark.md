---
template: section_watermark
eyebrow: "TEMPLATE: section_watermark"
title: "Sensors are now in everything that ships"
subtitle: "Bench-marking the two trends that make IoT economics work in the next 24 months"
commentary_label: "WHAT'S DRIVEN IT"
commentary: |
  - Improved power management
  - Continued miniaturisation
  - Sensor unit cost down 70% since 2018
  - Software stacks now standard, not custom
watermark_text: "Sensors in everything"
kicker: "**Why this matters now.** The unit-economics threshold for embedded sensors crossed in 2024 — that's what makes the FY27 use cases viable, not the FY30 ones we discussed last quarter."
---

<div class="chart">
  <canvas id="sensors_models" width="540" height="180"></canvas>
</div>

<script>
new Chart(document.getElementById('sensors_models'), {
  type: 'bar',
  data: {
    labels: ['2020','2021','2022','2023','2024','2025'],
    datasets: [{ label: 'Models with accelerometer', data: [1, 4, 20, 142, 285, 305], backgroundColor: '#1f4287' }]
  },
  options: {
    responsive: false,
    plugins: { legend: { display: false }, title: { display: true, text: 'Smartphone models launched with accelerometer', font: { size: 11 }, color: '#555' } },
    scales: { y: { beginAtZero: true } }
  }
});
</script>
