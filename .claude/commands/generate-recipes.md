# Generate Daily Optimised Meal Plan

Generate today's 3-meal nutrition-optimised, budget-minimised meal plan for NutriCents.

## Steps to Execute

### Step 1 — Establish Today's Date
- Determine today's date in `YYYY-MM-DD` format (Australian Eastern Time).
- All output files will use this date.

### Step 2 — Fetch Current Grocery Prices
Fetch current prices from the following Australian supermarket sources. Check **on-special** pages first, then everyday prices:

**Coles on-special:**
- https://www.coles.com.au/on-special/meat-seafood
- https://www.coles.com.au/on-special/fruit-vegetables
- https://www.coles.com.au/on-special/dairy-eggs-fridge
- https://www.coles.com.au/on-special/pantry

**Coles everyday:**
- https://www.coles.com.au/browse/fruit-vegetables
- https://www.coles.com.au/browse/dairy-eggs-fridge
- https://www.coles.com.au/browse/pantry
- https://www.coles.com.au/browse/meat-seafood

**Woolworths:**
- https://www.woolworths.com.au/shop/specials/
- https://www.woolworths.com.au/shop/browse/fruit-veg
- https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge
- https://www.woolworths.com.au/shop/browse/pantry
- https://www.woolworths.com.au/shop/browse/meat-poultry-seafood

**ALDI:**
- https://www.aldi.com.au/en/specials/
- https://www.aldi.com.au/en/groceries/

Extract: store name, product name, product ID/SKU (or URL slug), category, unit, unit size, price, whether on special, and source URL. Calculate price_per_100g for each item.

Save all results to `prices/prices_YYYY-MM-DD.csv` with columns:
```
date,store,product_name,product_id,category,unit,unit_size,price_aud,price_per_100g,on_special,special_price_aud,source_url
```

Create the `prices/` directory if it doesn't exist.

### Step 3 — Review Nutritional Database
Open and analyse `AFCD Release 3 - Nutrient profiles.xlsx`:
- Cross-reference ingredients found at good prices today against their AFCD nutrient profiles
- Identify ingredients with the best nutrient density per dollar at today's prices
- Build a shortlist of top-value ingredients for today's meal plan
- Cover all essential vitamins, minerals, and macronutrients across the 3 meals

### Step 4 — Review Previously Generated Recipes
Scan all files in `recipes/*.html`:
- Identify which ingredients, food groups, and nutrients have been frequently used
- Note which nutrients/food groups are underrepresented in recent history
- Plan today's recipes to fill nutritional and variety gaps
- If fewer than 3 previous recipe files exist, prioritise maximum nutrient breadth

### Step 5 — Design 3 Optimised Meals

Design Breakfast, Lunch, and Dinner **holistically** — they work as a system for the day.

**Constraints:**
- Minimise total daily food cost (sum of all 3 meals)
- Maximise nutritional spectrum coverage across the 3 meals combined
- Target ALL of these health benefits across the day:
  - Cardiovascular health (omega-3s, fibre, potassium, polyphenols)
  - Low blood pressure (potassium, magnesium, low sodium)
  - Anti-cancer (cruciferous veg, antioxidants, allicin, lycopene)
  - Lower LDL cholesterol (soluble fibre, plant sterols, healthy fats)
  - Low sugar / low GI (wholegrains, legumes, vegetables)
- Use on-special items where possible (highest priority)
- Share ingredients across meals where it reduces waste and cost
- Use Australian food terminology and seasonal awareness

**For each meal, prepare:**
- Recipe name (descriptive, health-benefit-focused)
- Ingredient list with exact quantities, store, and price per ingredient
- Total meal cost
- Macros: protein (g), carbohydrates (g), dietary fibre (g), total fat (g), sugar (g), calories (kcal)
- Micronutrient coverage (% RDI for each vitamin and mineral provided)
- Which of the 6 health targets this meal addresses (and how)
- GI rating (Low / Medium / High) with brief justification
- Step-by-step cooking instructions (simple, minimal equipment)
- Prep time + cook time

Order the 3 meals in the HTML from cheapest to most expensive.

### Step 6 — Generate `recipes/YYYY-MM-DD.html`

Write a self-contained, beautiful dark-theme HTML page.

**Design rules (match Screenshot.png):**
- Background: `#0f0f0f` or `#111111`
- Card backgrounds: `#1a1a1a` with `1px solid #2a2a2a` border
- Accent / highlight colour: `#4ecca3` (teal-green)
- Headings: white (`#ffffff`), body text: `#cccccc`
- Font: system-ui or Inter (load from Google Fonts)
- Cards with `border-radius: 12px`, `padding: 24px`, soft box-shadow
- Nutrient progress bars: coloured bars (teal fill, dark bg) showing % RDI
- Fully responsive (mobile-first)
- No JavaScript frameworks. Vanilla CSS only.

**Page structure:**
```
Header: NutriCents logo/name + tagline + today's date
Subheader: Total daily cost | Total estimated kcal | Health targets covered

[Meal 1 Card] — Cheapest
  - Meal name + emoji
  - Health badges (e.g. "❤️ Heart Health", "🩸 Low GI")
  - Ingredients table (ingredient | qty | store | price)
  - Total cost callout
  - Macro summary (protein / carbs / fat / fibre / calories)
  - Nutrient progress bars (% RDI per vitamin/mineral)
  - Cooking instructions (numbered steps)
  - Prep & cook time

[Meal 2 Card]
[Meal 3 Card]

[Daily Shopping List Section]
  - Consolidated ingredient list for all 3 meals
  - Grouped by store
  - Total cost per store
  - Grand total

Footer: "Powered by AFCD data · Prices from Coles, Woolworths, ALDI · Generated YYYY-MM-DD"
```

Create the `recipes/` directory if it doesn't exist.

### Step 7 — Update `index.html`

Update or create `index.html` in the repo root:
- List all recipe dates (most recent first), linking to `recipes/YYYY-MM-DD.html`
- Show for each entry: date, total daily cost, headline health benefits covered
- Same dark theme as recipe pages
- Include a brief project description at the top ("Cheapest possible nutritious meals for Australians")
- Keep all existing entries intact, prepend today's new entry

### Step 8 — Report Summary

After all files are written, output a brief summary:
- Today's date
- Total daily cost (all 3 meals combined)
- Cheapest meal and its cost
- Top 3 on-special ingredients used
- Key nutrients this plan excels at
- Any nutritional gaps identified (and plan to address in future runs)
- Files written: list all new/modified files
