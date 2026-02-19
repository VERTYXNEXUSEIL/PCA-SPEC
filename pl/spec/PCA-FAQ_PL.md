# PCA FAQ (PL)

## Czym PCA/CAE różni się od guardrails?

Guardrails są często filtrami runtime. PCA/CAE dodaje kryptograficzne powiązanie między intencją planu, constraints polityki i kontrolami wykonania, tworząc audytowalne, deterministyczne dowody.

## Co oznacza TOCTOU w tym kontekście?

TOCTOU oznacza, że akcja przeszła kontrole na jednym obserwowanym stanie, ale została użyta później na stanie, który istotnie się zmienił. PCA/CAE wymaga fail-closed fallback po wykryciu takiego dryfu.

## Dlaczego kodowanie kanoniczne jest ważne?

Bez kodowania kanonicznego semantycznie równoważny JSON może dawać różne skróty w różnych implementacjach. PCA/CAE wymaga kanonizacji, aby zagwarantować odtwarzalne skróty i interoperacyjną certyfikację.
