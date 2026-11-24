# Validation report

Date: 24 November 2026. Original live transactions executed on 23 November; deployed source and assessment rechecked on 24 November. Network: GenLayer Studionet (61999).

## Automated

`npm test`: **35 passed** (17 Python, 18 JavaScript). `npm run build`: production build passed.

Contract tests exercise real contract methods behind explicit in-memory web/model/consensus doubles: bounds, unsupported DOI/host rejection, duplicate IDs, owner authorization, invalid links, publisher DOI/type/target checks, evidence sealing, immutable assessments, exact quote checks, independent validator disagreement, self-support exclusion, contributor-overlap rejection, independent-support status, conservative history aggregation and missing sources/passages.

JavaScript tests cover pending/accepted states, execution failure despite FINALIZED, the observed FINISHED_WITH_RETURN and FINISHED_WITH_ERROR receipt formats, leader receipts, polling progression, abort, timeout/resume semantics, RPC errors, hash validation, HTML escaping, exact ABI inputs, recipient/argument matching and finalized-state effect checks.

## Live GenVM and network

The exact deployed source passed live schema introspection. Its fetched contract code matches the source file byte for byte. Deployment and all four write methods executed using GenLayer Studio's built-in account in Normal (Full Consensus), with no MetaMask and no extracted private keys.

The verified real correction is DOI `10.1371/journal.pone.0199469`, targeting `10.1371/journal.pone.0192773`. Notice validation fetched official publisher JATS. Assessment fetched all three source papers; four genuine excerpt passages matched the publisher and the deliberately invented fifth passage did not. All five expected claim statuses match finalized state. Quotes match their committed passages and notice body.

The network selected five participants per round and reached quorum. Receipts include AGREE votes and IDLE entries for work canceled after quorum; the evidence does **not** claim all five completed or that model providers are independent.

A deliberately repeated assessment was rejected with `ValueError: Notice missing or already assessed`. Its transaction finalized with an execution error; the original assessment hash remained unchanged. This distinguishes protocol finality from successful contract execution.

Exact hashes, receipt status, execution result, NORMAL mode, votes and links are in [the manifest](../public/verification.json). The read-only `npm run verify:live` script can reproduce the checks while this Studionet state remains available.

## Browser QA

Verified in the provided desktop Chrome browser:

- Correct project name, logo, configured deployed contract and live finalized report.
- Overview counters show 5 claims, 1 review required, 3 unaffected, 1 evidence gap.
- Claim selection shows the exact notice and supporting source passages.
- Text search and status filter select C5; its detail view records insufficient evidence without fabricated citations.
- Evidence library shows publisher-match flags and document hashes.
- Audit export emits a downloadable JSON audit record.
- All four methods prepare exact Studio ABI arguments; copy works.
- Active assessment tracking progresses to successful finalization and verifies recipient, arguments and state.
- Failed duplicate assessment is shown as FAILED even though its protocol status is FINALIZED.
- No application runtime error was observed in these checks. Browser-extension metadata messages were outside the app.

Responsive styles are included. Mobile-device browser testing was not performed. Provider/network outages and every real-world correction/retraction type are not exhaustively tested. No production security audit is claimed.

## Startup and RPC efficiency follow-up

The UI initializes before loading its fixture and no longer blocks module completion on network work. Fixture loading has a 15-second deadline. Rate-limit errors name the upstream limit and instruct the user to wait before retrying. For a single registered notice, the already fetched committed findings provide the complete aggregate, reducing a report refresh from nine RPC calls to four. Multiple-notice reports still use authoritative contract aggregation. Three additional tests cover no notice, pending notice, committed single-notice history, and multi-notice fallback.
