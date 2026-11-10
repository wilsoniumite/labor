# nipa_fiscal.py — what the United States taxes and what it pays out, by kind: the national-accounts series behind the
# draft's Section 9 ("what the United States does now"), taken from BEA's annual flat file into a small stored table.
#
#   receipts   NIPA Table 3.1: current tax receipts, by kind, and contributions for government social insurance
#   detail     NIPA Table 3.5: sales taxes and recurrent taxes on immovable property (property taxes)
#   benefits   NIPA Table 3.12: government social benefits to persons, the largest programmes
#
# Needs NipaDataA.txt in the gitignored cache (python3 code/one_basis.py --pull fetches it). The stored table is what
# everything else reads, so nothing downstream needs the BEA file.
# Run from provisioning/:  python3 code/nipa_fiscal.py      writes data/nipa_fiscal.csv and data/nipa_fiscal_vintage.json

import hashlib
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "paths", "code"))
import chains as ch  # noqa: E402

SERIES = {                                  # BEA series code: (column, BEA's label)
    "W054RC": ("tax_receipts", "Current tax receipts"),
    "W055RC": ("personal_taxes", "Personal current taxes"),
    "W056RC": ("production_taxes", "Taxes on production and imports"),
    "W025RC": ("corporate_taxes", "Taxes on corporate income, payable by corporations and other enterprises"),
    "W008RC": ("taxes_from_abroad", "Taxes from the rest of the world"),
    "W782RC": ("contributions", "Contributions for government social insurance"),
    "B248RC": ("sales_taxes", "State and local sales taxes"),
    "LA000355": ("property_taxes", "Recurrent taxes on immovable property"),
    "A063RC": ("benefits", "Government social benefits to persons"),
    "W823RC": ("social_security", "Social security"),
    "W824RC": ("medicare", "Medicare"),
    "W729RC": ("medicaid", "Medicaid"),
    "A1589C": ("unemployment", "Unemployment insurance"),
    "A1594C": ("veterans", "Veterans' benefits"),
    "TRP600": ("snap", "Supplemental Nutrition Assistance Program"),
    "W811RC": ("refundable_credits", "Refundable tax credits"),
}
YEARS = range(2000, 2025)


def extract():
    fp = os.path.join(ch.CACHE, "NipaDataA.txt")
    raw = ch.nipa_flat(fp, list(SERIES))
    missing = [c for c in SERIES if c not in raw]
    if missing:
        sys.exit(f"not in NipaDataA.txt: {missing}")
    table = pd.DataFrame({SERIES[c][0]: raw[c] for c in SERIES}).loc[lambda d: d.index.isin(YEARS)] / 1e3   # $mn to $bn
    table.index.name = "year"
    vintage = dict(file="NipaDataA.txt", bytes=os.path.getsize(fp), sha256_16=hashlib.sha256(open(fp, "rb").read()).hexdigest()[:16],
                   series={c: dict(column=k, label=label) for c, (k, label) in SERIES.items()})
    return table, vintage


def stored():
    """The stored table, $bn, by year."""
    return pd.read_csv(os.path.join(ROOT, "data", "nipa_fiscal.csv")).set_index("year")


if __name__ == "__main__":
    table, vintage = extract()
    table.to_csv(os.path.join(ROOT, "data", "nipa_fiscal.csv"))
    json.dump(vintage, open(os.path.join(ROOT, "data", "nipa_fiscal_vintage.json"), "w"), indent=1)
    r = table.loc[2023]
    total = r.tax_receipts + r.contributions
    print("2023, $bn: taxes and contributions %.0f" % total)
    for k in ("personal_taxes", "contributions", "production_taxes", "sales_taxes", "property_taxes", "corporate_taxes", "taxes_from_abroad"):
        print("  %-20s %7.0f  %.3f" % (k, r[k], r[k] / total))
    print("government social benefits to persons %.0f" % r.benefits)
    for k in ("social_security", "medicare", "medicaid", "unemployment", "veterans", "snap", "refundable_credits"):
        print("  %-20s %7.0f  %.3f" % (k, r[k], r[k] / r.benefits))
