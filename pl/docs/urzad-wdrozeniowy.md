# Urząd wdrożeniowy (PL)

Dokument opisuje minimalny „urząd wdrożeniowy” dla organizacji wdrażającej PCA/CAE.

## Role

- **Właściciel standardu**: utrzymuje zgodność z PCA-SPEC.
- **Właściciel operacji**: monitoruje decyzje `EXECUTE`/`FALLBACK` i reason codes.
- **Audytor**: okresowo weryfikuje deterministyczność i integralność dowodów.

## Artefakty obowiązkowe

- Rejestr wersji `constraints_version_id`.
- Rejestr reason codes i trendów.
- Harmonogram uruchamiania testów T1-T13.
- Procedura reagowania na `RC_UNKNOWN`.
