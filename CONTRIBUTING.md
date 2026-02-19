# Contributing

Thanks for contributing to PCA/CAE.

## How to contribute

1. Open an issue with context and expected behavior.
2. Submit a focused pull request.
3. Update tests/vectors for behavior changes.
4. Update `CHANGELOG.md`.

## For normative changes

Normative changes must include an RFC using `spec/PCA-RFC-TEMPLATE.md` and be consistent with `spec/` SSOT rules.

## Quality checks

```bash
cd reference/python
python -m pytest -q
ruff check .
```
