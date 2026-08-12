(() => {
  const data = window.UNM_MENU;
  if (!data) return;

  const els = {
    deck: document.getElementById("view-deck"),
    board: document.getElementById("view-board"),
    promo: document.getElementById("view-promo"),
    toolbar: document.getElementById("boardToolbar"),
    select: document.getElementById("locationSelect"),
    printBtn: document.getElementById("printBtn"),
    tabs: [...document.querySelectorAll(".tab")],
  };

  function money(value) {
    if (value == null) return "";
    const n = Number(value);
    if (Number.isFinite(n)) return n.toFixed(2);
    return String(value);
  }

  function logoRow(show) {
    if (!show) return "";
    return `<div class="logo-row" aria-hidden="true">${data.sodaLogos
      .map((name) => `<span class="logo-pill">${name}</span>`)
      .join("")}</div>`;
  }

  function renderItems(items = []) {
    return `<ul class="item-list">${items
      .map((item) => {
        const highlight = item.highlight ? " is-highlight" : "";
        const note = item.note ? `<div class="item__note">${item.note}</div>` : "";
        const sizes = item.sizes
          ? `<div class="item__sizes">${item.sizes.map((s) => `<span>${s}</span>`).join("")}</div>`
          : "";
        const price = item.price != null ? `<div class="item__price">${money(item.price)}</div>` : "";
        return `<li class="item${highlight}">
          <div class="item__name">${item.name}</div>
          ${price}
          ${note}
          ${sizes}
        </li>`;
      })
      .join("")}</ul>`;
  }

  function renderColumn(col) {
    const age = col.ageGate
      ? `<div class="age-row">
          <span class="age-badge">21+</span>
          ${(col.brands || []).map((b) => `<span class="brand-chip">${b}</span>`).join("")}
        </div>`
      : "";

    const ribbonClass = col.promo ? "ribbon ribbon--promo" : "ribbon";

    return `<section class="menu-col" data-type="${col.type}">
      <div class="${ribbonClass}">${col.title}</div>
      ${logoRow(col.logos)}
      ${age}
      ${renderItems(col.items)}
    </section>`;
  }

  function renderBoard(location, { solo = false } = {}) {
    const boardClass = solo ? "menu-board menu-board--solo" : "menu-board";
    return `<article class="${boardClass}" data-location="${location.id}">
      <div class="menu-board__top" aria-hidden="true"></div>
      <header class="menu-board__header">
        <div class="menu-board__header-side">${data.season} · ${data.title}</div>
        <div class="menu-board__brand">
          <span class="script">Lobos</span>
          <span class="title">${location.name}</span>
          <span class="stand">${location.tagline} · ${location.stand}</span>
        </div>
        <div class="menu-board__header-side menu-board__header-side--right">${location.stand}</div>
      </header>
      <div class="menu-board__cols">
        ${location.columns.map(renderColumn).join("")}
      </div>
      <footer class="menu-board__footer">
        <span>${data.taxNote}</span>
        ${
          data.cashless
            ? `<span class="cashless">Cashless Facility
                <span class="pay-dots" aria-hidden="true"><span></span><span></span><span></span><span></span></span>
              </span>`
            : ""
        }
      </footer>
    </article>`;
  }

  function renderPromo() {
    const p = data.promo;
    return `<article class="promo-board" data-promo="${p.id}">
      <div class="promo-board__hero">
        <p class="promo-kicker">${p.eyebrow}</p>
        <h1 class="promo-headline">4 FOR <span>$4</span></h1>
        <p class="promo-sub">${p.subhead}</p>
      </div>
      <div class="promo-board__menu">
        <div class="promo-bar">
          <strong>Fan Favorites</strong>
          <em>Value Menu</em>
        </div>
        <div class="promo-grid">
          ${p.items
            .map(
              (item) => `<div class="promo-cell">
                <span class="promo-cell__name">${item.name}</span>
                <span class="promo-cell__price">${item.price}</span>
              </div>`
            )
            .join("")}
        </div>
        <div class="promo-foot">
          <p>${p.tagline}</p>
          <div class="hash">${p.hashtag}</div>
          <div class="note">${p.note}</div>
        </div>
      </div>
    </article>`;
  }

  function fillDeck() {
    els.deck.innerHTML = data.locations
      .map(
        (loc, i) => `<div class="deck-card">
          <div class="deck-card__label">
            <span>Board ${String(i + 1).padStart(2, "0")}</span>
            <span>${loc.name} · ${loc.stand}</span>
          </div>
          ${renderBoard(loc)}
        </div>`
      )
      .join("");
  }

  function fillSelect() {
    els.select.innerHTML = data.locations
      .map((loc) => `<option value="${loc.id}">${loc.name} — ${loc.stand}</option>`)
      .join("");
  }

  function showBoard(id) {
    const loc = data.locations.find((l) => l.id === id) || data.locations[0];
    els.board.innerHTML = renderBoard(loc, { solo: true });
    els.select.value = loc.id;
  }

  function setView(view) {
    els.tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.view === view));
    els.deck.hidden = view !== "deck";
    els.board.hidden = view !== "board";
    els.promo.hidden = view !== "promo";
    els.toolbar.hidden = view !== "board";
  }

  // Init
  fillDeck();
  fillSelect();
  showBoard(data.locations[0].id);
  els.promo.innerHTML = renderPromo();
  setView("deck");

  els.tabs.forEach((tab) => {
    tab.addEventListener("click", () => setView(tab.dataset.view));
  });

  els.select.addEventListener("change", () => showBoard(els.select.value));
  els.printBtn.addEventListener("click", () => window.print());
})();
