# 🥗 NutriCents

**The Cost-to-Nutrition Optimizer**

NutriCents is a data-driven web platform that helps users eat healthier **for the lowest possible cost**.
It combines nutrition science, grocery pricing, and optimization algorithms to answer a simple but powerful question:

> *“What is the cheapest way to meet my daily nutritional needs?”*

---

## 🚀 Features

### 🧠 Core Optimization Engine

* **Cost Per Nutrient Leaderboard**
  Discover foods ranked by nutritional return on investment:

  * Protein per $1
  * Iron per $1
  * Cheapest complete protein combinations

* **Real-Time Supermarket Pricing**
  Syncs with major supermarkets (e.g. Coles, Woolworths, Aldi) to:

  * Track price changes
  * Automatically reprioritize recipes based on current deals

* **100% RDI Daily Planner**
  Generates a full-day meal plan that:

  * Meets 100% of recommended daily intake (RDI)
  * Minimizes total cost using optimization techniques (e.g. linear programming)

---

### 🍳 Smart Cooking & Kitchen Tools

* **Use My Pantry (Reverse Recipe Search)**
  Input what you already have → get optimized recipes to reduce food waste.

* **Smart Ingredient Swapper**
  Automatically suggests cheaper or equivalent alternatives without sacrificing nutrition.

* **Zero-Waste Meal Chaining**
  Plans meals across multiple days to ensure:

  * All purchased ingredients are used
  * Nothing goes to waste

---

### 👤 Personalization & Health

* **Family Batch Scaling**
  Scale recipes intelligently:

  * Adjusts quantities AND purchasing strategy
  * Recommends bulk buying when cheaper per unit

* **Dietary “Cheat Codes”**
  Budget-focused filters:

  * Cheapest Vegan
  * High Protein (Muscle Building)
  * Heart Healthy
  * Under $X per meal

* **Micro-Nutrient Visuals**
  Each recipe shows:

  * % of daily vitamins & minerals
  * Clear, visual nutrient coverage

---

### 🛒 Shopping Optimization

* **Aisle-Optimized Shopping Lists**
  Organized by supermarket layout to:

  * Save time
  * Reduce impulse purchases

* **Click & Collect Cart Export (Planned)**
  Send optimized carts directly to online grocery platforms.

* **Half-Price Stockpile Alerts**
  Get notified when staple foods hit deep discounts:

  * Buy strategically
  * Reduce long-term food costs

---

### 🌍 Community & Insights

* **$2 Meal Challenge**
  Community-submitted ultra-budget recipes:

  * Verified for nutrition + cost
  * Ranked by taste and value

* **Inflation Impact Tracker**
  See how much you save vs average grocery spend:

  * Monthly savings insights
  * Personal cost trends

---

## 🏗️ Tech Stack (Example)

> Adapt this section based on your actual implementation.

* **Frontend:** React / Docusaurus / Vanilla JS
* **Backend:** Python (Flask or Django)
* **Database:** DynamoDB / PostgreSQL
* **Hosting:** AWS (S3, API Gateway, Lambda)
* **Data Sources:**

  * Nutrition datasets (e.g. USDA / AUSNUT)
  * Supermarket pricing APIs / scraping

---

## 🧮 How It Works

NutriCents uses optimization algorithms to balance:

* Nutritional requirements (macros + micronutrients)
* Food prices (dynamic, real-time)
* User constraints (diet, budget, preferences)

At its core, the system solves a constrained optimization problem:

```
Minimize: Total Cost
Subject to:
- Nutrient requirements ≥ RDI
- Dietary constraints satisfied
- Ingredient availability & pricing
```

---

## 📦 Getting Started

```bash
# Clone the repo
git clone https://github.com/your-username/nutricents.git

# Navigate into the project
cd nutricents

# Install dependencies
npm install
# or
pip install -r requirements.txt

# Run locally
npm run dev
# or
python app.py
```

---

## 🛠️ Roadmap

* [ ] Supermarket API integrations (AU focus)
* [ ] Advanced linear programming engine
* [ ] Mobile-first UI
* [ ] User accounts & saved meal plans
* [ ] Cart export integrations
* [ ] Gamification & leaderboards
* [ ] AI-powered recipe generation

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📜 License

MIT License – feel free to use, modify, and build upon this project.

---

## 💡 Vision

NutriCents exists to make **healthy eating accessible during a cost-of-living crisis**.

By combining:

* financial optimization
* nutrition science
* real-world pricing

…it empowers people to make smarter food decisions—without sacrificing health.

