const $ = (id) => document.getElementById(id);

const pages = {
  dashboard: $("pageDashboard"),
  scan: $("pageScan"),
  history: $("pageHistory"),
};

function showPage(name) {
  Object.values(pages).forEach(p => p.classList.add("hidden"));
  pages[name].classList.remove("hidden");
}

$("navDashboard").onclick = () => { showPage("dashboard"); refreshAll(); };
$("navScan").onclick = () => showPage("scan");
$("navHistory").onclick = () => { showPage("history"); loadHistory(); };

let trendChart, distChart;

function setKPIs({ total, avg, safe, global }) {
  $("kpiTotal").textContent = total;
  $("kpiAvg").textContent = `${avg}%`;
  $("kpiSafe").textContent = safe;
  $("kpiGlobal").textContent = global;
}

function levelFromAvg(avg) {
  if (avg >= 70) return "HIGH";
  if (avg >= 40) return "MEDIUM";
  if (avg > 0) return "LOW";
  return "N/A";
}

function buildCharts(items) {
  const scores = [...items].reverse().map(x => x.score);
  const labels = scores.map((_, i) => `${i + 1}`);

  const low = items.filter(x => x.level === "Low").length;
  const med = items.filter(x => x.level === "Medium").length;
  const high = items.filter(x => x.level === "High").length;

  // Trend
  const tctx = $("trendChart").getContext("2d");
  if (trendChart) trendChart.destroy();
  trendChart = new Chart(tctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Risk Score",
        data: scores,
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 3,
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.08)" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.08)" }, suggestedMin: 0, suggestedMax: 100 }
      }
    }
  });

  // Distribution
  const dctx = $("distChart").getContext("2d");
  if (distChart) distChart.destroy();
  distChart = new Chart(dctx, {
    type: "doughnut",
    data: {
      labels: ["Low", "Medium", "High"],
      datasets: [{
        data: [low, med, high],
        borderWidth: 0,
      }]
    },
    options: {
      cutout: "65%",
      plugins: {
        legend: { labels: { color: "#cbd5e1" } }
      }
    }
  });
}

function renderRecent(items) {
  if (!items.length) {
    $("recentList").textContent = "No scans yet.";
    return;
  }
  const recent = items.slice(0, 6).map(x => {
    return `<div class="flex items-center justify-between gap-3 py-2 border-b border-slate-700/30">
      <div class="text-slate-200 text-sm truncate max-w-[70%]">${x.url}</div>
      <div class="text-xs text-slate-400">${x.level} · ${x.score}</div>
    </div>`;
  }).join("");
  $("recentList").innerHTML = recent;
}

async function refreshAll() {
  const res = await fetch("/api/history?limit=200");
  const data = await res.json();
  const items = data.items || [];
  const total = items.length;
  const avg = total ? Math.round(items.reduce((a, b) => a + b.score, 0) / total) : 0;
  const safe = items.filter(x => x.level === "Low").length;
  const global = levelFromAvg(avg);

  setKPIs({ total, avg, safe, global });
  buildCharts(items);
  renderRecent(items);
}

$("runScan").onclick = async () => {
  const input = $("scanInput").value.trim();
  if (!input) return;

  $("scanResult").classList.add("hidden");
  $("aiBlock").classList.add("hidden");
  $("aiReport").textContent = "";

  $("runScan").textContent = "Scanning...";
  $("runScan").disabled = true;

  try {
    const res = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input, generate_ai: $("genAI").checked })
    });

    const out = await res.json();

    $("scanResult").classList.remove("hidden");
    $("scanTime").textContent = `Scan completed in ${out.scan_seconds.toFixed(2)}s`;

    $("rScore").textContent = `${out.score}/100`;
    $("rLevel").textContent = out.level;
    $("rCat").textContent = out.category;
    $("rConf").textContent = `${Math.round(out.confidence * 100)}%`;

    $("redirectChain").textContent = out.redirect_chain.join("\n");

    $("reasons").innerHTML = "";
    (out.reasons || []).forEach(r => {
      const li = document.createElement("li");
      li.textContent = r;
      $("reasons").appendChild(li);
    });

    $("features").textContent = JSON.stringify(out.features, null, 2);

    if (out.ai_report) {
      $("aiBlock").classList.remove("hidden");
      $("aiReport").textContent = out.ai_report;
    }

    // Refresh dashboard KPIs & charts
    refreshAll();

  } catch (e) {
    alert("Scan failed. Check backend logs.");
  } finally {
    $("runScan").textContent = "Run Scan";
    $("runScan").disabled = false;
  }
};

async function loadHistory() {
  const res = await fetch("/api/history?limit=200");
  const data = await res.json();
  const items = data.items || [];

  const wrap = $("historyList");
  wrap.innerHTML = "";

  if (!items.length) {
    wrap.innerHTML = `<div class="glass rounded-3xl p-6 text-slate-300">No previous scans found.</div>`;
    return;
  }

  items.forEach(x => {
    const card = document.createElement("div");
    card.className = "glass glow rounded-3xl p-6";
    card.innerHTML = `
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div class="text-sm text-slate-300 truncate max-w-[75%]">${x.url}</div>
        <div class="text-xs text-slate-500">${x.ts}</div>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
        <div class="glass rounded-2xl p-4"><div class="text-xs text-slate-400">Score</div><div class="text-xl font-extrabold">${x.score}</div></div>
        <div class="glass rounded-2xl p-4"><div class="text-xs text-slate-400">Level</div><div class="text-xl font-extrabold">${x.level}</div></div>
        <div class="glass rounded-2xl p-4"><div class="text-xs text-slate-400">Category</div><div class="text-sm font-bold mt-1">${x.category}</div></div>
        <div class="glass rounded-2xl p-4"><div class="text-xs text-slate-400">Confidence</div><div class="text-xl font-extrabold">${Math.round(x.confidence * 100)}%</div></div>
      </div>
    `;
    wrap.appendChild(card);
  });
}

$("clearHistory").onclick = async () => {
  if (!confirm("Delete all scan history?")) return;
  await fetch("/api/history/clear", { method: "POST" });
  loadHistory();
  refreshAll();
};

// Default
showPage("dashboard");
refreshAll();

