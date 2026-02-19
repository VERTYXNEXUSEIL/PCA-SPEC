# Conformance Checklists

## Bronze
- [ ] Deterministic canonical encoding implemented.
- [ ] Domain-separated digest labels implemented.
- [ ] Constraints version/digest/effective-time enforced.
- [ ] Mandatory fallback with reason codes.
- [ ] Pass required baseline vectors.

## Silver
- [ ] Bronze complete.
- [ ] Merkle root/proof support implemented.
- [ ] Conflict detector path tested.
- [ ] Pass vectors through T10.

## Gold
- [ ] Silver complete.
- [ ] OOD tripwire implemented.
- [ ] Disclosure-budget enforcement implemented.
- [ ] Full T1-T13 vector conformance report published.
