/* UNM Lobos 25/26 Football Concessions — menu data
   Updated from LOBO_Football_Menu_Graphic_Designer_Change_Sheet.docx
   Prices display WITHOUT dollar signs (production convention).
*/

window.UNM_MENU = {
  season: "25/26",
  title: "Lobo Football Menu",
  athleticsLine: "Lobos Athletics",
  universityLine: "University of New Mexico",
  taxNote: "All prices subject to applicable sales tax.",
  cashless: true,
  changeSheet: "LOBO Football Menu Graphic Designer Change Sheet",
  brand: {
    cherry: "#BA0C2F",
    silver: "#A7A8AA",
    metal: "#4A4F55",
    turquoise: "#00A8B5",
    white: "#FFFFFF",
    light: "#F4F4F6",
  },

  sodaLogos: ["Pepsi", "Mt Dew", "Dr Pepper", "Starry", "Dasani"],

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

  /** Shared building blocks (post change-sheet) */
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
    snacksNoPickle: {
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
    dawgs: {
      id: "dawgs",
      title: "Dawgs",
      icon: "food",
      items: [
        {
          name: "The Louie",
          price: "15.00",
          note: "Footlong · Frito pie style",
        },
        {
          name: "The Lucy",
          price: "14.00",
          note: "Footlong · Hatch green chile & cheese",
        },
        {
          name: "The Chomper",
          price: "14.00",
          note: "Footlong · roasted green chile relish",
        },
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
  },

  /**
   * 10-page production deck (matches change-sheet page numbers).
   * Each location may override `columns`; otherwise uses standardCore().
   */
  locations: [
    {
      page: 1,
      id: "page-01-stadium-sips",
      name: "Stadium Sips",
      stand: "SW Shack",
      tagline: "Concessions",
      variant: "standard",
    },
    {
      page: 2,
      id: "page-02-south-tower",
      name: "The Tower",
      stand: "South Tower",
      tagline: "Concessions",
      variant: "standard",
    },
    {
      page: 3,
      id: "page-03-northeast",
      name: "Northeast",
      stand: "NE Concessions",
      tagline: "Concessions",
      variant: "standard",
    },
    {
      page: 4,
      id: "page-04-grab-go",
      name: "Grab 'N Go",
      stand: "NW Stadium",
      tagline: "Quick Service",
      variant: "bottled",
    },
    {
      page: 5,
      id: "page-05-red-rally-a",
      name: "Red Rally",
      stand: "Stand A",
      tagline: "Concessions",
      variant: "red-rally",
    },
    {
      page: 6,
      id: "page-06-main-west",
      name: "Main West",
      stand: "Concessions",
      tagline: "Concessions",
      variant: "standard",
    },
    {
      page: 7,
      id: "page-07-dawg-house-b",
      name: "Dawg House",
      stand: "Rendition B",
      tagline: "Was Nacho Mama · Mirrored menu",
      variant: "dawg-house",
    },
    {
      page: 8,
      id: "page-08-red-rally-b",
      name: "Red Rally",
      stand: "Stand B",
      tagline: "Concessions",
      variant: "red-rally",
    },
    {
      page: 9,
      id: "page-09-west-stand",
      name: "West Stand",
      stand: "Concessions",
      tagline: "Concessions",
      variant: "standard",
    },
    {
      page: 10,
      id: "page-10-dawg-house-a",
      name: "Dawg House",
      stand: "Primary",
      tagline: "Footlongs & Favorites",
      variant: "dawg-house",
    },
  ],
};

/** Resolve columns per location variant after data load */
(function resolveMenuColumns() {
  const m = window.UNM_MENU;
  const b = m.blocks;

  function standard() {
    return [b.foodStandard, b.snacks, b.coldDrinks, b.beer, {
      id: "value",
      title: "Fan Favorites",
      icon: "star",
      promo: true,
      items: [
        { name: "16 oz Pepsi", price: "4.00", highlight: true },
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Popcorn", price: "4.00", highlight: true },
        { name: "Water", price: "4.00", highlight: true },
      ],
    }];
  }

  function bottled() {
    return [b.bottledDrinks, b.snacksNoPickle, b.beer, {
      id: "food",
      title: "Food",
      icon: "food",
      items: [
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Nachos", price: "7.50" },
        { name: "Regular Fries", price: "6.50" },
        { name: "Cheese Fries", price: "12.00" },
      ],
    }, {
      id: "value",
      title: "Fan Favorites",
      icon: "star",
      items: [
        { name: "16 oz Pepsi", price: "4.00", highlight: true },
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Popcorn", price: "4.00", highlight: true },
        { name: "Water", price: "4.00", highlight: true },
      ],
    }];
  }

  function redRally() {
    // Change sheet: remove LOBO CLASSICS header on these pages
    return [b.foodRedRally, b.snacks, b.coldDrinks, b.beer, {
      id: "value",
      title: "Fan Favorites",
      icon: "star",
      items: [
        { name: "16 oz Pepsi", price: "4.00", highlight: true },
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Popcorn", price: "4.00", highlight: true },
        { name: "Water", price: "4.00", highlight: true },
      ],
    }];
  }

  function dawgHouse() {
    // No nachos, no frozen Lobo Ritas; Frito Pie lives here only
    return [b.dawgs, b.dawgHouseFood, b.snacks, b.coldDrinks, b.beer];
  }

  const map = {
    standard,
    bottled,
    "red-rally": redRally,
    "dawg-house": dawgHouse,
  };

  m.locations.forEach((loc) => {
    const fn = map[loc.variant] || standard;
    loc.columns = fn();
  });

  m.coreColumns = standard();
})();
