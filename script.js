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

  const ICONS = {
    food: `<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 14h16v2H4zm1-3h2l1-6h2l1 6h2l1-7h2l1 7h2v2H5z"/></svg>`,
    snacks: `<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 21h8l1-9H7zm1-11h6l-.6-3H9.6zM11 4h2v2h-2z"/></svg>`,
    drinks: `<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 3h10l-1 18H8zm2.2 2-.7 14h7l-.7-14z"/></svg>`,
    beer: `<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5 6h10v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2zm12 2h2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2z"/></svg>`,
    star: `<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 3 2.4 6.6H21l-5.2 4 2 6.4L12 16.8 6.2 20l2-6.4L3 9.6h6.6z"/></svg>`,
  };

  function money(value) {
    if (value == null) return "";
    const n = Number(value);
    if (Number.isFinite(n)) return n.toFixed(2);
    return String(value);
  }

  function columnsFor(location) {
    return location.columns || data.coreColumns;
  }

  function renderItems(items = []) {
    return `<ul class="item-list">${items
      .map((item) => {
        const mods = [
          item.highlight ? "is-highlight" : "",
          item.accent ? "is-accent" : "",
        ]
          .filter(Boolean)
          .join(" ");
        const note = item.note ? `<div class="item__note">${item.note}</div>` : "";
        const sizes = item.sizes
          ? `<div class="item__sizes">${item.sizes.map((s) => `<span>${s}</span>`).join("")}</div>`
          : "";
        const price =
          item.price != null
            ? `<span class="item__price">${money(item.price)}</span>`
            : `<span class="item__price item__price--empty"></span>`;
        return `<li class="item ${mods}">
          <div class="item__row">
            <span class="item__name">${item.name}</span>
            <span class="item__leader" aria-hidden="true"></span>
            ${price}
          </div>
          ${note}
          ${sizes}
        </li>`;
      })
      .join("")}</ul>`;
  }

  function renderColumn(col) {
    const icon = ICONS[col.icon] || ICONS.star;
    const age = col.ageGate
      ? `<div class="age-row">
          <span class="age-badge">21+</span>
          ${(col.brands || []).map((b) => `<span class="brand-chip">${b}</span>`).join("")}
        </div>`
      : "";
    const logos = col.logos
      ? `<div class="logo-row" aria-hidden="true">${data.sodaLogos
          .map((name) => `<span class="logo-pill">${name}</span>`)
          .join("")}</div>`
      : "";

    return `<section class="menu-col" data-type="${col.id || col.type || ""}">
      <header class="menu-col__head">
        <span class="menu-col__icon">${icon}</span>
        <h3 class="menu-col__title">${col.title}</h3>
      </header>
      ${age}
      ${renderItems(col.items)}
      ${logos}
    </section>`;
  }

  function renderHero(location) {
    const p = data.promo;
    return `<header class="board-hero">
      <div class="board-hero__brand">
        <div class="wolf-mark" aria-hidden="true">LA</div>
        <div>
          <div class="board-hero__athletics">${data.athleticsLine}</div>
          <div class="board-hero__university">${data.universityLine}</div>
          <div class="board-hero__stand">${location.name} · ${location.stand}</div>
        </div>
      </div>

      <div class="board-hero__favorites">
        <span class="value-banner">${p.valueLabel}</span>
        <h1 class="favorites-title">${p.headline}</h1>
        <p class="favorites-tagline">${p.tagline}</p>
      </div>

      <div class="board-hero__offer">
        <div class="offer-badge">
          <span class="offer-badge__four">4</span>
          <span class="offer-badge__for">FOR</span>
          <span class="offer-badge__price">$4</span>
        </div>
        <div class="offer-products">
          ${p.products
            .map(
              (prod) => `<div class="offer-product">
                <div class="offer-product__shot" data-product="${prod.name}"></div>
                <span>${prod.label}</span>
              </div>`
            )
            .join("")}
        </div>
      </div>
    </header>`;
  }

  function renderFooter() {
    const f = data.footer;
    return `<footer class="board-footer">
      <div class="board-footer__cashless">
        <strong>${f.cashless}</strong>
        <span class="contactless" aria-hidden="true"></span>
      </div>
      <div class="board-footer__fuel">
        <strong>${f.fuel}</strong>
      </div>
      <div class="board-footer__pay">
        <strong>${f.pay}</strong>
        <div class="pay-methods">
          ${f.payMethods.map((m) => `<span>${m}</span>`).join("")}
        </div>
      </div>
      <div class="board-footer__thanks">
        <strong>${f.thanks}</strong>
      </div>
    </footer>`;
  }

  function renderBoard(location, { solo = false } = {}) {
    const cols = columnsFor(location);
    const boardClass = solo ? "stadium-board stadium-board--solo" : "stadium-board";
    return `<article class="${boardClass}" data-location="${location.id}">
      ${renderHero(location)}
      <div class="board-cols" style="--cols:${cols.length}">
        ${cols.map(renderColumn).join("")}
      </div>
      ${renderFooter()}
      <p class="board-tax">${data.taxNote}</p>
    </article>`;
  }

  function renderPromoPoster() {
    const p = data.promo;
    return `<article class="promo-board" data-promo="${p.id}">
      <div class="promo-board__hero">
        <p class="promo-kicker">All Season Long</p>
        <h1 class="promo-headline">4 FOR <span>$4</span></h1>
        <p class="promo-sub">${p.headline} · ${p.valueLabel}</p>
      </div>
      <div class="promo-board__menu">
        <div class="promo-bar">
          <strong>${p.headline}</strong>
          <em>${p.valueLabel}</em>
        </div>
        <div class="promo-grid">
          ${p.products
            .map(
              (item) => `<div class="promo-cell">
                <span class="promo-cell__name">${item.label}</span>
                <span class="promo-cell__price">4</span>
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

  fillDeck();
  fillSelect();
  showBoard(data.locations[0].id);
  els.promo.innerHTML = renderPromoPoster();
  setView("board");

  els.tabs.forEach((tab) => {
    tab.addEventListener("click", () => setView(tab.dataset.view));
  });
  els.select.addEventListener("change", () => showBoard(els.select.value));
  els.printBtn.addEventListener("click", () => window.print());
})();
