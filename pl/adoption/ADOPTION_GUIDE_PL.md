# Przewodnik adopcji PCA/CAE (PL)

## Etap 1 — Inwentaryzacja

- Zidentyfikuj przepływy, w których decyzja `EXECUTE`/`FALLBACK` ma znaczenie regulacyjne.
- Zmapuj źródła stanu używane do wyliczenia `state_digest`.

## Etap 2 — Integracja techniczna

- Wprowadź kanonizację JSON zgodną z `PCA-SPEC v1.0`.
- Dodaj wyliczanie `pc_digest` i walidację `constraints_digest`.
- Ustal obsługę `effective_time`.

## Etap 3 — Operacjonalizacja

- Rejestruj reason codes (`RC_*`) i decyzje wykonawcze.
- Uruchamiaj testy conformance i publikuj dowody.
