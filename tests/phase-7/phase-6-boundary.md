# Phase 6 → Phase 7 Boundary Tests

- [ ] Retrieval accepts normalized language from Conversation Understanding.
- [ ] Retrieval accepts normalized intent from Conversation Understanding.
- [ ] Retrieval does not require raw customer text when normalized intent/context are available.
- [ ] `customer_id_reference` is never treated as customer profile data.
- [ ] Retrieval returns evidence metadata with factual results.
- [ ] Missing evidence produces `insufficient_evidence`.
- [ ] Conflicting eligible sources produce `conflict`.
- [ ] Expired sources cannot support current price, promotion, or stock claims.
