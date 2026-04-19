# CO-03 — Shelf Life Compliance Checker

## Purpose

Validate that stock being shipped meets the minimum remaining shelf life requirement for the destination country at the time of arrival.

---

## Owner

**Primary:** GxP Compliance Manager

---

## When This Skill Is Used

- During compliance validation of shipping requests
- After batch selection (SI-10) to confirm selected batches meet shelf life rules

---

## Inputs

1. **Shelf life requirements** — From DI-08 (minimum remaining shelf life by country)
2. **Batch selection** — From SI-10 (selected batches with expiry dates)
3. **Shipping windows** — From LT-02 (expected arrival dates)

---

## Steps

1. **For each batch being shipped**, calculate remaining shelf life at expected arrival date
2. **Compare to destination country's minimum requirement**
3. **Classify**:
   - **COMPLIANT** — Remaining shelf life meets or exceeds the minimum
   - **NON-COMPLIANT** — Remaining shelf life is below the minimum
4. **Flag non-compliant batches** with details on the gap
5. **Produce shelf life compliance report**

---

## Output

- Shelf life compliance status for each batch/country combination
- Remaining shelf life at arrival vs. minimum required
- Non-compliant batches with gap details
- Recommendations (select different batch, expedite shipment, etc.)

---

## Notes

- Shelf life compliance is a patient safety issue — non-compliant stock must not be shipped
- This skill works closely with SI-03 (Expiry Profile Analyser) and SI-10 (Batch Selection Advisor)
