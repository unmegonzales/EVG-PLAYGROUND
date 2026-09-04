// Visitor File Submissions — client-side interactions.
// Handles file selection (browse + drag/drop), packet completion tracking,
// submission receipts, and a locally persisted receipt history.

const form = document.getElementById("submissionForm");
const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");
const browseButton = document.getElementById("browseButton");
const fileList = document.getElementById("fileList");
const receipt = document.getElementById("receipt");
const completionValue = document.getElementById("completionValue");
const completionBar = document.getElementById("completionBar");
const historyList = document.getElementById("historyList");
const clearHistoryButton = document.getElementById("clearHistory");
const fileTemplate = document.getElementById("fileTemplate");

const MAX_FILE_BYTES = 25 * 1024 * 1024;
const HISTORY_KEY = "visitor-submissions:history";
const REQUIRED_FIELDS = ["name", "organization", "email", "team", "category"];

let selectedFiles = [];

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const exponent = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1024)),
    units.length - 1
  );
  const value = bytes / Math.pow(1024, exponent);
  return `${value.toFixed(value >= 10 || exponent === 0 ? 0 : 1)} ${units[exponent]}`;
}

function fileKey(file) {
  return `${file.name}:${file.size}:${file.lastModified}`;
}

function addFiles(fileCollection) {
  const incoming = Array.from(fileCollection);
  let rejected = 0;

  for (const file of incoming) {
    if (file.size > MAX_FILE_BYTES) {
      rejected += 1;
      continue;
    }
    const exists = selectedFiles.some((existing) => fileKey(existing) === fileKey(file));
    if (!exists) {
      selectedFiles.push(file);
    }
  }

  if (rejected > 0) {
    dropZone.classList.add("error");
    setTimeout(() => dropZone.classList.remove("error"), 1600);
  }

  renderFiles();
  updateCompletion();
}

function removeFile(key) {
  selectedFiles = selectedFiles.filter((file) => fileKey(file) !== key);
  renderFiles();
  updateCompletion();
}

function renderFiles() {
  fileList.innerHTML = "";

  for (const file of selectedFiles) {
    const node = fileTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector("strong").textContent = file.name;
    node.querySelector("span").textContent = formatBytes(file.size);
    node.querySelector("button").addEventListener("click", () => removeFile(fileKey(file)));
    fileList.appendChild(node);
  }
}

function completionItems() {
  const data = new FormData(form);
  const items = [];

  for (const field of REQUIRED_FIELDS) {
    items.push(Boolean(String(data.get(field) || "").trim()));
  }
  items.push(selectedFiles.length > 0);
  items.push(form.elements.consent.checked);

  return items;
}

function updateCompletion() {
  const items = completionItems();
  const done = items.filter(Boolean).length;
  const percent = Math.round((done / items.length) * 100);

  completionValue.textContent = `${percent}%`;
  completionBar.style.width = `${percent}%`;
}

function generateReceiptNumber() {
  const stamp = Date.now().toString(36).toUpperCase().slice(-5);
  const suffix = Math.floor(Math.random() * 900 + 100);
  return `VS-${stamp}-${suffix}`;
}

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (error) {
    return [];
  }
}

function saveHistory(entries) {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(entries));
  } catch (error) {
    /* storage may be unavailable; history stays in-memory only */
  }
}

function renderHistory() {
  const entries = loadHistory();
  historyList.innerHTML = "";

  if (entries.length === 0) {
    const empty = document.createElement("p");
    empty.className = "history-card";
    empty.textContent = "No receipts yet.";
    historyList.appendChild(empty);
    return;
  }

  for (const entry of entries) {
    const card = document.createElement("div");
    card.className = "history-card";

    const title = document.createElement("strong");
    title.textContent = `${entry.receipt} · ${entry.team}`;

    const detail = document.createElement("span");
    detail.textContent = `${entry.name} — ${entry.fileCount} file${entry.fileCount === 1 ? "" : "s"} · ${entry.timestamp}`;

    card.append(title, detail);
    historyList.appendChild(card);
  }
}

function markFieldErrors() {
  const data = new FormData(form);
  let firstInvalid = null;

  for (const field of REQUIRED_FIELDS) {
    const element = form.elements[field];
    const valid = Boolean(String(data.get(field) || "").trim());
    element.classList.toggle("error", !valid);
    if (!valid && !firstInvalid) firstInvalid = element;
  }

  if (firstInvalid) firstInvalid.focus();
  return firstInvalid === null;
}

function showReceipt(entry) {
  receipt.classList.add("is-complete");
  receipt.innerHTML = "";

  const number = document.createElement("span");
  number.className = "receipt__number";
  number.textContent = entry.receipt;

  const heading = document.createElement("h2");
  heading.textContent = "Packet received";

  const detail = document.createElement("p");
  detail.textContent = `Routed to ${entry.team} · ${entry.fileCount} file${entry.fileCount === 1 ? "" : "s"} attached. Keep ${entry.receipt} for your records.`;

  receipt.append(number, heading, detail);
}

form.addEventListener("input", updateCompletion);
form.addEventListener("change", updateCompletion);

browseButton.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (event) => {
  addFiles(event.target.files);
  fileInput.value = "";
});

["dragenter", "dragover"].forEach((type) => {
  dropZone.addEventListener(type, (event) => {
    event.preventDefault();
    dropZone.classList.add("is-dragging");
  });
});

["dragleave", "dragend", "drop"].forEach((type) => {
  dropZone.addEventListener(type, (event) => {
    event.preventDefault();
    dropZone.classList.remove("is-dragging");
  });
});

dropZone.addEventListener("drop", (event) => {
  if (event.dataTransfer && event.dataTransfer.files) {
    addFiles(event.dataTransfer.files);
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const fieldsValid = markFieldErrors();
  const hasFiles = selectedFiles.length > 0;
  const consented = form.elements.consent.checked;

  if (!fieldsValid || !hasFiles || !consented) {
    if (!hasFiles) {
      dropZone.classList.add("error");
      setTimeout(() => dropZone.classList.remove("error"), 1600);
    }
    return;
  }

  const data = new FormData(form);
  const entry = {
    receipt: generateReceiptNumber(),
    name: String(data.get("name")).trim(),
    team: String(data.get("team")).trim(),
    fileCount: selectedFiles.length,
    timestamp: new Date().toLocaleString(),
  };

  const entries = loadHistory();
  entries.unshift(entry);
  saveHistory(entries.slice(0, 8));

  showReceipt(entry);
  renderHistory();

  form.reset();
  selectedFiles = [];
  renderFiles();
  updateCompletion();
});

form.addEventListener("reset", () => {
  selectedFiles = [];
  setTimeout(() => {
    renderFiles();
    updateCompletion();
    REQUIRED_FIELDS.forEach((field) => form.elements[field].classList.remove("error"));
  }, 0);
});

clearHistoryButton.addEventListener("click", () => {
  saveHistory([]);
  renderHistory();
});

renderFiles();
renderHistory();
updateCompletion();
