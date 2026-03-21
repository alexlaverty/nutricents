#!/usr/bin/env python3
"""
AFCD Query Tool — CLI for querying the Australian Food Composition Database.

Usage:
    python scripts/afcd_query.py search <query>
    python scripts/afcd_query.py profile <food_name>
    python scripts/afcd_query.py key-nutrients <food_name>
    python scripts/afcd_query.py top-by-nutrient <nutrient_name> [--n=10]
    python scripts/afcd_query.py find-column <query>
    python scripts/afcd_query.py compare <food1> <food2> [<food3> ...]
    python scripts/afcd_query.py value-for-money <food_name> <price_per_100g>
    python scripts/afcd_query.py list-foods [--filter=<query>]

Examples:
    python scripts/afcd_query.py search "oats rolled"
    python scripts/afcd_query.py profile "Oats, rolled, uncooked"
    python scripts/afcd_query.py key-nutrients "salmon pink canned"
    python scripts/afcd_query.py top-by-nutrient "Iron (mg)" --n=15
    python scripts/afcd_query.py top-by-nutrient "selenium"
    python scripts/afcd_query.py find-column "omega"
    python scripts/afcd_query.py compare "oats" "brown rice" "sweet potato"
    python scripts/afcd_query.py value-for-money "oats" 0.45
    python scripts/afcd_query.py list-foods --filter=lentil
"""

import argparse
import json
import sys
from pathlib import Path

# Allow running from repo root or scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.afcd_lib import AFCDDatabase, KEY_NUTRIENTS, kcal_from_kj


def cmd_search(db: AFCDDatabase, args: argparse.Namespace):
    query = " ".join(args.query)
    results = db.search(query, max_results=args.n)
    if results.empty:
        print(f"No foods found matching: '{query}'")
        return
    print(f"\nSearch results for '{query}' ({len(results)} matches):\n")
    print(results[["Public Food Key", "Food Name"]].to_string(index=False))


def cmd_profile(db: AFCDDatabase, args: argparse.Namespace):
    food_name = " ".join(args.food_name)
    row = db.get_profile(food_name)
    if row is None:
        print(f"No food found matching: '{food_name}'")
        print("Tip: use 'search' command to find the exact name.")
        return

    print(f"\n{'='*70}")
    print(f"FULL PROFILE: {row['Food Name']}")
    print(f"Public Food Key: {row['Public Food Key']}")
    print(f"{'='*70}\n")

    for col in db.columns:
        val = row.get(col)
        if col in ("Public Food Key", "Classification", "Derivation", "Food Name"):
            continue
        if val is not None and str(val) not in ("nan", "None", ""):
            print(f"  {col:<60} {val}")


def cmd_key_nutrients(db: AFCDDatabase, args: argparse.Namespace):
    food_name = " ".join(args.food_name)
    profile = db.get_key_nutrients(food_name)
    if profile is None:
        print(f"No food found matching: '{food_name}'")
        return

    print(f"\n{'='*70}")
    print(f"KEY NUTRIENTS: {profile['food_name']}")
    print(f"Public Food Key: {profile['public_food_key']}")
    print(f"{'='*70}")
    print(f"\n{'Nutrient':<45} {'Value':>10}  {'% RDI (M)':>10}")
    print(f"{'-'*70}")

    for nutrient, data in profile["nutrients"].items():
        val = data["value"]
        pct = data["pct_rdi_male"]
        if val is None:
            continue
        val_str = f"{val:.2f} {data['unit']}"
        pct_str = f"{pct:.1f}%" if pct is not None else "N/A"
        print(f"  {nutrient:<43} {val_str:>12}  {pct_str:>10}")

    # Energy in kcal too
    energy_kj = profile["nutrients"].get("Energy (kJ)", {}).get("value")
    if energy_kj:
        print(f"\n  Energy: {energy_kj:.0f} kJ = {kcal_from_kj(energy_kj):.0f} kcal")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(profile, indent=2))


def cmd_top_by_nutrient(db: AFCDDatabase, args: argparse.Namespace):
    nutrient_query = " ".join(args.nutrient)

    # Try to resolve fuzzy column name
    if nutrient_query not in db.columns:
        matches = db.find_nutrient_column(nutrient_query)
        if not matches:
            print(f"No column matching '{nutrient_query}'. Use 'find-column' to search.")
            return
        if len(matches) == 1:
            col = matches[0]
        else:
            print(f"Multiple columns match '{nutrient_query}':")
            for i, m in enumerate(matches):
                print(f"  [{i}] {m}")
            print("\nUsing first match. Use exact column name to specify.")
            col = matches[0]
    else:
        col = nutrient_query

    results = db.top_by_nutrient(col, n=args.n)
    if results.empty:
        print("No results.")
        return

    col_display = col.replace("\n", " ").strip()
    print(f"\nTop {args.n} foods by: {col_display}\n")
    print(f"{'Food Name':<55} {col_display[:22]:>22}")
    print(f"{'-'*80}")
    for _, row in results.iterrows():
        val = row[col]
        name = str(row["Food Name"])[:54]
        print(f"  {name:<54} {val:>22.2f}")


def cmd_find_column(db: AFCDDatabase, args: argparse.Namespace):
    query = " ".join(args.query)
    matches = db.find_nutrient_column(query)
    if not matches:
        print(f"No columns matching '{query}'.")
    else:
        print(f"\nColumns matching '{query}':\n")
        for m in matches:
            print(f"  {m}")


def cmd_compare(db: AFCDDatabase, args: argparse.Namespace):
    foods = args.foods
    result = db.compare(foods)
    if result.empty:
        print("No matching foods found.")
        return

    print(f"\nComparison (per 100g):\n")
    # Show just the key nutrients that have any data
    available = [c for c in KEY_NUTRIENTS if c in result.index]
    display = result.loc[[c for c in available if c in result.index]]
    display.index = [KEY_NUTRIENTS[c] for c in display.index]
    print(display.to_string())


def cmd_value_for_money(db: AFCDDatabase, args: argparse.Namespace):
    food_name = " ".join(args.food_name[:-1]) if len(args.food_name) > 1 else args.food_name[0]
    price = args.price

    result = db.nutrient_value_per_dollar(food_name, price)
    if result is None:
        print(f"No food found matching: '{food_name}'")
        return

    print(f"\n{'='*70}")
    print(f"VALUE FOR MONEY: {result['food_name']}")
    print(f"Price: ${price:.2f} per 100g")
    print(f"{'='*70}")
    print(f"\n{'Nutrient':<45} {'Per 100g':>12}  {'Per $1':>10}  {'% RDI/$':>10}")
    print(f"{'-'*80}")

    for nutrient, data in result["nutrients_per_dollar"].items():
        val_str = f"{data['per_100g']:.2f} {data['unit']}"
        per_dollar = f"{data['per_dollar']:.3f}"
        pct_per_dollar = f"{data['pct_rdi_per_dollar']:.1f}%" if data["pct_rdi_per_dollar"] is not None else "N/A"
        print(f"  {nutrient:<43} {val_str:>13}  {per_dollar:>10}  {pct_per_dollar:>10}")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(result, indent=2))


def cmd_list_foods(db: AFCDDatabase, args: argparse.Namespace):
    foods = db.list_all_foods()
    if args.filter:
        q = args.filter.lower()
        foods = [f for f in foods if q in f.lower()]
    print(f"\n{len(foods)} foods found:\n")
    for f in foods:
        print(f"  {f}")


def main():
    parser = argparse.ArgumentParser(
        description="Query the Australian Food Composition Database (AFCD) Release 3.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = subparsers.add_parser("search", help="Search foods by name keywords")
    p_search.add_argument("query", nargs="+", help="Search terms (space-separated keywords)")
    p_search.add_argument("--n", type=int, default=20, help="Max results (default 20)")

    # profile
    p_profile = subparsers.add_parser("profile", help="Full nutrient profile for a food")
    p_profile.add_argument("food_name", nargs="+", help="Food name (substring match)")

    # key-nutrients
    p_key = subparsers.add_parser("key-nutrients", help="Key nutrients summary with % RDI")
    p_key.add_argument("food_name", nargs="+", help="Food name (substring match)")
    p_key.add_argument("--json", action="store_true", help="Also output JSON")

    # top-by-nutrient
    p_top = subparsers.add_parser("top-by-nutrient", help="Rank all foods by a nutrient")
    p_top.add_argument("nutrient", nargs="+", help="Nutrient column name (or partial match)")
    p_top.add_argument("--n", type=int, default=10, help="Number of results (default 10)")

    # find-column
    p_col = subparsers.add_parser("find-column", help="Search column names in the database")
    p_col.add_argument("query", nargs="+", help="Search terms")

    # compare
    p_compare = subparsers.add_parser("compare", help="Side-by-side key nutrient comparison")
    p_compare.add_argument("foods", nargs="+", help="Food names to compare (space-separated list, quote multi-word names)")

    # value-for-money
    p_vfm = subparsers.add_parser("value-for-money", help="Nutrient density per dollar")
    p_vfm.add_argument("food_name", nargs="+", help="Food name, with last arg being price")
    p_vfm.add_argument("price", type=float, help="Price in AUD per 100g")
    p_vfm.add_argument("--json", action="store_true", help="Also output JSON")

    # list-foods
    p_list = subparsers.add_parser("list-foods", help="List all foods in the database")
    p_list.add_argument("--filter", type=str, default=None, help="Filter by substring")

    args = parser.parse_args()

    db = AFCDDatabase()
    print(f"[AFCD] Loaded {db.food_count} foods from database.", file=sys.stderr)

    dispatch = {
        "search": cmd_search,
        "profile": cmd_profile,
        "key-nutrients": cmd_key_nutrients,
        "top-by-nutrient": cmd_top_by_nutrient,
        "find-column": cmd_find_column,
        "compare": cmd_compare,
        "value-for-money": cmd_value_for_money,
        "list-foods": cmd_list_foods,
    }

    dispatch[args.command](db, args)


if __name__ == "__main__":
    main()
