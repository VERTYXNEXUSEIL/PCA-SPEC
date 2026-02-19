# PCA-SPEC v1.0 (Normatywny, PL)

## 1. Status

Ten dokument definiuje normatywny standard techniczny v1.0 dla Proof-Carrying Autonomy (PCA) / Certified Agentic Execution (CAE).

## 2. Język zgodności

Słowa kluczowe **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** oraz **MAY** mają charakter normatywny.

## 3. Obiekty główne

- **Action IR (AIR)**: kanoniczna reprezentacja pośrednia planowanej akcji.
- **Constraints**: obwiednia wykonania sterowana polityką, identyfikowana wersją i skrótem.
- **Plan Certificate (PC)**: podpisany lub atestowalny obiekt wiążący dowody planowania z kontrolami wykonania.
- **Evidence Capsule**: ustrukturyzowana obwiednia provenance zawierająca dowody.

## 4. Kodowanie kanoniczne

Implementacje MUST kanonizować JSON przed haszowaniem:

1. Kodowanie UTF-8.
2. Klucze obiektów sortowane leksykograficznie.
3. Brak wartości numerycznych NaN i Infinity.
4. Numeryczne `-0` znormalizowane do `0`.
5. Pola opcjonalne nieobecne w danych źródłowych MUST być pomijane (nie serializowane jako `null`), chyba że schemat wymaga jawnej nullable.

## 5. Haszowanie z separacją domen

Wszystkie skróty MUST używać SHA-256 na `label || ":" || canonical_bytes` z etykietami:

`STATEv1`, `GOALv1`, `CONSv1`, `POLv1`, `CFGv1`, `STEPv1`, `PLANv1`, `PCv1`, `AIRv1`.

## 6. Budowa skrótów

### 6.1 Skrót kroku

`step_digest_i = H("STEPv1", {state_digest, goal_digest, constraints_digest, policy_digest, config_digest, air_digest})`

### 6.2 Skrót planu (liniowy)

`plan_digest = H("PLANv1", {step_digest_1, ..., step_digest_n})`

Implementacje MAY dodatkowo wyliczać korzenie Merkle dla `step_digest_i`; jeżeli są obecne, reguły Merkle MUST być udokumentowane i deterministyczne.

### 6.3 Skrót PC

`pc_digest = H("PCv1", canonical_pc_without_signature_fields)`

Pola podpisu lub atestacji MUST NOT wpływać na `pc_digest`.

## 7. Wiązanie constraints

PC MUST zawierać:

- `constraints_version_id`
- `constraints_digest`
- `effective_time` (granice przedziału RFC3339)

Wykonanie MUST odrzucać niezgodną wersję/skrót oraz znaczniki czasu spoza okna.

## 8. Protokół certyfikowanego wykonania

1. Ponownie oblicz `pc_digest`.
2. Zweryfikuj wersję i skrót constraints.
3. Zweryfikuj poprawność `effective_time`.
4. Oceń kontrole konfliktów i tripwire.
5. Zwróć deterministyczny werdykt i reason code.

Jeżeli którekolwiek obowiązkowe sprawdzenie zakończy się błędem, wykonawca MUST zwrócić `decision = "FALLBACK"` i dołączyć stabilny reason code z `PCA-RC-v1`.

## 9. Wymagania TOCTOU i fallback

Wykonawcy MUST wykrywać istotny dryf stanu pomiędzy asercjami z czasu planowania a obserwacjami z czasu wykonania. Przy dryfie wykonanie MUST przejść fail-closed do fallback.

## 10. Reason codes

Reason codes są normatywnymi identyfikatorami i po publikacji MUST pozostać stabilne. Patrz `PCA-RC-v1.md`.

## 11. Profile zgodności

- **Bronze**: liniowy skrót planu, obowiązkowe kontrole, reason codes.
- **Silver**: Bronze + wsparcie Merkle + zgodność wektorowa T1–T10.
- **Gold**: Silver + OOD tripwire + disclosure budget + pełne T1–T13.

## 12. Harness testowy

Implementacje deklarujące zgodność MUST uruchamiać `PCA-TEST v1` i publikować dowody pass/fail.
