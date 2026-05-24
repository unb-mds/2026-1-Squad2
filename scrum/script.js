// ── Leitura segura: o bloco de dados é texto inerte, nunca executado como JS.
// Se o placeholder não foi substituído (ex: template aberto diretamente),
// o dashboard exibe estado vazio sem travar.
const EMPTY_STATE = {
  has_activity: false, repo: "—", generated_at: "—",
  weeks: [], commits: [],
  issues_opened: [], issues_closed: [], issue_volumes: [],
  prs_opened: [], prs_merged: [], prs_rejected: [],
};

let DATA = EMPTY_STATE;
try {
  const raw = document.getElementById("data-payload").textContent.trim();
  if (raw && raw !== "__DATA_PAYLOAD__") {
    DATA = JSON.parse(raw);
  }
} catch (e) {
  console.warn("Falha ao ler dados injetados:", e);
}

// Populate meta
document.getElementById("meta-repo").textContent = DATA.repo || "—";
document.getElementById("meta-time").textContent = DATA.generated_at || "—";

if (!DATA.has_activity) {
  document.getElementById("empty-banner").classList.add("visible");
}

// Shared Chart.js defaults
Chart.defaults.color = "#7c7f9a";
Chart.defaults.borderColor = "#2a2d3a";
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size = 11;

const tooltipDefaults = {
  backgroundColor: "#1a1d27",
  borderColor: "#2a2d3a",
  borderWidth: 1,
  titleColor: "#e2e4ef",
  bodyColor: "#b0b3c8",
  padding: 10,
};

// ── 1. Commits ────────────────────────────────────────────────────────────
new Chart(document.getElementById("chart-commits"), {
  type: "bar",
  data: {
    labels: DATA.weeks,
    datasets: [{
      label: "Commits",
      data: DATA.commits,
      backgroundColor: "rgba(176, 106, 255, 0.65)",
      borderColor: "#b06aff",
      borderWidth: 1,
      borderRadius: 4,
    }],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { ...tooltipDefaults },
    },
    scales: {
      x: { ticks: { maxRotation: 45 } },
      y: { beginAtZero: true, ticks: { stepSize: 1 } },
    },
  },
});

// ── 2. Issues Fluxo ───────────────────────────────────────────────────────
new Chart(document.getElementById("chart-issues"), {
  type: "line",
  data: {
    labels: DATA.weeks,
    datasets: [
      {
        label: "Abertas",
        data: DATA.issues_opened,
        borderColor: "#f0b429",
        backgroundColor: "rgba(240,180,41,0.12)",
        tension: 0.35,
        fill: true,
        pointRadius: 3,
      },
      {
        label: "Fechadas",
        data: DATA.issues_closed,
        borderColor: "#4caf83",
        backgroundColor: "rgba(76,175,131,0.12)",
        tension: 0.35,
        fill: true,
        pointRadius: 3,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: "bottom", labels: { boxWidth: 12 } },
      tooltip: { ...tooltipDefaults, mode: "index", intersect: false },
    },
    scales: {
      x: { ticks: { maxRotation: 45 } },
      y: { beginAtZero: true, ticks: { stepSize: 1 } },
    },
  },
});

// ── 3. Volume por Issue ───────────────────────────────────────────────────
const volData = DATA.issue_volumes || [];
const hasVolumes = volData.length > 0;

new Chart(document.getElementById("chart-volumes"), {
  type: "bar",
  data: {
    labels: hasVolumes
      ? volData.map(i => `#${i.number} ${i.title}`)
      : ["Sem issues no período"],
    datasets: [{
      label: "Caracteres no corpo",
      data: hasVolumes ? volData.map(i => i.body_len) : [0],
      backgroundColor: "rgba(77, 166, 255, 0.65)",
      borderColor: "#4da6ff",
      borderWidth: 1,
      borderRadius: 4,
    }],
  },
  options: {
    indexAxis: "y",
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        ...tooltipDefaults,
        callbacks: {
          label: ctx => ` ${ctx.parsed.x.toLocaleString("pt-BR")} chars`,
        },
      },
    },
    scales: {
      x: { beginAtZero: true },
      y: { ticks: { font: { size: 10 } } },
    },
  },
});

// ── 4. Pull Requests ──────────────────────────────────────────────────────
new Chart(document.getElementById("chart-prs"), {
  type: "bar",
  data: {
    labels: DATA.weeks,
    datasets: [
      {
        label: "Abertas",
        data: DATA.prs_opened,
        backgroundColor: "rgba(240,180,41,0.75)",
        borderRadius: 4,
        stack: "prs",
      },
      {
        label: "Mergeadas",
        data: DATA.prs_merged,
        backgroundColor: "rgba(76,175,131,0.75)",
        borderRadius: 4,
        stack: "prs",
      },
      {
        label: "Rejeitadas",
        data: DATA.prs_rejected,
        backgroundColor: "rgba(224,92,106,0.75)",
        borderRadius: 4,
        stack: "prs",
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: "bottom", labels: { boxWidth: 12 } },
      tooltip: { ...tooltipDefaults, mode: "index", intersect: false },
    },
    scales: {
      x: { ticks: { maxRotation: 45 }, stacked: true },
      y: { beginAtZero: true, stacked: true, ticks: { stepSize: 1 } },
    },
  },
});