# PCA-TEST v1 (PL)

Definiuje testy zgodności T1-T13.

## Zestaw testów

- **T1 PC replay**: powtórzony nonce/session MUST uruchomić `RC_PC_REPLAY`.
- **T2 Domain separation**: błędna etykieta hash MUST uruchomić `RC_DOMAIN_SEPARATION`.
- **T3 Constraints mismatch**: niezgodny constraints digest/version MUST uruchomić `RC_CONSTRAINTS_MISMATCH`.
- **T4 Reason stability**: identyczne błędne wejścia MUST dawać ten sam reason code.
- **T5 TOCTOU**: dryf stanu między check/use MUST uruchomić `RC_TOCTOU`.
- **T6 Effective time**: wykonanie poza oknem MUST uruchomić `RC_EFFECTIVE_TIME`.
- **T7 Optional field omission**: kanonizacja MUST nie serializować nieobecnych pól opcjonalnych.
- **T8 Conflict detector**: zadeklarowany konflikt MUST uruchomić `RC_CONFLICT`.
- **T9 Merkle proof**: niepoprawny proof MUST uruchomić `RC_MERKLE_PROOF`.
- **T10 BRS gate**: przekroczenie progu MUST uruchomić `RC_BRS_GATE`.
- **T11 OOD tripwire**: flaga OOD MUST uruchomić `RC_OOD_TRIPWIRE`.
- **T12 Disclosure budget**: przekroczenie budżetu MUST uruchomić `RC_DISCLOSURE_BUDGET`.
- **T13 Positive path**: poprawne wykonanie MUST zwrócić `EXECUTE` + `RC_OK`.

## Kryteria akceptacji

- Wszystkie wymagane testy przechodzą dla deklarowanego profilu zgodności.
- Skróty są deterministyczne pomiędzy ponownymi uruchomieniami.
- Werdykty błędów są deterministyczne i uzasadnione.
