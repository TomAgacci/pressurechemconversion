# ============================
# PRESSURE-CHEM DEVIATION ENGINE (REAL CHEMISTRY)
# ============================

from collections import Counter

# --- Utility: parse chemical formulas into element counts ---
def parse_formula(formula):
    import re
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    counts = Counter()
    for element, num in tokens:
        counts[element] += int(num) if num else 1
    return counts

# --- Deviation computation ---
def deviation_map(reactants, products):
    # Sum reactant atoms
    total_react = Counter()
    for r in reactants:
        total_react += parse_formula(r)

    # Sum product atoms
    total_prod = Counter()
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
    return deviations

# --- Example: ethanol formation from glucose ---
reactants = ["C6H12O6"]          # glucose
products  = ["C2H6O", "C2H6O",   # 2 ethanol
             "CO2", "CO2"]       # 2 CO2

deviations = deviation_map(reactants, products)

# --- Print deviation table ---
for element, info in deviations.items():
    print(f"{element}: {info}")
