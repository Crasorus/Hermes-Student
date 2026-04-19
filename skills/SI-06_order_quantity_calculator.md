# SI-06 — Order Quantity Calculator

## Purpose

Calculate the optimal order quantity for each location that needs replenishment. This balances demand coverage, lead time, safety stock requirements, and order size constraints.

---

## Owner

**Primary:** Supply & Inventory Analyst

---

## When This Skill Is Used

- After SI-05 (Reorder Trigger Evaluator) identifies locations needing replenishment
- Produces the order quantities that feed into the supply plan

---

## Inputs

1. **Reorder triggers** — Output from SI-05 (locations that need orders)
2. **Demand forecast** — Forecasted consumption rates per location from DF-05
3. **Supply network** — Lead times from DI-06
4. **Policies** — Minimum and maximum order quantities, safety stock targets, maximum stock levels from DI-07
5. **Study configuration** — Pack sizes, shelf-life requirements, and review period
6. **Pipeline stock** — Stock on order or in transit per location (from SI-02 or DI-04)

---

## Steps

1. **For each location needing replenishment**, calculate:
   - **Demand during coverage period** = forecasted consumption rate (from DF-05) × (lead time + review period)
   - **Safety stock target** from policy
   - **Current stock on hand** at the location
   - **Stock on order** (in transit or pipeline stock already due to arrive)
   - **Order quantity** = demand during coverage period + safety stock target − current stock on hand − stock on order
2. **Apply constraints**:
   - Ensure quantity meets the **minimum order quantity**
   - Ensure quantity does not exceed the **maximum order quantity**
   - Check that the resulting stock position (current stock + stock on order + order quantity) does not exceed the **maximum stock level** — reduce quantity if it would
3. **Round up to pack sizes** — Round the quantity up to the nearest whole pack size to avoid shortfall
4. **Check shelf life** — Verify that ordered stock will remain within usable shelf life on arrival and through the expected consumption period; flag if not
5. **Identify the source** — Which manufacturing site or depot will fulfil the order
6. **Calculate required-by date**:
   - Required-by date = date current stock on hand is projected to reach the safety stock level
   - i.e., today + (current stock on hand − safety stock target) / daily consumption rate
7. **Produce order recommendations** — Quantity, source, destination, required-by date, and calculation rationale for each order

---

## Output

- Recommended order quantity for each location and item
- Source location for each order
- Required-by date (based on when stock will reach safety stock level)
- Rationale for each quantity (showing the calculation)

---

## Notes

- Order quantities should be right-sized — over-ordering creates waste (especially expiry risk in clinical supply), under-ordering creates patient risk
- Always round up to available pack sizes to avoid shortfall
- Pipeline stock must be accounted for to prevent systematic over-ordering
- The coverage period includes the review period because no new order can be placed until the next review cycle
- The order recommendations feed into the supply plan and ultimately into LT-06 (Shipping Request Generator)
