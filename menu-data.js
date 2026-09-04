/* UNM Lobos 25/26 Football Concessions — menu data
   Print sizes from: Football Menu Printing Dimensions - Fireup.pdf
   Content updates from: LOBO Football Menu Graphic Designer Change Sheet
   Prices display WITHOUT dollar signs.
*/

window.UNM_MENU = {
  season: "25/26",
  title: "Lobo Football Menu",
  athleticsLine: "Lobos Athletics",
  universityLine: "University of New Mexico",
  taxNote: "All prices subject to applicable sales tax.",
  cashless: true,
  changeSheet: "LOBO Football Menu Graphic Designer Change Sheet",
  printSpecDoc: "Football Menu Printing Dimensions - Fireup.pdf",
  brand: {
    cherry: "#BA0C2F",
    silver: "#A7A8AA",
    metal: "#4A4F55",
    turquoise: "#00A8B5",
    white: "#FFFFFF",
    light: "#F4F4F6",
  },

  sodaLogos: ["Pepsi", "Mt Dew", "Dr Pepper", "Starry", "Dasani"],

  /** Named print presets (inches) → CSS aspect + orientation */
  printPresets: {
    "96x36-landscape": {
      label: "96 in × 36 in Landscape",
      widthIn: 96,
      heightIn: 36,
      orientation: "landscape",
      ratio: "8 / 3",
      className: "size-96x36",
    },
    "192x48-landscape": {
      label: "192 in × 48 in Landscape (frame 196 × 48)",
      widthIn: 192,
      heightIn: 48,
      frameWidthIn: 196,
      frameHeightIn: 48,
      orientation: "landscape",
      ratio: "4 / 1",
      className: "size-192x48",
    },
    "24x36-portrait": {
      label: "24 in × 36 in Portrait",
      widthIn: 24,
      heightIn: 36,
      orientation: "portrait",
      ratio: "2 / 3",
      className: "size-24x36",
    },
    "12x18-portrait": {
      label: "12 in × 18 in Portrait",
      widthIn: 12,
      heightIn: 18,
      orientation: "portrait",
      ratio: "2 / 3",
      className: "size-12x18",
    },
  },

  promo: {
    id: "four-for-four",
    valueLabel: "Value Menu",
    headline: "Fan Favorites",
    tagline: "Great Game. Great Food. Go Lobos.",
    offer: "4 for $4",
    products: [
      { name: "Pepsi", label: "16 oz Pepsi" },
      { name: "Lobo Dog", label: "Lobo Dog" },
      { name: "Popcorn", label: "Popcorn" },
      { name: "Water", label: "Water" },
    ],
    hashtag: "#GOLOBOS",
    note: "Available at main west, northwest & northeast concession areas.",
  },

  footer: {
    cashless: "Cashless Facility",
    fuel: "We Fuel Champions",
    pay: "Pay Your Way",
    thanks: "Thank you for supporting Lobo Athletics!",
    payMethods: ["GPay", "Apple Pay", "Visa", "MC", "Disc", "Amex"],
  },

  blocks: {
    foodStandard: {
      id: "food",
      title: "Food",
      icon: "food",
      items: [
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Nachos", price: "7.50" },
        { name: "Regular Fries", price: "6.50" },
        { name: "Add Cheese", price: "1.50", accent: true },
        { name: "Cheese Fries", price: "12.00" },
      ],
    },
    foodRedRally: {
      id: "food",
      title: "Food",
      icon: "food",
      items: [
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Nachos", price: "7.50" },
        { name: "Regular Fries", price: "6.50" },
        { name: "Add Cheese", price: "1.50", accent: true },
        {
          name: "Grit Hammer Bites",
          price: "15.00",
          note: "Popcorn chicken & fries — choice of spicy buffalo or classic.",
        },
        { name: "Cheese Fries", price: "12.00" },
      ],
    },
    snacks: {
      id: "snacks",
      title: "Snacks",
      icon: "snacks",
      items: [
        { name: "Popcorn — Regular", price: "4.00", highlight: true },
        { name: "Soft Pretzel", price: "6.00" },
        { name: "Candy", price: "7.00" },
        { name: "Chips", price: "4.50" },
        { name: "Peanuts", price: "5.00" },
      ],
    },
    coldDrinks: {
      id: "cold-drinks",
      title: "Cold Drinks",
      icon: "drinks",
      logos: true,
      items: [
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
        { name: "Souvenir Soda", price: "8.50", note: "Free refills" },
        { name: "Bottled Soda", price: "7.00" },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Gatorade", price: "5.50" },
        { name: "Monster Energy", price: "6.00" },
      ],
    },
    bottledDrinks: {
      id: "cold-drinks",
      title: "Bottled Drinks",
      icon: "drinks",
      logos: true,
      items: [
        { name: "Bottled Soda", price: "7.00" },
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Gatorade", price: "5.50" },
        { name: "Monster Energy", price: "6.00" },
      ],
    },
    beer: {
      id: "beer",
      title: "Beer + Booze",
      icon: "beer",
      ageGate: true,
      brands: ["Bud Light", "Coors Light"],
      items: [
        { name: "Domestic Beer — 16 oz", price: "12.00" },
        { name: "Premium Beer — 16 oz", price: "13.00" },
        { name: "Domestic Can", price: "9.00" },
        { name: "Seltzer / RTD", price: "10.00" },
        { name: "Cocktail", price: "12.00" },
      ],
    },
    beverageShack: {
      id: "drinks",
      title: "Drinks",
      icon: "drinks",
      logos: true,
      items: [
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
        { name: "Souvenir Soda", price: "8.50", note: "Free refills" },
        { name: "Bottled Soda", price: "7.00" },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Gatorade", price: "5.50" },
      ],
    },
    dawgs: {
      id: "dawgs",
      title: "Dawgs",
      icon: "food",
      items: [
        { name: "The Louie", price: "15.00", note: "Footlong · Frito pie style" },
        { name: "The Lucy", price: "14.00", note: "Footlong · Hatch green chile & cheese" },
        { name: "The Chomper", price: "14.00", note: "Footlong · roasted green chile relish" },
        {
          name: "The Lone Wolf",
          price: "12.00",
          note: "Footlong all-beef dog · classic stadium style",
        },
        { name: "Lobo Dog", price: "4.00", highlight: true },
      ],
    },
    dawgHouseFood: {
      id: "food",
      title: "Food",
      icon: "food",
      items: [
        { name: "Frito Pie", price: "12.00" },
        { name: "Regular Fries", price: "6.50" },
        { name: "Cheese Fries", price: "12.00" },
        { name: "Add Cheese", price: "1.50", accent: true },
      ],
    },
    value: {
      id: "value",
      title: "Fan Favorites",
      icon: "star",
      items: [
        { name: "16 oz Pepsi", price: "4.00", highlight: true },
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Popcorn", price: "4.00", highlight: true },
        { name: "Water", price: "4.00", highlight: true },
      ],
    },
    elotico: {
      id: "elotico",
      title: "Elotico",
      icon: "food",
      items: [
        { name: "Elotico", price: "9.00", note: "NM red chile elote cup" },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
      ],
    },
    miniMelts: {
      id: "mini-melts",
      title: "Mini Melts",
      icon: "snacks",
      items: [
        { name: "Mini Melts", price: "8.00", note: "Ask for available flavors" },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
      ],
    },
  },

  /**
   * Fireup print sheet locations (exact names + measurements).
   * page index follows the Fireup sheet order (1–12).
   */
  locations: [
    {
      page: 1,
      id: "lobo-trailer-n-scoreboard",
      name: "Lobo Trailer",
      stand: "N Scoreboard",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "24x36-portrait",
      variant: "portrait-trailer",
    },
    {
      page: 2,
      id: "mbp-mobile-beer",
      name: "MBP",
      stand: "Mobile Beer Portables",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "12x18-portrait",
      variant: "portrait-beer",
    },
    {
      page: 3,
      id: "grab-go-market",
      name: "Grab & Go Market",
      stand: "Market",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "96x36-landscape",
      variant: "grab-go",
    },
    {
      page: 4,
      id: "specialty-ne",
      name: "Specialty",
      stand: "NE",
      tagline: "Outside Price Menu · Dawg House",
      placement: "OUTSIDE",
      printKey: "96x36-landscape",
      variant: "dawg-house",
    },
    {
      page: 5,
      id: "specialty-nw",
      name: "Specialty",
      stand: "NW",
      tagline: "Outside Price Menu · Dawg House (mirrored)",
      placement: "OUTSIDE",
      printKey: "96x36-landscape",
      variant: "dawg-house",
    },
    {
      page: 6,
      id: "red-rally-interior",
      name: "Red Rally NE & NW",
      stand: "Interior",
      tagline: "Inside Price Menu",
      placement: "INSIDE",
      printKey: "96x36-landscape",
      variant: "red-rally",
    },
    {
      page: 7,
      id: "red-rally-exterior",
      name: "Red Rally NE & NW",
      stand: "Exterior",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "192x48-landscape",
      variant: "red-rally",
    },
    {
      page: 8,
      id: "se-beverage-shack",
      name: "Southeast Beverage Shack",
      stand: "SE",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "96x36-landscape",
      variant: "beverage-shack",
    },
    {
      page: 9,
      id: "sw-beverage-shack",
      name: "Southwest Beverage Shack",
      stand: "SW",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "96x36-landscape",
      variant: "beverage-shack",
    },
    {
      page: 10,
      id: "mbp-elotico",
      name: "MBP",
      stand: "Mobile Portable Elotico",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "12x18-portrait",
      variant: "portrait-elotico",
    },
    {
      page: 11,
      id: "mbp-mini-melts-ne",
      name: "MBP",
      stand: "Mini Melts NE",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "12x18-portrait",
      variant: "portrait-mini-melts",
    },
    {
      page: 12,
      id: "mbp-mini-melts-nw",
      name: "MBP",
      stand: "Mini Melts NW",
      tagline: "Outside Price Menu",
      placement: "OUTSIDE",
      printKey: "12x18-portrait",
      variant: "portrait-mini-melts",
    },
  ],
};

(function resolveMenuColumns() {
  const m = window.UNM_MENU;
  const b = m.blocks;

  const variants = {
    "grab-go": () => [b.bottledDrinks, b.snacks, b.beer, b.foodStandard, b.value],
    "red-rally": () => [b.foodRedRally, b.snacks, b.coldDrinks, b.beer, b.value],
    "dawg-house": () => [b.dawgs, b.dawgHouseFood, b.snacks, b.coldDrinks, b.beer],
    "beverage-shack": () => [b.beverageShack, b.beer, b.snacks, b.value, {
      id: "extras",
      title: "Extras",
      icon: "star",
      items: [
        { name: "Candy", price: "7.00" },
        { name: "Chips", price: "4.50" },
        { name: "Peanuts", price: "5.00" },
      ],
    }],
    "portrait-trailer": () => [b.value, b.foodStandard, b.snacks, b.coldDrinks],
    "portrait-beer": () => [b.beer, b.beverageShack],
    "portrait-elotico": () => [b.elotico],
    "portrait-mini-melts": () => [b.miniMelts],
  };

  m.locations.forEach((loc) => {
    const preset = m.printPresets[loc.printKey];
    loc.print = preset;
    const fn = variants[loc.variant] || variants["grab-go"];
    loc.columns = fn();
  });

  m.coreColumns = variants["red-rally"]();
})();
