# SRQ-04 Search-to-Contract and Metrics Design

## Goal

Prove that the stable `search_agama.py` output for the checked SRQ-04 representative passage can be used directly in an answer that satisfies the citation contract, then align public test metrics with the resulting full-suite baseline.

## Scope

- Add one integration-style regression test that obtains `《雜阿含經》(T02n0099)` line 147 through `search_agama()` and passes its returned citation into `build_answer_contract_review()` for SRQ-04.
- Update the root README and changelog from the stale 277-test baseline to the expected 285-test baseline after the new single test passes in the full suite.
- Preserve search ranking, CLI output, provider routes, platform status, and scholarly-collation boundaries.

## Behavior

The test searches the exact checked line text, selects the match with `T02n0099` and line 147, and constructs a bounded answer containing search scope, representative status, CBETA, the returned citation, and pending-collation wording. The SRQ-04 contract must pass without copying a hand-written anchor. This covers the source-to-answer citation handoff without calling a provider.

## Validation and Rollback

Run the new test, SRQ-04 contract tests, Agama search tests, package-metadata tests, strict repository checks, and full pytest. Rollback is confined to deleting the additive test and restoring two metric strings; no corpus or runtime evidence changes are involved.
