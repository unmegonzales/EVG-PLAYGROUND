/* UNM Lobos 25/26 Football Concessions — menu data
   Replicate a location by cloning an entry and editing columns.
*/

window.UNM_MENU = {
  season: "25/26",
  title: "Lobo Football Menu",
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

  /** Shared brand soda set shown on many stands */
  sodaLogos: ["Starry", "Pepsi Zero", "Wild Cherry", "Dr Pepper", "Gatorade", "Aquafina"],

  locations: [
    {
      id: "stadium-sips-sw",
      name: "Stadium Sips",
      stand: "SW Shack",
      tagline: "Concessions",
      layout: "classic-tri",
      columns: [
        {
          type: "cold-drinks",
          title: "Cold Drinks",
          logos: true,
          items: [
            { name: "Souvenir Soda", price: "8.50", note: "Free refills" },
            { name: "20 oz. Bottle Soda", price: "5.50" },
            { name: "Gatorade", price: "5.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Monster Energy", price: "6.00" },
          ],
        },
        {
          type: "snacks",
          title: "Snacks",
          items: [
            { name: "Popcorn", price: "4.00", highlight: true },
            { name: "Candy", price: "5.00" },
            { name: "Peanuts", price: "5.00" },
            { name: "Chips", price: "4.50" },
          ],
        },
        {
          type: "beer",
          title: "Beer Time",
          ageGate: true,
          brands: ["Bud Light", "Teller"],
          items: [
            { name: "Domestic Draft", sizes: ["16 oz 8.50", "24 oz 11.00"] },
            { name: "Premium Draft", sizes: ["16 oz 10.00", "24 oz 13.00"] },
            { name: "Domestic Can", price: "9.00" },
            { name: "Seltzer / RTD", price: "10.00" },
            { name: "Cocktail", price: "12.00" },
          ],
        },
      ],
    },
    {
      id: "south-tower",
      name: "The Tower",
      stand: "South Tower",
      tagline: "Concessions",
      layout: "classic-tri",
      columns: [
        {
          type: "cold-drinks",
          title: "Cold Drinks",
          logos: true,
          items: [
            { name: "Souvenir Soda", price: "8.50", note: "Free refills" },
            { name: "20 oz. Bottle Soda", price: "5.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Gatorade", price: "5.50" },
          ],
        },
        {
          type: "food",
          title: "Hot Favorites",
          items: [
            { name: "Lobo Dog", price: "4.00", highlight: true },
            { name: "Nachos", price: "8.50" },
            { name: "Soft Pretzel", price: "6.00" },
            { name: "Popcorn", price: "4.00", highlight: true },
          ],
        },
        {
          type: "beer",
          title: "Beer Time",
          ageGate: true,
          brands: ["Bud Light", "Teller"],
          items: [
            { name: "Domestic Draft", sizes: ["16 oz 8.50", "24 oz 11.00"] },
            { name: "Premium Draft", sizes: ["16 oz 10.00", "24 oz 13.00"] },
            { name: "Domestic Can", price: "9.00" },
            { name: "Cocktail", price: "12.00" },
          ],
        },
      ],
    },
    {
      id: "red-rally-nw",
      name: "Red Rally",
      stand: "NW Stand",
      tagline: "Concessions",
      layout: "classic-tri",
      columns: [
        {
          type: "cold-drinks",
          title: "Cold Drinks",
          logos: true,
          items: [
            { name: "16 oz. Pepsi Product", price: "4.00", highlight: true },
            { name: "Souvenir Soda", price: "8.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Gatorade", price: "5.50" },
          ],
        },
        {
          type: "snacks",
          title: "Snacks",
          items: [
            { name: "Popcorn", price: "4.00", highlight: true },
            { name: "Candy", price: "5.00" },
            { name: "Chips", price: "4.50" },
            { name: "Nuts", price: "5.00" },
          ],
        },
        {
          type: "beer",
          title: "Beer Time",
          ageGate: true,
          brands: ["Bud Light"],
          items: [
            { name: "Domestic Draft", sizes: ["16 oz 8.50", "24 oz 11.00"] },
            { name: "Domestic Can", price: "9.00" },
            { name: "Seltzer / RTD", price: "10.00" },
          ],
        },
      ],
    },
    {
      id: "main-west-premium",
      name: "Main West",
      stand: "Premium Eats",
      tagline: "New for 25/26",
      layout: "classic-tri",
      columns: [
        {
          type: "food",
          title: "Signature Eats",
          items: [
            { name: "The Big Chuck", price: "15.00", note: "Fried beef · chile aioli · fries" },
            { name: "Green Chile Cheese Fries", price: "13.00" },
            { name: "Louie's Classic Frito Pie", price: "12.00" },
            { name: "Elotico", price: "9.00", note: "NM red chile elote cup" },
          ],
        },
        {
          type: "food",
          title: "Louie's Footlongs",
          items: [
            { name: "The Louie", price: "12.00", note: "Frito pie footlong" },
            { name: "The Lucy", price: "12.00", note: "Hatch green chile & cheese" },
            { name: "The Chomper", price: "12.00", note: "Roasted green chile relish" },
            { name: "Lobo Dog", price: "4.00", highlight: true },
          ],
        },
        {
          type: "cold-drinks",
          title: "Drinks",
          logos: true,
          items: [
            { name: "16 oz. Pepsi Product", price: "4.00", highlight: true },
            { name: "Souvenir Soda", price: "8.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Domestic Draft", price: "8.50" },
          ],
        },
      ],
    },
    {
      id: "nw-grab-go",
      name: "Grab 'N Go",
      stand: "NW Stadium",
      tagline: "Quick Service",
      layout: "classic-tri",
      columns: [
        {
          type: "cold-drinks",
          title: "Bottled Drinks",
          logos: true,
          items: [
            { name: "20 oz. Bottle Soda", price: "5.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Gatorade", price: "5.50" },
            { name: "Monster Energy", price: "6.00" },
          ],
        },
        {
          type: "snacks",
          title: "Snacks",
          items: [
            { name: "Popcorn", price: "4.00", highlight: true },
            { name: "Candy", price: "5.00" },
            { name: "Chips", price: "4.50" },
            { name: "Peanuts", price: "5.00" },
            { name: "Soft Pretzel", price: "6.00" },
          ],
        },
        {
          type: "value",
          title: "Fan Favorites",
          promo: true,
          items: [
            { name: "16 oz. Pepsi", price: "4.00", highlight: true },
            { name: "Lobo Dog", price: "4.00", highlight: true },
            { name: "Popcorn", price: "4.00", highlight: true },
            { name: "Water", price: "4.00", highlight: true },
          ],
        },
      ],
    },
    {
      id: "ne-concessions",
      name: "Northeast",
      stand: "NE Concessions",
      tagline: "Concessions",
      layout: "classic-tri",
      columns: [
        {
          type: "cold-drinks",
          title: "Cold Drinks",
          logos: true,
          items: [
            { name: "16 oz. Pepsi Product", price: "4.00", highlight: true },
            { name: "Souvenir Soda", price: "8.50" },
            { name: "Aquafina Water", price: "4.00", highlight: true },
            { name: "Gatorade", price: "5.50" },
          ],
        },
        {
          type: "food",
          title: "Ballpark Bites",
          items: [
            { name: "Lobo Dog", price: "4.00", highlight: true },
            { name: "Nachos", price: "8.50" },
            { name: "Popcorn", price: "4.00", highlight: true },
            { name: "Candy", price: "5.00" },
          ],
        },
        {
          type: "beer",
          title: "Beer Time",
          ageGate: true,
          brands: ["Bud Light", "Teller"],
          items: [
            { name: "Domestic Draft", sizes: ["16 oz 8.50", "24 oz 11.00"] },
            { name: "Premium Draft", sizes: ["16 oz 10.00", "24 oz 13.00"] },
            { name: "Domestic Can", price: "9.00" },
            { name: "Cocktail", price: "12.00" },
          ],
        },
      ],
    },
  ],

  /** Standalone promo board — this year's launch style */
  promo: {
    id: "four-for-four",
    eyebrow: "All Season Long",
    headline: "4 FOR $4",
    subhead: "Fan Favorites · Value Menu",
    tagline: "Affordable. Simple. Go Lobos.",
    hashtag: "#GOLOBOS",
    items: [
      { name: "16 oz. Pepsi", price: "4", icon: "soda" },
      { name: "Lobo Dog", price: "4", icon: "dog" },
      { name: "Popcorn", price: "4", icon: "popcorn" },
      { name: "Water", price: "4", icon: "water" },
    ],
    note: "Available at main west, northwest & northeast concession areas.",
  },
};
