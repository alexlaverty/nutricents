# Generate Daily Optimised Meal Plan

Generate today's 3-meal nutrition-optimised, budget-minimised meal plan for NutriCents.

## Steps to Execute

### Step 1 — Establish Today's Date
- Determine today's date in `YYYY-MM-DD` format (Australian Eastern Time).
- All output files will use this date.

### Step 2 — Load or Fetch Grocery Prices

**First, check the prices cache:**
Open `prices/prices_YYYY-MM-DD.csv` (today's date). If it exists:
- Read all rows and note which stores already have prices recorded
- For any store that already has rows in the CSV, **skip fetching that store** — use the cached data directly
- Prices with a `source_url` starting with `receipt-` are receipt-verified and always trusted

**For stores not yet in today's CSV**, fetch prices using Chrome by loading these URLs:

**ALDI (check these first — best value):**
- Fruit & vegetables: `https://www.aldi.com.au/products/fruits-vegetables/k/950000000`
- Meat & seafood: `https://www.aldi.com.au/products/meat-seafood/k/940000000`
- Dairy, eggs & fridge: `https://www.aldi.com.au/products/dairy-eggs-fridge/k/960000000`
- Lower prices (everyday deals): `https://www.aldi.com.au/products/lower-prices/k/1588161425841179`
- Super savers: `https://www.aldi.com.au/products/super-savers/k/1588161426952145`
- Limited time only (specials): `https://www.aldi.com.au/products/limited-time-only/k/1588161420755352`

**Woolworths specials (check before everyday):**
- Fruit & veg specials: `https://www.woolworths.com.au/shop/browse/fruit-veg/fruit-veg-specials`
- Meat & seafood specials: `https://www.woolworths.com.au/shop/browse/poultry-meat-seafood/poultry-meat-seafood-specials`
- Half price: `https://www.woolworths.com.au/shop/browse/specials/half-price`

**Woolworths everyday:**
- `https://www.woolworths.com.au/shop/browse/fruit-veg`
- `https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge`
- `https://www.woolworths.com.au/shop/browse/pantry`
- `https://www.woolworths.com.au/shop/browse/meat-poultry-seafood`

**Coles on-special (check before everyday):**
- `https://www.coles.com.au/on-special/meat-seafood`
- `https://www.coles.com.au/on-special/fruit-vegetables`
- `https://www.coles.com.au/on-special/dairy-eggs-fridge`
- `https://www.coles.com.au/on-special/pantry`

**Coles everyday:**
- `https://www.coles.com.au/browse/fruit-vegetables`
- `https://www.coles.com.au/browse/dairy-eggs-fridge`
- `https://www.coles.com.au/browse/pantry`
- `https://www.coles.com.au/browse/meat-seafood`

**PRICE INTEGRITY — CRITICAL:**
- **Never estimate, guess, or fabricate a price.** Only record prices you have personally read from the store's website.
- If a page fails to load, or a product's price is not visible, **leave the price blank** in the recipe and note "price unavailable — check in-store".
- A recipe with some missing prices is far better than a recipe with invented prices.
- Do not use training-data knowledge of "typical" prices as a fallback — prices change and will mislead the user.

**Save verified prices** to `prices/prices_YYYY-MM-DD.csv` (append, do not duplicate by product_id):
```
date,store,product_name,product_id,category,unit,unit_size,price_aud,price_per_100g,on_special,special_price_aud,source_url
```
- `source_url` — the exact URL you loaded to find this price
- `price_per_100g` — calculate from price and unit size
- `on_special` — `true` / `false`
- `special_price_aud` — was-price if on special, else blank

Create the `prices/` directory if it doesn't exist.

### Step 3 — Review Nutritional Database
Open and analyse `AFCD Release 3 - Nutrient profiles.xlsx`:
- Cross-reference ingredients found at verified prices today against their AFCD nutrient profiles
- Identify ingredients with the best nutrient density per dollar at today's prices
- Build a shortlist of top-value ingredients for today's meal plan
- Cover all essential vitamins, minerals, and macronutrients across the 3 meals

### Step 4 — Review Previously Generated Recipes
Scan all files in `recipes/*.html`:
- Identify which ingredients, food groups, and nutrients have been frequently used in past days
- Note which nutrients/food groups are underrepresented in recent history
- Plan today's recipes to fill nutritional and variety gaps
- If fewer than 3 previous recipe files exist, prioritise maximum nutrient breadth

### Step 5 — Check Today's Existing Meals (If Any)
Check if `recipes/YYYY-MM-DD.html` already exists for today:
- If it does, read and parse the existing meal cards to understand what has already been generated today
- Tally up the nutrition already covered across today's existing meals (macros, micros, sodium, key food groups)
- The 3 new meals you generate must **complement** today's existing meals holistically — together all of today's meals should cover the broadest possible nutritional spectrum
- Avoid duplicating meals or ingredients already in today's file
- If the file does not exist yet, proceed with maximum nutritional breadth as normal

### Step 6 — Design 3 Optimised Meals

Design Breakfast, Lunch, and Dinner **holistically** — they work as a system across the whole day.

**Constraints:**
- Minimise total daily food cost (sum of all 3 meals)
- Maximise nutritional spectrum coverage across all of today's meals combined (including any already generated)
- Target ALL of these health benefits across the day:
  - Cardiovascular health (omega-3s, fibre, potassium, polyphenols)
  - Low blood pressure (potassium, magnesium, low sodium)
  - Anti-cancer (cruciferous veg, antioxidants, allicin, lycopene)
  - Lower LDL cholesterol (soluble fibre, plant sterols, healthy fats)
  - Low sugar / low GI (wholegrains, legumes, vegetables)
- Use on-special / super-saver / limited-time items where possible (highest priority)
- Share ingredients across meals where it reduces waste and cost
- Use Australian food terminology and seasonal awareness
- **STRICT — LACTOSE FREE:** The user is severely lactose intolerant. NEVER use regular milk, regular yoghurt, regular cheese, cream, or butter. ONLY use lactose-free dairy (Zymil, Jalna Lactose Free, ALDI Lact-Free) or plant-based alternatives (oat milk, soy milk). Hard aged cheeses in tiny amounts are acceptable but must be flagged. Prefer canned salmon/sardines, eggs, broccoli, and leafy greens for calcium.
- **STRICT — LOW SODIUM:** Daily sodium target is ≤1,500mg (≤500mg per meal). Never add table salt. Use no-added-salt canned goods (tomatoes, legumes). Use low-sodium soy sauce only. Avoid processed meats, stock cubes, and high-sodium condiments. Flavour with garlic, lemon, herbs, and spices instead. Show sodium (mg) and % of 1,500mg daily target prominently in every meal's nutrient breakdown.

**For each meal, prepare:**
- Recipe name (descriptive, health-benefit-focused)
- Ingredient list with exact quantities, store, and **verified price** per ingredient (blank if price not confirmed)
- Total meal cost (sum only confirmed prices; note if total is partial due to unconfirmed prices)
- Macros: protein (g), carbohydrates (g), dietary fibre (g), total fat (g), sugar (g), calories (kcal)
- Micronutrient coverage (% RDI for each vitamin and mineral provided)
- Which of the 6 health targets this meal addresses (and how)
- GI rating (Low / Medium / High) with brief justification
- Step-by-step cooking instructions (simple, minimal equipment)
- Prep time + cook time

Order the 3 meals in the HTML from cheapest to most expensive.

### Step 7 — Write or Append to `recipes/YYYY-MM-DD.html`

**If the file does not exist:** create it as a full self-contained dark-theme HTML page (see design rules below).

**If the file already exists:** append the 3 new meal cards into the existing page — insert them before the shopping list section (or before `</main>` / `</body>` if the shopping list is regenerated). Also regenerate/update the shopping list to consolidate ALL of today's meals (old + new). Update the day-total stats in the header to reflect all meals now in the file.

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
           (reflects ALL meals for today, including prior runs)

[Meal Card — Set 1, Meal 1] — Cheapest
  - Meal name + emoji
  - Health badges (e.g. "❤️ Heart Health", "🩸 Low GI")
  - Ingredients table (ingredient | qty | store | price — blank if unverified)
  - Total cost callout (note if partial due to unverified prices)
  - Macro summary (protein / carbs / fat / fibre / calories)
  - Nutrient progress bars (% RDI per vitamin/mineral)
  - Sodium callout (mg + % of 1,500mg daily target)
  - Cooking instructions (numbered steps)
  - Prep & cook time

[Meal Card — Set 1, Meal 2]
[Meal Card — Set 1, Meal 3]

(... additional meal sets appended here on subsequent runs ...)

[Daily Shopping List Section]
  - Consolidated ingredient list for ALL meals in today's file
  - Grouped by store
  - Total cost per store (confirmed prices only)
  - Grand total (with note if some prices are unverified)

Footer: "Powered by AFCD data · Prices from Coles, Woolworths, ALDI · Generated YYYY-MM-DD"
```

Create the `recipes/` directory if it doesn't exist.

### Step 8 — Update `index.html`

Update or create `index.html` in the repo root:
- List all recipe dates (most recent first), linking to `recipes/YYYY-MM-DD.html`
- Show for each entry: date, total daily cost, number of meals, headline health benefits covered
- Same dark theme as recipe pages
- Include a brief project description at the top ("Cheapest possible nutritious meals for Australians")
- Keep all existing entries intact, update today's entry with the latest stats

### Step 9 — Report Summary

After all files are written, output a brief summary:
- Today's date
- Total daily cost across all of today's meals (confirmed prices only)
- Cheapest meal and its cost
- Any ingredients where price could not be verified (user should check in-store)
- Top on-special / super-saver ingredients used
- Key nutrients this plan excels at
- Any nutritional gaps identified (and plan to address in future runs)
- Files written: list all new/modified files
