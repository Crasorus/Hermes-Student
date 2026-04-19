# SI-01 — Stock Position Calculator

## Purpose

Calculate current stock on hand by depot, country, treatment arm, and item. This skill produces the complete inventory snapshot that all other supply skills depend on.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- At the start of any supply planning workflow
- Provides the foundation for SI-02 through SI-10

---

## Inputs

1. **Parsed ERP data** — Output from DI-04 (stock on hand, batch details, in-transit shipments, open orders)
2. **Supply network** — Output from DI-06 (depot locations, country assignments)

---

## Steps

1. **Aggregate stock on hand** by depot, country, treatment arm, and item
2. **Include in-transit quantities** — Stock that has been shipped but not yet received
3. **Include open orders** — Stock that has been ordered but not yet shipped
4. **Calculate total available** — Stock on hand + in-transit + on order
5. **Produce inventory snapshot** — Complete position by location and item

---

## Output

- Stock on hand by depot, country, arm, and item
- Batch-level detail preserved (lot number, expiry date, quantity per batch) for downstream use by SI-03 and SI-10
- In-transit quantities by destination
- Open order quantities by destination
- Total available (on hand + in transit + on order) by location
- Snapshot date

---

## Notes

- This is a point-in-time snapshot — it shows the position as of the data drop date
- The stock position feeds into SI-02 (Weeks of Supply), SI-04 (Safety Stock Checker), and SI-07 (Supply Gap Identifier)
