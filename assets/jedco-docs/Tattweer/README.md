# Tattweer Program — Mock Application Dataset

**TRAINING USE ONLY — بيانات وهمية للتدريب**

This folder contains 8 mock applications for the JEDCO Tattweer (تطوير) program,
designed to cover all key review scenarios for automated pipeline testing.

## Application Index

| File | ID | Company | Sector | Expected Decision | Scenario |
|------|----|---------|--------|-------------------|----------|
| TW-2026-001.txt | TW-2026-001 | Al-Barakah Food Industries | Food Processing | **APPROVE** | Strong eligible application |
| TW-2026-002.txt | TW-2026-002 | Nour Digital Solutions | IT / Software | **APPROVE** | Eligible — tech sector |
| TW-2026-003.txt | TW-2026-003 | Al-Majd Furniture Factory | Wood / Furniture | **REJECT** | Operating license expires during project |
| TW-2026-004.txt | TW-2026-004 | Petra Crafts & Exports | Handicrafts | **REJECT** | Company less than 2 years old |
| TW-2026-005.txt | TW-2026-005 | Jordan Clean Energy Corp | Manufacturing | **REJECT** | Public shareholding company (excluded) |
| TW-2026-006.txt | TW-2026-006 | Blessed Olive Oil | Agri-food | **INCOMPLETE** | Missing audited financial statements |
| TW-2026-007.txt | TW-2026-007 | Al-Nakheel Plastics | Plastics / Packaging | **REJECT** | Previously benefited from Tattweer |
| TW-2026-008.txt | TW-2026-008 | Hashemite Medical Supplies | Medical Devices | **REVIEW** | Borderline — weak financials, marginal grant amount |

## Key Review Rules (for automation)

1. **Company age** — Must be ≥ 2 years at application date
2. **Operating license** — Must remain valid for the full 12-month implementation window
3. **Ownership** — Public shareholding companies (شركة مساهمة عامة) are excluded
4. **Repeat beneficiary** — Cannot have benefited from the same program before
5. **Grant ceiling** — Maximum 50,000 JOD, funding ratio 70% JEDCO / 30% applicant
6. **Required documents** — All 6 documents must be present for COMPLETE status

## Cycle
Tattweer Spring Cycle 2026 — March / April 2026
