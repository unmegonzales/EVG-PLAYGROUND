/* UNM Lobos 25/26 Football Concessions — menu data
   Primary layout matches the stadium board sample:
   hero (brand + Fan Favorites + 4-for-$4) → 5 columns → footer.
   Clone a location entry to replicate for another stand.
*/

window.UNM_MENU = {
  season: "25/26",
  title: "Lobo Football Menu",
  athleticsLine: "Lobos Athletics",
  universityLine: "University of New Mexico",
  taxNote: "All prices subject to applicable sales tax.",
  cashless: true,
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

  /**
   * Shared 5-column core used across stands.
   * Per-location overrides can replace `columns` entirely.
   */
  coreColumns: [
    {
      id: "food",
      title: "Food",
      icon: "food",
      items: [
        { name: "Lobo Dog", price: "4.00", highlight: true },
        { name: "Nachos", price: "7.50" },
        { name: "Regular Fries", price: "6.50" },
        { name: "Add Cheese", price: "1.50", accent: true },
        { name: "The Big Chuck", price: "15.00", note: "Fried beef · chile aioli · fries" },
        { name: "Green Chile Cheese Fries", price: "13.00" },
        { name: "Louie's Classic Frito Pie", price: "12.00" },
      ],
    },
    {
      id: "snacks",
      title: "Snacks",
      icon: "snacks",
      items: [
        { name: "Popcorn — Regular", price: "4.00", highlight: true },
        { name: "Popcorn — Souvenir", price: "13.00" },
        { name: "Soft Pretzel", price: "6.00" },
        { name: "Candy", price: "5.00" },
        { name: "Chips", price: "4.50" },
        { name: "Peanuts", price: "5.00" },
      ],
    },
    {
      id: "cold-drinks",
      title: "Cold Drinks",
      icon: "drinks",
      logos: true,
      items: [
        { name: "Pepsi Product — 16 oz", price: "4.00", highlight: true },
        { name: "Souvenir Soda", price: "8.50", note: "Free refills" },
        { name: "20 oz Bottle Soda", price: "5.50" },
        { name: "Water", price: "4.00", highlight: true },
        { name: "Gatorade", price: "5.50" },
        { name: "Monster Energy", price: "6.00" },
      ],
    },
    {
      id: "beer",
      title: "Beer + Booze",
      icon: "beer",
      ageGate: true,
      brands: ["Bud Light", "Coors Light"],
      items: [
        { name: "Domestic Draft", sizes: ["16 oz · 8.50", "24 oz · 11.00"] },
        { name: "Premium Draft", sizes: ["16 oz · 10.00", "24 oz · 13.00"] },
        { name: "Domestic Can", price: "9.00" },
        { name: "Seltzer / RTD", price: "10.00" },
        { name: "Cocktail", price: "12.00" },
      ],
    },
    {
      id: "classics",
      title: "Lobo Classics",
      icon: "star",
      items: [
        { name: "Loborita", sizes: ["Single · 15.00", "Double · 28.00"] },
        { name: "MVP Supreme Carne Asada", price: "16.00" },
        { name: "The Louie Footlong", price: "12.00", note: "Frito pie style" },
        { name: "The Lucy Footlong", price: "12.00", note: "Hatch green chile & cheese" },
        { name: "The Chomper Footlong", price: "12.00", note: "Green chile relish" },
        { name: "Elotico", price: "9.00", note: "NM red chile elote cup" },
      ],
    },
  ],

  locations: [
    {
      id: "stadium-sips-sw",
      name: "Stadium Sips",
      stand: "SW Shack",
      tagline: "Concessions",
    },
    {
      id: "south-tower",
      name: "The Tower",
      stand: "South Tower",
      tagline: "Concessions",
    },
    {
      id: "red-rally-nw",
      name: "Red Rally",
      stand: "NW Stand",
      tagline: "Concessions",
    },
    {
      id: "main-west-premium",
      name: "Main West",
      stand: "Premium Eats",
      tagline: "New for 25/26",
    },
    {
      id: "nw-grab-go",
      name: "Grab 'N Go",
      stand: "NW Stadium",
      tagline: "Quick Service",
    },
    {
      id: "ne-concessions",
      name: "Northeast",
      stand: "NE Concessions",
      tagline: "Concessions",
    },
  ],
};
