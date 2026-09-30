const $ = (sel) => document.querySelector(sel);

let pieChart = null;
let lineChart = null;

async function api(path, options = {}) {
  const resp = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) {
    const detail = await resp.text();
    throw new Error(`${resp.status}: ${detail}`);
  }
  return resp.json();
}

function fmtDate(iso) {
  return iso ? iso.replace("T", " ").slice(0, 19) : "-";
}

function badgeFor(label) {
  return label === "fire"
    ? '<span class="badge badge-fire">FIRE</span>'
    : '<span class="badge badge-safe">NOT FIRE</span>';
}

async function loadHealth() {
  try {
    const res = await api("/health");
    const el = $("#health-badge");
    el.textContent = "sistem aktif";
    el.className = "badge badge-ok";
    if (!res.status || res.status !== "ok") throw new Error("bad");
  } catch {
    const el = $("#health-badge");
    el.textContent = "tidak terhubung";
    el.className = "badge badge-fire";
  }
}

async function loadStats() {
  try {
    const s = await api("/api/v1/stats");
    $("#stat-total").textContent = s.total;
    $("#stat-fire").textContent = s.fire_count;
    $("#stat-safe").textContent = s.not_fire_count;
    $("#stat-avg").textContent = Math.round(s.avg_probability * 100) + "%";
  } catch {
    $("#stat-total").textContent = "-";
  }
}

async function loadHistory() {
  try {
    const rows = await api("/api/v1/predictions?limit=50");
    renderHistoryTable(rows);
    renderCharts(rows);
  } catch {
    $("#history-table tbody").innerHTML =
      '<tr><td colspan="8">Tidak dapat memuat riwayat.</td></tr>';
  }
}

function renderHistoryTable(rows) {
  const tbody = $("#history-table tbody");
  if (!rows.length) {
    tbody.innerHTML =
      '<tr><td colspan="8">Belum ada riwayat. Lakukan prediksi pertama.</td></tr>';
    return;
  }
  tbody.innerHTML = rows
    .map(
      (r) => `
      <tr>
        <td>${r.id}</td>
        <td>${fmtDate(r.created_at)}</td>
        <td>${r.temperature}</td>
        <td>${r.ws}</td>
        <td>${r.rain}</td>
        <td>${r.rh}</td>
        <td>${(r.probability * 100).toFixed(1)}%</td>
        <td>${badgeFor(r.label)}</td>
      </tr>`
    )
    .join("");
}

function renderCharts(rows) {
  if (!window.Chart) return;

  const fireCount = rows.filter((r) => r.label === "fire").length;
  const notFireCount = rows.length - fireCount;

  if (pieChart) pieChart.destroy();
  if (lineChart) lineChart.destroy();

  pieChart = new Chart($("#chart-pie"), {
    type: "doughnut",
    data: {
      labels: ["Fire", "Not Fire"],
      datasets: [
        {
          data: [fireCount, notFireCount],
          backgroundColor: ["#e03131", "#2f9e44"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom", labels: { color: "#8b98a5" } } },
    },
  });

  const series = [...rows].reverse();
  lineChart = new Chart($("#chart-line"), {
    type: "line",
    data: {
      labels: series.map((r) => "#" + r.id),
      datasets: [
        {
          label: "Probabilitas Kebakaran",
          data: series.map((r) => r.probability),
          borderColor: "#e8590c",
          backgroundColor: "rgba(232, 89, 12, 0.15)",
          fill: true,
          tension: 0.3,
          pointBackgroundColor: series.map((r) =>
            r.label === "fire" ? "#e03131" : "#2f9e44"
          ),
          pointRadius: 4,
        },
        {
          label: "Threshold 0.21",
          data: series.map(() => 0.21),
          borderColor: "#4dabf7",
          borderDash: [6, 4],
          pointRadius: 0,
          tension: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 0,
          max: 1,
          ticks: { color: "#8b98a5" },
          grid: { color: "#2a333d" },
        },
        x: { ticks: { color: "#8b98a5", maxTicksLimit: 12 }, grid: { display: false } },
      },
      plugins: { legend: { labels: { color: "#8b98a5" } } },
    },
  });
}

function renderResult(res) {
  const box = $("#result");
  const badge = $("#result-badge");
  box.classList.remove("hidden");

  badge.textContent = res.label === "fire" ? "FIRE" : "NOT FIRE";
  badge.className =
    "badge-result badge-result badge-" + (res.label === "fire" ? "fire" : "safe");

  const pct = Math.round(res.probability * 100);
  $("#result-prob").textContent = pct + "%";
  $("#prob-fill").style.width = pct + "%";
  $("#result-threshold").textContent = res.threshold.toFixed(2) || "0.21";
  $("#result-state").textContent = res.label === "fire" ? "terdeteksi risiko" : "aman";
}

async function submitPrediction(event) {
  event.preventDefault();
  const btn = $("#predict-btn");
  btn.disabled = true;
  btn.textContent = "Menghitung...";

  const payload = {
    temperature: parseFloat($("#temperature").value),
    ws: parseFloat($("#ws").value),
    rain: parseFloat($("#rain").value),
    rh: parseFloat($("#rh").value),
  };

  try {
    const res = await api("/api/v1/predict", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    renderResult(res);
    $("#result-placeholder").classList.add("hidden");
    await Promise.all([loadStats(), loadHistory()]);
  } catch (err) {
    const badge = $("#result-badge");
    badge.textContent = "ERROR";
    badge.className = "badge-result badge-result badge-fire";
    $("#result-prob").textContent = "-";
    $("#prob-fill").style.width = "0%";
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.textContent = "Prediksi Risiko";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("#predict-form").addEventListener("submit", submitPrediction);
  loadHealth();
  loadStats();
  loadHistory();
  setInterval(() => {
    loadHealth();
    loadStats();
    loadHistory();
  }, 30000);
});