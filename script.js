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

  /** White line icons for 4-for-$4 gradient frames */
  const OFFER_ICONS = {
    Pepsi: `<svg class="offer-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M18 8h12l2 4v28a3 3 0 0 1-3 3H19a3 3 0 0 1-3-3V12l2-4z" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M17 16h14M20 8c0 3 8 3 8 0" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="24" cy="28" r="5" stroke="currentColor" stroke-width="2.2"/>
    </svg>`,
    "Lobo Dog": `<svg class="offer-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M8 28c6-8 26-8 32 0" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M10 30c5 6 23 6 28 0" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M14 26c2 3 4 3 6 0M22 24c2 3 4 3 6 0M30 26c2 3 4 3 6 0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
    Popcorn: `<svg class="offer-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M16 20h16l-2 22H18L16 20z" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M18 28h12M17 34h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <circle cx="20" cy="15" r="3.2" stroke="currentColor" stroke-width="2"/>
      <circle cx="28" cy="13" r="3.5" stroke="currentColor" stroke-width="2"/>
      <circle cx="24" cy="18" r="2.8" stroke="currentColor" stroke-width="2"/>
    </svg>`,
    Water: `<svg class="offer-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true">
      <path d="M20 6h8v5l3 3v26a3 3 0 0 1-3 3h-8a3 3 0 0 1-3-3V14l3-3V6z" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
      <path d="M20 6h8M18 20h12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M24 26v10" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    </svg>`,
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
          <div class="board-hero__stand">Page ${location.page || "—"} · ${location.name} · ${location.stand}</div>
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
            .map((prod) => {
              const icon = OFFER_ICONS[prod.name] || "";
              return `<div class="offer-product">
                <div class="offer-product__shot" data-product="${prod.name}">
                  ${icon}
                </div>
                <span>${prod.label}</span>
              </div>`;
            })
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

  function renderBoard(location, { solo = false, showMeta = false } = {}) {
    const cols = columnsFor(location);
    const print = location.print || {};
    const sizeClass = print.className || "";
    const orientClass = print.orientation === "portrait" ? "is-portrait" : "is-landscape";
    const compactClass = print.widthIn && print.widthIn <= 24 ? "is-compact" : "";
    const boardClass = [
      "stadium-board",
      solo ? "stadium-board--solo" : "",
      sizeClass,
      orientClass,
      compactClass,
    ]
      .filter(Boolean)
      .join(" ");

    const meta = showMeta
      ? `<div class="print-meta">
          <span>Sheet #${location.page}</span>
          <span>${location.placement || "—"}</span>
          <span>${print.label || "Size TBD"}</span>
        </div>`
      : "";

    return `${meta}<article class="${boardClass}" data-location="${location.id}" data-print="${location.printKey || ""}">
      ${renderHero(location)}
      <div class="board-cols" style="--cols:${cols.length}">
        ${cols.map(renderColumn).join("")}
      </div>
      ${renderFooter()}
      <p class="board-tax">${data.taxNote}${print.label ? ` · Print: ${print.label}` : ""}</p>
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
        (loc) => `<div class="deck-card">
          <div class="deck-card__label">
            <span>#${String(loc.page).padStart(2, "0")} · ${loc.placement || ""}</span>
            <span>${loc.name} · ${loc.stand} · ${loc.print?.label || ""}</span>
          </div>
          ${renderBoard(loc, { showMeta: false })}
        </div>`
      )
      .join("");
  }

  function fillSelect() {
    els.select.innerHTML = data.locations
      .map((loc) => {
        const size = loc.print?.label || "";
        return `<option value="${loc.id}">#${loc.page} — ${loc.name} — ${loc.stand} — ${size}</option>`;
      })
      .join("");
  }

  function showBoard(id) {
    const loc = data.locations.find((l) => l.id === id) || data.locations[0];
    els.board.innerHTML = renderBoard(loc, { solo: true, showMeta: true });
    els.select.value = loc.id;
  }

  function setView(view) {
    els.tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.view === view));
    els.deck.hidden = view !== "deck";
    els.board.hidden = view !== "board";
    els.promo.hidden = view !== "promo";
    els.toolbar.hidden = view !== "board";
  }

  function ensurePrintStyleEl() {
    let el = document.getElementById("printPageStyle");
    if (!el) {
      el = document.createElement("style");
      el.id = "printPageStyle";
      document.head.appendChild(el);
    }
    return el;
  }

  /** Set @page to Fireup inches for the active board (or letter for deck/promo). */
  function applyPrintPageSize(location) {
    const el = ensurePrintStyleEl();
    if (!location?.print) {
      el.textContent = `@media print { @page { size: letter landscape; margin: 0.25in; } }`;
      document.documentElement.dataset.printSize = "letter-landscape";
      return;
    }
    const { widthIn, heightIn, orientation, label } = location.print;
    const sizeValue =
      orientation === "portrait" ? `${widthIn}in ${heightIn}in` : `${widthIn}in ${heightIn}in`;
    el.textContent = `
@media print {
  @page {
    size: ${sizeValue};
    margin: 0;
  }
}
`.trim();
    document.documentElement.dataset.printSize = label || `${widthIn}x${heightIn}`;
  }

  function printCurrentView() {
    const activeTab = els.tabs.find((t) => t.classList.contains("is-active"));
    const view = activeTab?.dataset.view || "board";

    if (view === "board") {
      const loc =
        data.locations.find((l) => l.id === els.select.value) || data.locations[0];
      applyPrintPageSize(loc);
      // Brief beat so the style tag is in the DOM before the print dialog
      requestAnimationFrame(() => window.print());
      return;
    }

    if (view === "deck") {
      // Deck uses one shared page size (largest common landscape proof).
      // For final production, print Single Board one location at a time.
      applyPrintPageSize({
        print: {
          widthIn: 96,
          heightIn: 36,
          orientation: "landscape",
          label: "96 in × 36 in Landscape (deck proof)",
        },
      });
      requestAnimationFrame(() => window.print());
      return;
    }

    // Promo poster — tabloid-friendly proof
    ensurePrintStyleEl().textContent = `
@media print {
  @page { size: tabloid portrait; margin: 0.4in; }
}
`.trim();
    document.documentElement.dataset.printSize = "tabloid-portrait";
    requestAnimationFrame(() => window.print());
  }

  fillDeck();
  fillSelect();
  showBoard(data.locations[0].id);
  applyPrintPageSize(data.locations[0]);
  els.promo.innerHTML = renderPromoPoster();
  setView("board");

  els.tabs.forEach((tab) => {
    tab.addEventListener("click", () => setView(tab.dataset.view));
  });
  els.select.addEventListener("change", () => {
    showBoard(els.select.value);
    const loc = data.locations.find((l) => l.id === els.select.value);
    applyPrintPageSize(loc);
  });
  els.printBtn.addEventListener("click", printCurrentView);
})();
