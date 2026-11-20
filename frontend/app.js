const FILE_NAMES = {
  global: "全局参数.csv",
  demand: "需求分布.csv",
  supply: "供应城市.csv",
  distance: "距离数据.csv"
};

const TABLE_META = {
  global: { title: "全局参数", description: "设置模型成本、仓库数量、库存与时效约束", columns: ["名称", "单位", "数量"] },
  demand: { title: "需求分布", description: "维护各服务城市及其需求数量", columns: ["城市", "需求量"] },
  supply: { title: "候选仓库", description: "维护可用于建设仓库的候选城市", columns: ["城市"] },
  distance: { title: "距离数据", description: "维护需求城市到候选仓库之间的距离和运输时间", columns: ["城市1", "城市2", "距离（公里）", "时间（小时）"] }
};

const defaultApiUrl = window.location.hostname && !["127.0.0.1", "localhost"].includes(window.location.hostname)
  ? `${window.location.protocol}//${window.location.hostname}`
  : "http://127.0.0.1:8000";

const state = {
  data: { global: [], demand: [], supply: [], distance: [] },
  currentTable: "global",
  resultTable: "warehouse",
  results: null,
  apiUrl: localStorage.getItem("warehouse-api-url") || defaultApiUrl
};

const elements = {};

document.addEventListener("DOMContentLoaded", async () => {
  cacheElements();
  bindEvents();
  routeFromHash();
  await loadSampleData();
  renderAllDataViews();
  elements.apiUrlInput.value = state.apiUrl;
  window.setTimeout(checkApiConnection, 500);
});

function cacheElements() {
  [
    "sidebar", "menuButton", "connectionButton", "connectionTitle", "connectionSubtitle", "statusDot",
    "resetButton", "runTopButton", "heroRunButton", "workflowRunButton", "runDataButton", "emptyRunButton",
    "rerunButton", "uploadAllButton", "batchFileInput", "uploadTableButton", "tableFileInput", "addRowButton",
    "tableSearch", "editorTable", "tableTitle", "tableDescription", "tableCount", "dataSummary",
    "supplyCount", "demandCount", "routeCount", "totalDemand", "globalRows", "demandRows", "supplyRows", "distanceRows",
    "apiModal", "closeApiModal", "apiUrlInput", "testApiButton", "saveApiButton", "apiMessage",
    "runOverlay", "runStatus", "runProgress", "emptyResults", "resultsContent", "resultSubtitle", "resultMetrics",
    "totalCostLabel", "costDonut", "costLegend", "warehouseCount", "warehouseChart", "resultTable", "exportButton", "toastRegion"
  ].forEach((id) => { elements[id] = document.getElementById(id); });
}

function bindEvents() {
  window.addEventListener("hashchange", routeFromHash);
  document.querySelectorAll("[data-goto]").forEach((button) => button.addEventListener("click", () => navigate(button.dataset.goto)));
  document.querySelectorAll(".data-tab").forEach((button) => button.addEventListener("click", () => selectDataTable(button.dataset.table)));
  document.querySelectorAll("[data-result-table]").forEach((button) => button.addEventListener("click", () => selectResultTable(button.dataset.resultTable)));
  [elements.runTopButton, elements.heroRunButton, elements.workflowRunButton, elements.runDataButton, elements.emptyRunButton, elements.rerunButton].forEach((button) => button.addEventListener("click", runOptimization));
  elements.menuButton.addEventListener("click", () => elements.sidebar.classList.toggle("open"));
  elements.connectionButton.addEventListener("click", openApiModal);
  elements.closeApiModal.addEventListener("click", closeApiModal);
  elements.apiModal.addEventListener("click", (event) => { if (event.target === elements.apiModal) closeApiModal(); });
  elements.testApiButton.addEventListener("click", checkApiConnection);
  elements.saveApiButton.addEventListener("click", saveApiUrl);
  elements.resetButton.addEventListener("click", resetSampleData);
  elements.uploadAllButton.addEventListener("click", () => elements.batchFileInput.click());
  elements.batchFileInput.addEventListener("change", handleBatchUpload);
  elements.uploadTableButton.addEventListener("click", () => elements.tableFileInput.click());
  elements.tableFileInput.addEventListener("change", handleSingleUpload);
  elements.addRowButton.addEventListener("click", addRow);
  elements.tableSearch.addEventListener("input", renderEditorTable);
  elements.editorTable.addEventListener("input", handleCellEdit);
  elements.editorTable.addEventListener("click", handleTableClick);
  elements.exportButton.addEventListener("click", exportResults);
}

function routeFromHash() {
  const sectionId = location.hash.replace("#", "") || "overview";
  const section = document.getElementById(sectionId) || document.getElementById("overview");
  document.querySelectorAll(".page-section").forEach((item) => item.classList.toggle("active", item === section));
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.section === section.id));
  elements.sidebar?.classList.remove("open");
  window.scrollTo({ top: 0, behavior: "instant" });
}

function navigate(section) {
  if (location.hash === `#${section}`) routeFromHash();
  else location.hash = section;
}

async function loadSampleData() {
  const entries = Object.entries(FILE_NAMES);
  const loaded = await Promise.all(entries.map(async ([key, fileName]) => {
    const response = await fetch(`data/${encodeURIComponent(fileName)}`);
    if (!response.ok) throw new Error(`无法读取 ${fileName}`);
    return [key, parseCSV(await response.text())];
  }));
  state.data = Object.fromEntries(loaded);
}

async function resetSampleData() {
  try {
    await loadSampleData();
    state.results = null;
    renderAllDataViews();
    showEmptyResults();
    toast("示例数据已恢复", "success");
  } catch (error) {
    toast(error.message, "error");
  }
}

function parseCSV(text) {
  const rows = [];
  let row = [], field = "", inQuotes = false;
  const source = text.replace(/^\uFEFF/, "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  for (let index = 0; index < source.length; index += 1) {
    const char = source[index];
    if (char === '"' && inQuotes && source[index + 1] === '"') { field += '"'; index += 1; }
    else if (char === '"') inQuotes = !inQuotes;
    else if (char === "," && !inQuotes) { row.push(field.trim()); field = ""; }
    else if (char === "\n" && !inQuotes) { row.push(field.trim()); if (row.some(Boolean)) rows.push(row); row = []; field = ""; }
    else field += char;
  }
  if (field || row.length) { row.push(field.trim()); if (row.some(Boolean)) rows.push(row); }
  if (!rows.length) return [];
  const headers = rows.shift();
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, coerceValue(values[index] ?? "")])));
}

function coerceValue(value) {
  if (typeof value !== "string" || value.trim() === "") return value;
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : value;
}

function toCSV(rows) {
  if (!rows?.length) return "";
  const columns = [...new Set(rows.flatMap(Object.keys))];
  const escape = (value) => {
    const text = String(value ?? "");
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  };
  return [columns.join(","), ...rows.map((row) => columns.map((column) => escape(row[column])).join(","))].join("\n");
}

function renderAllDataViews() {
  renderScenarioMetrics();
  renderDataSummary();
  renderEditorTable();
}

function renderScenarioMetrics() {
  const totalDemand = state.data.demand.reduce((sum, row) => sum + numberValue(row["需求量"]), 0);
  elements.supplyCount.textContent = formatNumber(state.data.supply.length, 0);
  elements.demandCount.textContent = formatNumber(state.data.demand.length, 0);
  elements.routeCount.textContent = formatNumber(state.data.distance.length, 0);
  elements.totalDemand.textContent = formatNumber(totalDemand, totalDemand >= 100 ? 0 : 3);
  elements.globalRows.textContent = state.data.global.length;
  elements.demandRows.textContent = state.data.demand.length;
  elements.supplyRows.textContent = state.data.supply.length;
  elements.distanceRows.textContent = state.data.distance.length;
}

function renderDataSummary() {
  const validPaths = state.data.distance.filter((row) => numberValue(row["距离（公里）"]) >= 0 && numberValue(row["时间（小时）"]) >= 0).length;
  elements.dataSummary.innerHTML = `
    <span class="summary-pill"><i></i> ${state.data.global.length} 项参数已配置</span>
    <span class="summary-pill"><i></i> ${state.data.demand.length} 个需求城市</span>
    <span class="summary-pill"><i></i> ${state.data.supply.length} 个候选仓库</span>
    <span class="summary-pill"><i></i> ${validPaths} 条有效路径</span>`;
}

function selectDataTable(key) {
  state.currentTable = key;
  elements.tableSearch.value = "";
  document.querySelectorAll(".data-tab").forEach((button) => button.classList.toggle("active", button.dataset.table === key));
  renderEditorTable();
}

function renderEditorTable() {
  const meta = TABLE_META[state.currentTable];
  const query = elements.tableSearch.value.trim().toLowerCase();
  const rows = state.data[state.currentTable].map((row, index) => ({ row, index })).filter(({ row }) => !query || Object.values(row).some((value) => String(value).toLowerCase().includes(query)));
  elements.tableTitle.textContent = meta.title;
  elements.tableDescription.textContent = meta.description;
  elements.editorTable.innerHTML = `
    <thead><tr><th class="row-number">#</th>${meta.columns.map((column) => `<th>${escapeHTML(column)}</th>`).join("")}<th></th></tr></thead>
    <tbody>${rows.map(({ row, index }) => `<tr data-index="${index}"><td class="row-number">${index + 1}</td>${meta.columns.map((column) => `<td contenteditable="true" data-column="${escapeHTML(column)}">${escapeHTML(row[column] ?? "")}</td>`).join("")}<td><button class="delete-row" data-delete="${index}" aria-label="删除此行">×</button></td></tr>`).join("")}</tbody>`;
  elements.tableCount.textContent = `共 ${rows.length} 条数据${query ? `（筛选自 ${state.data[state.currentTable].length} 条）` : ""}`;
}

function handleCellEdit(event) {
  const cell = event.target.closest("[data-column]");
  const rowElement = event.target.closest("tr[data-index]");
  if (!cell || !rowElement) return;
  state.data[state.currentTable][Number(rowElement.dataset.index)][cell.dataset.column] = coerceValue(cell.textContent.trim());
  renderScenarioMetrics();
  renderDataSummary();
}

function handleTableClick(event) {
  const button = event.target.closest("[data-delete]");
  if (!button) return;
  state.data[state.currentTable].splice(Number(button.dataset.delete), 1);
  renderAllDataViews();
}

function addRow() {
  state.data[state.currentTable].push(Object.fromEntries(TABLE_META[state.currentTable].columns.map((column) => [column, ""])));
  renderAllDataViews();
  const tableWrap = elements.editorTable.parentElement;
  tableWrap.scrollTop = tableWrap.scrollHeight;
}

async function handleSingleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const rows = parseCSV(await file.text());
  if (!validateColumns(state.currentTable, rows)) return;
  state.data[state.currentTable] = rows;
  renderAllDataViews();
  event.target.value = "";
  toast(`${file.name} 已载入`, "success");
}

async function handleBatchUpload(event) {
  let loaded = 0;
  for (const file of event.target.files) {
    const key = Object.keys(FILE_NAMES).find((candidate) => FILE_NAMES[candidate] === file.name);
    if (!key) continue;
    const rows = parseCSV(await file.text());
    if (validateColumns(key, rows, false)) { state.data[key] = rows; loaded += 1; }
  }
  renderAllDataViews();
  event.target.value = "";
  toast(loaded ? `已载入 ${loaded} 个数据文件` : "未找到匹配的 CSV 文件名", loaded ? "success" : "error");
}

function validateColumns(key, rows, notify = true) {
  const columns = rows.length ? Object.keys(rows[0]) : [];
  const missing = TABLE_META[key].columns.filter((column) => !columns.includes(column));
  if (missing.length && notify) toast(`缺少字段：${missing.join("、")}`, "error");
  return missing.length === 0;
}

function validateScenario() {
  const errors = [];
  Object.keys(TABLE_META).forEach((key) => {
    if (!state.data[key].length) errors.push(`${TABLE_META[key].title}不能为空`);
    else if (!validateColumns(key, state.data[key], false)) errors.push(`${TABLE_META[key].title}字段不完整`);
  });
  if (!state.data.demand.every((row) => numberValue(row["需求量"]) >= 0)) errors.push("需求量必须为非负数");
  return errors;
}

function openApiModal() {
  elements.apiUrlInput.value = state.apiUrl;
  elements.apiMessage.textContent = "";
  elements.apiModal.hidden = false;
}

function closeApiModal() { elements.apiModal.hidden = true; }

function saveApiUrl() {
  const value = elements.apiUrlInput.value.trim().replace(/\/$/, "");
  if (!/^https?:\/\//i.test(value)) {
    setApiMessage("请输入以 http:// 或 https:// 开头的地址", "error");
    return;
  }
  state.apiUrl = value;
  localStorage.setItem("warehouse-api-url", value);
  setApiMessage("地址已保存", "success");
  checkApiConnection();
  window.setTimeout(closeApiModal, 650);
}

async function checkApiConnection() {
  const candidate = elements.apiUrlInput?.value.trim().replace(/\/$/, "") || state.apiUrl;
  setConnectionState(false, "正在检测...", candidate.replace(/^https?:\/\//, ""));
  try {
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 3500);
    const response = await fetch(`${candidate}/docs`, { method: "GET", signal: controller.signal });
    window.clearTimeout(timer);
    if (!response.ok) throw new Error("服务未响应");
    setConnectionState(true, "API 已连接", candidate.replace(/^https?:\/\//, ""));
    setApiMessage("连接成功，可以运行优化", "success");
    return true;
  } catch (_) {
    setConnectionState(false, "API 未连接", "点击配置服务地址");
    setApiMessage("暂时无法连接，请检查地址、服务状态和 CORS 配置", "error");
    return false;
  }
}

function setConnectionState(online, title, subtitle) {
  elements.statusDot.classList.toggle("online", online);
  elements.connectionTitle.textContent = title;
  elements.connectionSubtitle.textContent = subtitle;
}

function setApiMessage(message, type = "") {
  elements.apiMessage.textContent = message;
  elements.apiMessage.className = `modal-message ${type}`;
}

async function runOptimization() {
  const errors = validateScenario();
  if (errors.length) { toast(errors[0], "error"); navigate("data"); return; }
  elements.runOverlay.hidden = false;
  updateRunProgress(18, "正在校验场景数据...");
  const progressTimer = window.setTimeout(() => updateRunProgress(52, "正在构建仓网优化模型..."), 500);
  const solveTimer = window.setTimeout(() => updateRunProgress(76, "求解器正在搜索更优方案..."), 1400);
  try {
    const payload = { files: Object.fromEntries(Object.entries(FILE_NAMES).map(([key, fileName]) => [fileName, state.data[key]])) };
    const response = await fetch(`${state.apiUrl}/api/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(`服务返回 ${response.status}`);
    const result = await response.json();
    if (!result.success) throw new Error(result.error || "求解失败");
    updateRunProgress(100, "方案已生成，正在整理结果...");
    state.results = normalizeResults(result.results);
    window.setTimeout(() => {
      elements.runOverlay.hidden = true;
      renderResults(result.runtime);
      navigate("results");
      toast(`优化完成，用时 ${result.runtime} 秒`, "success");
    }, 450);
  } catch (error) {
    elements.runOverlay.hidden = true;
    toast(`无法完成优化：${error.message}`, "error");
    if (error instanceof TypeError) openApiModal();
  } finally {
    window.clearTimeout(progressTimer);
    window.clearTimeout(solveTimer);
  }
}

function updateRunProgress(percent, message) {
  elements.runProgress.style.width = `${percent}%`;
  elements.runStatus.textContent = message;
}

function normalizeResults(results) {
  const find = (fragment) => {
    const key = Object.keys(results).find((name) => name.includes(fragment));
    const value = key ? results[key] : [];
    if (Array.isArray(value)) return value;
    if (value && typeof value === "object") {
      const keys = Object.keys(value);
      if (keys.length && keys.every((item) => Array.isArray(value[item]))) {
        const length = Math.max(...keys.map((item) => value[item].length));
        return Array.from({ length }, (_, index) => Object.fromEntries(keys.map((item) => [item, value[item][index]])));
      }
    }
    return [];
  };
  return { warehouse: find("构建仓库"), demand: find("需求城市"), kpi: find("指标") };
}

function renderResults(runtime) {
  elements.emptyResults.hidden = true;
  elements.resultsContent.hidden = false;
  elements.exportButton.disabled = false;
  elements.resultSubtitle.textContent = `模型已完成求解 · 运行时间 ${runtime} 秒 · ${new Date().toLocaleString("zh-CN", { hour12: false })}`;
  const kpis = Object.fromEntries(state.results.kpi.map((row) => [row["指标名称"], row["指标值"]]));
  const metricConfig = [
    ["总成本", "总成本", "violet", "¥"],
    ["需求覆盖率", "需求覆盖率", "green", ""],
    ["总需求量", "总需求量", "blue", ""],
    ["推荐仓库", "仓库数量", "amber", ""]
  ];
  elements.resultMetrics.innerHTML = metricConfig.map(([label, key, color, prefix]) => {
    const value = key === "仓库数量" ? state.results.warehouse.length : kpis[key];
    return `<article class="metric-card"><span class="metric-icon ${color}">${metricIcon(key)}</span><small>${label}</small><strong>${prefix}${formatMetricValue(value)}</strong></article>`;
  }).join("");
  renderCostChart(kpis);
  renderWarehouseChart();
  selectResultTable(state.resultTable);
}

function renderCostChart(kpis) {
  const config = [
    { name: "运输成本", color: "#6657d9" },
    { name: "仓储成本", color: "#4b8fe8" },
    { name: "缺货成本", color: "#e8795d" },
    { name: "资金占用成本", color: "#43a581" }
  ];
  const values = config.map((item) => numberValue(kpis[item.name]));
  const total = values.reduce((sum, value) => sum + value, 0) || 1;
  let cursor = 0;
  const segments = config.map((item, index) => {
    const start = cursor;
    cursor += values[index] / total * 100;
    return `${item.color} ${start}% ${cursor}%`;
  });
  elements.costDonut.style.background = `conic-gradient(${segments.join(",")})`;
  elements.costDonut.querySelector("span").textContent = `¥${compactNumber(total)}`;
  elements.totalCostLabel.textContent = `总计 ¥${formatNumber(total, 2)}`;
  elements.costLegend.innerHTML = config.map((item, index) => `<div><i style="background:${item.color}"></i><span>${item.name}</span><strong>${(values[index] / total * 100).toFixed(1)}%</strong></div>`).join("");
}

function renderWarehouseChart() {
  const rows = state.results.warehouse;
  const max = Math.max(...rows.map((row) => numberValue(row["库存水平"])), 1);
  elements.warehouseCount.textContent = rows.length;
  elements.warehouseChart.innerHTML = rows.map((row) => {
    const value = numberValue(row["库存水平"]);
    return `<div class="bar-item" title="${escapeHTML(row["城市"])}：${value}"><strong>${formatNumber(value, 2)}</strong><i style="height:${Math.max(value / max * 78, 3)}%"></i><span>${escapeHTML(row["城市"])}</span></div>`;
  }).join("") || '<div class="empty-table">没有推荐仓库</div>';
}

function selectResultTable(key) {
  state.resultTable = key;
  document.querySelectorAll("[data-result-table]").forEach((button) => button.classList.toggle("active", button.dataset.resultTable === key));
  if (!state.results) return;
  const rows = state.results[key];
  const columns = rows.length ? Object.keys(rows[0]) : [];
  elements.resultTable.innerHTML = `<thead><tr>${columns.map((column) => `<th>${escapeHTML(column)}</th>`).join("")}</tr></thead><tbody>${rows.map((row) => `<tr>${columns.map((column) => `<td>${escapeHTML(row[column] ?? "")}</td>`).join("")}</tr>`).join("")}</tbody>`;
}

function showEmptyResults() {
  elements.emptyResults.hidden = false;
  elements.resultsContent.hidden = true;
  elements.exportButton.disabled = true;
  elements.resultSubtitle.textContent = "运行模型后，这里将展示推荐方案与成本分析。";
}

function exportResults() {
  if (!state.results) return;
  Object.entries({ "构建仓库的城市输出.csv": state.results.warehouse, "需求城市满足情况输出.csv": state.results.demand, "指标输出.csv": state.results.kpi }).forEach(([name, rows], index) => {
    window.setTimeout(() => downloadFile(name, `\uFEFF${toCSV(rows)}`), index * 180);
  });
  toast("结果文件已开始下载", "success");
}

function downloadFile(name, content) {
  const blob = new Blob([content], { type: "text/csv;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = name;
  link.click();
  URL.revokeObjectURL(link.href);
}

function metricIcon(name) {
  const icons = {
    "总成本": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 9h8M8 13h8M12 9v8"/></svg>',
    "需求覆盖率": '<svg viewBox="0 0 24 24"><path d="m4 12 5 5L20 6"/></svg>',
    "总需求量": '<svg viewBox="0 0 24 24"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
    "仓库数量": '<svg viewBox="0 0 24 24"><path d="M4 21V9l8-5 8 5v12M8 21v-6h8v6"/></svg>'
  };
  return icons[name] || icons["总成本"];
}

function formatMetricValue(value) {
  if (typeof value === "string" && value.includes("%")) return value;
  return formatNumber(numberValue(value), 2);
}

function numberValue(value) {
  const numeric = Number(String(value ?? 0).replace(/[%,$¥\s]/g, ""));
  return Number.isFinite(numeric) ? numeric : 0;
}

function formatNumber(value, maximumFractionDigits = 2) {
  return new Intl.NumberFormat("zh-CN", { maximumFractionDigits }).format(Number(value) || 0);
}

function compactNumber(value) {
  return new Intl.NumberFormat("zh-CN", { notation: "compact", maximumFractionDigits: 1 }).format(Number(value) || 0);
}

function escapeHTML(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function toast(message, type = "") {
  const item = document.createElement("div");
  item.className = `toast ${type}`;
  item.textContent = message;
  elements.toastRegion.appendChild(item);
  window.setTimeout(() => item.remove(), 4200);
}
