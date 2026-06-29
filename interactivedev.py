# ============================================================
# INTERACTIVE PRESSURE-CHEM DEVIATION ENGINE (REAL CHEMISTRY)
# ============================================================

from collections import Counter
import re

# --- Parse chemical formula into element counts ---
def parse_formula(formula):
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    counts = Counter()
    for element, num in tokens:
        counts[element] += int(num) if num else 1
    return counts

# --- Compute deviation map ---
def deviation_map(reactants, products):
    total_react = Counter()
    total_prod = Counter()

    # Sum reactants
    for r in reactants:
        total_react += parse_formula(r)

    # Sum products
    for p in products:
        total_prod += parse_formula(p)

    # Compute deviations
    deviations = {}
    for element in total_react:
        R = total_react[element]
        P = total_prod.get(element, 0)
        deviations[element] = {
            "reactant_total": R,
            "product_total": P,
            "fraction_to_products": P / R if R > 0 else 0,
            "fraction_remaining": (R - P) / R if R > 0 else 0
        }
    return deviations, total_react, total_prod

# --- Interactive loop ---
def run_engine():
    print("\n=== Pressure-Chem Deviation Engine ===")
    print("Enter chemical formulas like C6H12O6, CO2, C2H6O, SiO2, H2O")
    print("Separate multiple molecules with commas.\n")

    while True:
        react_in = input("Reactants: ").strip()
        prod_in  = input("Products: ").strip()

        reactants = [r.strip() for r in react_in.split(",") if r.strip()]
        products  = [p.strip() for p in prod_in.split(",") if p.strip()]

        deviations, total_react, total_prod = deviation_map(reactants, products)

        print("\n--- Element Totals ---")
        print("Reactants:", dict(total_react))
        print("Products :", dict(total_prod))

        print("\n--- Deviations ---")
        for element, info in deviations.items():
            print(f"{element}:")
            print(f"  Reactant total      = {info['reactant_total']}")
            print(f"  Product total       = {info['product_total']}")
            print(f"  Fraction to product = {info['fraction_to_products']:.3f}")
            print(f"  Fraction remaining  = {info['fraction_remaining']:.3f}")

        # Conservation check
        print("\n--- Conservation Check ---")
        for element in total_react:
            R = total_react[element]
            P = total_prod.get(element, 0)
            if R != P:
                print(f"WARNING: {element} not conserved (Reactants={R}, Products={P})")
        print("\n")

        again = input("Run another deviation? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting deviation engine.")
            break

# --- Start the engine ---
if __name__ == "__main__":
    run_engine()
