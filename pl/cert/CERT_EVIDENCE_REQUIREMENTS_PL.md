# Wymagania dowodowe certyfikacji (PL)

## Minimalny pakiet

1. Konfiguracja środowiska i wersje komponentów.
2. Logi wykonania z decyzjami `EXECUTE` / `FALLBACK`.
3. Mapowanie przypadków testowych T1-T13 do wyników.
4. Procedury reprodukcji i ponownego uruchomienia.

## Kryteria odrzucenia

- Niedeterministyczny reason code (`RC_REASON_UNSTABLE`).
- Brak fail-closed dla TOCTOU.
- Niespójna implementacja etykiet, np. `STATEv1`.
