# NutriCents — Claude Operating Instructions

## Project Mission

Generate the **absolute healthiest, most nutritious meals possible for the absolute lowest price**, tailored for an Australian (Sydney-based) audience.

Every decision — ingredient selection, recipe design, meal planning — must be optimised along two axes simultaneously:
1. **Maximum nutrition quality** (broadest spectrum of essential vitamins, minerals, macros, and health-promoting compounds)
2. **Minimum total cost** (based on real, current Sydney grocery prices)

---

## Nutrition Data Source

**File:** `AFCD Release 3 - Nutrient profiles.xlsx` (in this repo root)

This is the **Australian Food Composition Database (AFCD) Release 3** — a reference database containing nutrient content of foods commonly available in Australia. Data is primarily sourced from high-quality laboratory analysis.

- Always cross-reference ingredient nutritional data against this file before finalising recipes.
- When selecting ingredients, rank them by nutrient density per dollar using AFCD data.
- Track coverage of: protein, carbohydrates, dietary fibre, total fat, omega-3s, vitamins (A, B1, B2, B3, B5, B6, B7, B9, B12, C, D, E, K), and minerals (calcium, iron, magnesium, potassium, sodium, zinc, selenium, phosphorus, manganese, copper, iodine, chromium, molybdenum).

---

## Grocery Price Sources

Always fetch **current prices** from Australian supermarkets before generating recipes. Prices must be real, dated, and saved.

### Primary Sources (Sydney-based)

**Coles**

| Type | URL |
|------|-----|
| On-special — meat/seafood | `https://www.coles.com.au/on-special/meat-seafood` |
| On-special — fruit/veg | `https://www.coles.com.au/on-special/fruit-vegetables` |
| On-special — dairy/eggs | `https://www.coles.com.au/on-special/dairy-eggs-fridge` |
| On-special — pantry | `https://www.coles.com.au/on-special/pantry` |
| Everyday — fruit/veg | `https://www.coles.com.au/browse/fruit-vegetables` |
| Everyday — dairy/eggs | `https://www.coles.com.au/browse/dairy-eggs-fridge` |
| Everyday — pantry | `https://www.coles.com.au/browse/pantry` |
| Everyday — meat/seafood | `https://www.coles.com.au/browse/meat-seafood` |

**Woolworths**

| Type | URL |
|------|-----|
| Specials — fruit/veg | `https://www.woolworths.com.au/shop/browse/fruit-veg/fruit-veg-specials` |
| Specials — meat/seafood | `https://www.woolworths.com.au/shop/browse/poultry-meat-seafood/poultry-meat-seafood-specials` |
| Specials — half price | `https://www.woolworths.com.au/shop/browse/specials/half-price` |
| Everyday — fruit/veg | `https://www.woolworths.com.au/shop/browse/fruit-veg` |
| Everyday — dairy/eggs | `https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge` |
| Everyday — pantry | `https://www.woolworths.com.au/shop/browse/pantry` |
| Everyday — meat/seafood | `https://www.woolworths.com.au/shop/browse/meat-poultry-seafood` |

**ALDI**

| Type | URL |
|------|-----|
| Fruit & vegetables | `https://www.aldi.com.au/products/fruits-vegetables/k/950000000` |
| Meat & seafood | `https://www.aldi.com.au/products/meat-seafood/k/940000000` |
| Dairy, eggs & fridge | `https://www.aldi.com.au/products/dairy-eggs-fridge/k/960000000` |
| Lower prices (everyday deals) | `https://www.aldi.com.au/products/lower-prices/k/1588161425841179` |
| Super savers | `https://www.aldi.com.au/products/super-savers/k/1588161426952145` |
| Limited time only (specials) | `https://www.aldi.com.au/products/limited-time-only/k/1588161420755352` |

**IGA**

| Type | URL |
|------|-----|
| Browse all | `https://www.igashop.com.au/` |

**Priority:** Always check on-special / specials / limited-time / super-saver pages first — they directly affect which recipes are cheapest today.

### Price Integrity Rules — CRITICAL

**Never estimate or fabricate prices. Only use prices you have personally verified by fetching the store's website.**

- If you cannot retrieve a verified price for an ingredient (page blocked, product not found, etc.), **leave the price blank** in the recipe and note it as "price unavailable — check in-store"
- Do NOT fall back to guessing, approximating from memory, or using "typical" prices
- A recipe with some blank prices is far better than a recipe with fabricated prices that mislead the user
- Always use Chrome (via browser tool) to load grocery store pages and extract real prices — do not assume prices from training data

### Price Caching — Same-Day Reuse

Before fetching any store's prices, check whether `prices/prices_YYYY-MM-DD.csv` already exists for today:

- If the CSV exists and already contains rows for a given store, **do not re-fetch that store's pages** — use the cached prices directly
- This avoids redundant web requests when the skill is run multiple times in one day
- If a store is missing from today's CSV entirely, fetch it and append the results
- Receipt-verified prices (source field contains `receipt-`) are always trusted and never need re-fetching

### Price Saving Rules

When prices are fetched and verified, **always save them** to a CSV file:

**Path:** `prices/prices_YYYY-MM-DD.csv`

**CSV columns:**
```
date,store,product_name,product_id,category,unit,unit_size,price_aud,price_per_100g,on_special,special_price_aud,source_url
```

- `date` — ISO format (e.g. `2026-03-22`)
- `store` — `Coles`, `Woolworths`, `ALDI`, `IGA`, etc.
- `product_id` — store's unique SKU or slug (e.g. `coles-sku-12345` or URL slug)
- `unit` — `kg`, `g`, `L`, `mL`, `each`, `pack`
- `price_per_100g` — normalised cost for comparison (calculate from price and unit size)
- `on_special` — `true` or `false`
- `special_price_aud` — original price if on special, else blank
- `source_url` — exact URL the price was retrieved from (or `receipt-STORE-YYYY-MM-DD` for receipt-verified prices)

Always append to the file for today's date if it already exists (do not duplicate rows by product_id).

---

## Health Optimisation Targets

Every recipe and meal plan must holistically target ALL of the following health benefits:

| Goal | Key Nutrients / Foods |
|------|----------------------|
| **Cardiovascular health** | Omega-3s, potassium, magnesium, fibre, polyphenols, oats, salmon, nuts, legumes |
| **Low blood pressure** | Potassium, magnesium, calcium, **low sodium (target &lt;1,500mg/day total)**, beetroot, leafy greens, garlic |
| **Anti-cancer properties** | Cruciferous vegetables (broccoli, cabbage, kale), lycopene (tomatoes), allicin (garlic/onion), antioxidants (vitamins C, E, selenium) |
| **Lower LDL cholesterol** | Soluble fibre (oats, legumes, barley), plant sterols, healthy fats (olive oil, avocado, nuts), omega-3s |
| **Low sugar** | Avoid refined sugars, minimise high-GI ingredients, favour whole foods |
| **Low glycaemic index (GI)** | Legumes, wholegrains, vegetables, sweet potato over white potato, brown rice over white rice |

---

## Recipe Generation Rules

### Three Meals Per Day Philosophy
When generating a daily meal set, think **holistically across all 3 meals**:
- Breakfast + Lunch + Dinner together must cover the broadest possible spectrum of nutrition
- No single meal needs to be "complete" — the trio should work as a system
- Minimise total ingredient cost across all 3 meals (look for ingredient overlap to reduce waste)
- Order recipes by cheapest + broadest nutrient density first

### Recipe Requirements
Each recipe must include:
- **Name** with health benefit focus (e.g. "Heart-Healthy Oat & Banana Breakfast")
- **Per-ingredient cost** (from today's scraped prices, store + price clearly shown)
- **Total meal cost**
- **Macronutrient breakdown** (protein, carbs, fat, fibre, sugar)
- **Micronutrient coverage** — list which vitamins and minerals this meal provides and at what % of RDI
- **Health benefits** — list which of the 6 targets above this meal addresses and how
- **GI rating** (Low / Medium / High)
- **Cooking instructions** — simple, minimal equipment, beginner-friendly
- **Prep time** and **cook time**

### Ingredient Selection Principles
- Always prefer the cheapest option that meets the nutritional goal (check on-specials first)
- Prioritise whole foods over processed
- Use legumes, eggs, canned fish, oats, frozen vegetables, and seasonal produce as budget superfoods
- Avoid expensive items unless they provide irreplaceable nutritional value
- Consider bulk buys when price-per-100g is significantly lower (note this in the recipe)

### Dietary Requirement — Low Sodium (STRICT)
The user requires a **low sodium diet** to support healthy blood pressure. This is a hard constraint:
- **Daily sodium target: ≤ 1,500mg** (well below the Australian AI of 2,000mg)
- **Per-meal target: ≤ 500mg sodium** — always calculate and display sodium per meal
- **Avoid high-sodium ingredients:** processed meats (bacon, ham, salami), regular soy sauce, stock cubes, canned goods with added salt, pickled foods, most condiments, table salt additions
- **Prefer:** fresh or frozen vegetables (unsalted), dried legumes (no added salt), fresh herbs and spices for flavour instead of salt
- **Swap high-sodium for low-sodium versions:**
  - Low-sodium soy sauce (e.g. Kikkoman Less Salt) instead of regular
  - No-added-salt canned tomatoes instead of regular canned tomatoes
  - No-added-salt canned legumes (chickpeas, lentils) instead of regular
  - Canned fish in water (lower sodium than brine) where possible
- **Flag sodium content clearly** in every recipe — show mg per meal and % of daily 1,500mg target
- **Boost potassium** alongside reducing sodium — the K:Na ratio is as important as sodium alone; prioritise bananas, sweet potato, spinach, lentils, salmon
- Use lemon juice, fresh garlic, herbs (parsley, basil, coriander), spices (cumin, turmeric, paprika, pepper) and vinegar as flavour alternatives to salt

### Dietary Requirement — Lactose Intolerance (STRICT)
The user is **severely lactose intolerant**. This is a hard constraint that overrides all other ingredient choices:
- **NEVER use** regular milk, regular yoghurt, regular cheese, cream, butter, or any standard dairy product
- **ALWAYS use** lactose-free alternatives when dairy nutrition is needed:
  - Lactose-free milk (e.g. Zymil, ALDI Lact-Free) instead of regular milk
  - Lactose-free yoghurt (e.g. Jalna Lactose Free, Zymil) instead of regular yoghurt
  - Lactose-free cheese where cheese is called for
  - Plant-based milks (oat milk, soy milk, almond milk) are also acceptable
- Hard aged cheeses (parmesan, cheddar, pecorino) are naturally very low in lactose and **may** be used in small quantities as a flavour addition only — note this explicitly in the recipe
- Canned fish (salmon, sardines, tuna) remains the best budget source of calcium — prefer these over dairy
- Eggs, leafy greens, broccoli, and canned salmon (with bones) should be prioritised as non-dairy calcium sources
- Always label lactose-free products clearly in the ingredient list (e.g. "Lactose-free milk — Zymil")

---

## HTML Output — Static Website

Claude generates static HTML files for this repo. GitHub Pages serves the website.

### Design Reference
See `Screenshot.png` for the target aesthetic:
- **Dark background** — near-black (`#1a1a1a` / `#0f0f0f`)
- **Card-style layout** — rounded corners, subtle borders, floating card feel
- **Accent colour** — bright teal/green (similar to `#4ecca3` or `#00e5a0`)
- **Typography** — clean sans-serif, bold headings, good contrast
- **Dark mode first** — everything designed for dark backgrounds
- No CSS frameworks needed — clean vanilla CSS

### File Structure
```
/                          ← repo root
├── index.html             ← homepage (links to all daily meal plans)
├── recipes/
│   ├── YYYY-MM-DD.html    ← daily meal plan (generated by skill)
│   └── ...
├── prices/
│   └── prices_YYYY-MM-DD.csv
├── AFCD Release 3 - Nutrient profiles.xlsx
└── Screenshot.png
```

### Homepage (`index.html`)
- Lists all generated daily meal plans (most recent first)
- Shows total daily cost, headline health benefits, and date for each entry
- Links to each `recipes/YYYY-MM-DD.html`
- Must be updated every time a new recipe page is generated

### Daily Recipe Page (`recipes/YYYY-MM-DD.html`)
- Shows **all meals generated for that day** — the skill may be run multiple times in a day, and each run appends a new set of 3 meals to the same file
- Each meal displayed as a card with all required recipe fields
- Nutrient coverage shown as visual progress bars (HTML/CSS only, no JS charts)
- Shopping list section at the bottom (all ingredients consolidated across all meals in the file, with store + price)
- "Back to all meals" link to `index.html`
- If the file already exists when the skill runs, **append** the new meal cards after the existing ones — do not overwrite

---

## Recipe Variation — Longitudinal Nutrition

Before generating new recipes, **always review previously generated recipe files** in `recipes/`:
- Identify which nutrients, food groups, and ingredients have been heavily featured
- Deliberately rotate to underrepresented ingredients and nutrients
- The goal is that over a week or month of generated plans, the user receives complete and varied nutrition across all food groups
- Track patterns: if the last 3 plans all featured oats for breakfast, suggest a savoury egg alternative

---

## Skill Command

A custom Claude skill exists at `.claude/commands/generate-recipes.md`.

Run it with: `/generate-recipes`

This skill will:
1. Check today's prices CSV — reuse cached prices for any store already fetched today
2. Fetch prices (via Chrome) from stores not yet cached — save real verified prices only, never estimates
3. Review the AFCD nutrient database
4. Review all previously generated recipe HTML files in `recipes/` for variety/rotation
5. If today's recipe file already exists, read the existing meals and account for their nutrition holistically
6. Generate 3 new optimised meals that complement today's existing meals (or provide maximum breadth if none exist yet)
7. Append the new meal cards to `recipes/YYYY-MM-DD.html` (create if new, append if exists)
8. Update `index.html`

---

## Australian Context

- All prices in **AUD ($)**
- All nutritional RDIs based on **Australian Nutrient Reference Values (NRVs)** from the NHMRC
- Ingredient names should use **Australian terminology** (e.g. "capsicum" not "bell pepper", "rockmelon" not "cantaloupe", "zucchini" not "courgette", "coriander" not "cilantro", "eggplant" not "aubergine")
- Serving sizes calibrated for **Australian adults** (standard reference: male 70kg, female 60kg, or note if different)
- Seasonal produce awareness: note if an ingredient is in/out of season in Sydney
