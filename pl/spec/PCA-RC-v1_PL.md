# PCA Reason Codes v1 (PL)

## Reguły stabilności

1. Identyfikatory kodów są niezmienne.
2. Semantyka może być doprecyzowana, ale nie może być odwrócona.
3. Kody wycofane pozostają zarezerwowane i MUST NOT być przypisane ponownie.

## Słownik

- `RC_OK`: Weryfikacja i kontrole wykonania zakończone powodzeniem.
- `RC_PC_REPLAY`: Wykryto odtworzenie (replay) PC.
- `RC_DOMAIN_SEPARATION`: Niezgodność skrótu z separacją domen.
- `RC_CONSTRAINTS_MISMATCH`: Niezgodność skrótu constraints lub wersji.
- `RC_REASON_UNSTABLE`: Wykryto niedeterministyczne generowanie reason code.
- `RC_TOCTOU`: Naruszenie dryfu time-of-check/time-of-use.
- `RC_EFFECTIVE_TIME`: `effective_time` poza dopuszczalnym oknem.
- `RC_CONFLICT`: Detektor konfliktu zablokował akcję.
- `RC_MERKLE_PROOF`: Niepoprawny dowód Merkle.
- `RC_BRS_GATE`: Bramka Behavioral Risk Score odrzuciła żądanie.
- `RC_OOD_TRIPWIRE`: Uruchomiono tripwire out-of-distribution.
- `RC_DISCLOSURE_BUDGET`: Przekroczony disclosure budget.
- `RC_UNKNOWN`: Fallback dla nieskategoryzowanej, ale deterministycznej awarii.
