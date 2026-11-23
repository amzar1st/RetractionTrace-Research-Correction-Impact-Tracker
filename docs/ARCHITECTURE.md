# Evidence and consensus architecture

RetractionTrace addresses a trust gap between a publisher changing a source and a report author acknowledging which dependent claims need review. It records claim-specific judgments with citations and immutable evidence commitments. It never equates retraction with a proof of falsehood.

## Contract state

- `reports`: bounded registry of up to 200 reports, each with up to five claims and three distinct PLOS ONE papers. Reports carry owner, version, exact source passages, links, revision, and a SHA-256 commitment.
- `notices`: up to 20 unique publisher notice DOIs per report. Official JATS metadata must identify the supplied DOI, notice type, and target paper in `related-article`. Exact submitted excerpts must occur in the notice body. No arbitrary URLs or user-controlled hosts are fetched.
- `assessments`: one immutable record per report/notice pair. Findings, verified source document hashes, policy version and assessment commitment are stored.

Only a report's registering account can link sources, submit notices, or assess. Linking is a complete replacement before the first notice, after which report evidence is sealed. Changes require a new report version/ID. There is no admin setter, upgrade mechanism, fee collection, or value transfer. Reads are public; report contents are public.

## Notice verification

The leader fetches official PLOS JATS over HTTPS using a DOI-derived, fixed-host endpoint. It verifies the document's own article DOI, correction/retraction type, explicit target article metadata and exact notice excerpt. Validators fetch the same official source independently and compare normalized full notice body and type. Accepted body and publisher document SHA-256 are committed. Page errors fail the write; no user-submitted notice can replace official publisher evidence.

## Claim assessment

The leader independently fetches each registered source's current JATS document. It records contributor surnames and verifies every registered passage against normalized text. Missing or changed passages are marked unverified, not assumed true. The model sees pinned claims, explicit claim-source links, the verified official notice body, and live passage-match results. It proposes relation, independent remaining source IDs, exact citations, notice quote and explanation for every claim.

Validators rerun that entire fetch/model task independently. They validate proposed quotes against their own publisher checks and compare stable substantive fields: claim ID, changed-passage relationship, independently supporting source IDs, and cited source/passage IDs. Different wording of explanatory prose and quote lengths is permitted; semantic decisions cannot differ. Rejected proposals do not produce an assessment.

Exact substring checks prevent fabricated quotations. Linked-source checks prevent unrelated citations. Remaining support cannot be the corrected source and must be both linked and quoted. The MVP conservatively rejects independent-support assertions for shared contributor surnames or missing author metadata. The model must additionally consider whether evidence is copied, merely cites the changed study, or concerns a different tool/population. Author-name checks are a conservative filter, not proof of independent datasets.

## Status policy

| Relationship | Independent support remains | Result |
| --- | --- | --- |
| Changed material unrelated to linked claim | Any | UNAFFECTED |
| Claim has no link to changed paper | Any | UNAFFECTED for this notice |
| Changed/withdrawn material supports claim | Yes | SUPPORT_WEAKENED |
| Changed/withdrawn material supports claim | No | REVIEW_REQUIRED |
| Missing evidence or ambiguous relationship | Unknown | INSUFFICIENT_EVIDENCE |

Retractions forbid an UNRELATED relation for a linked claim. They prompt review or weakened support, never a `FALSE` finding. Status is derived deterministically, not chosen by the model. Aggregate claim status retains the most conservative existing assessment across registered notices in this order: UNAFFECTED < SUPPORT_WEAKENED < INSUFFICIENT_EVIDENCE < REVIEW_REQUIRED. Unassessed notices prevent an aggregate UNAFFECTED result. Newer unrelated notices cannot erase older review flags.

## Frontend and signing boundary

The frontend uses a pinned `genlayer-js` client for finalized `readContract` calls and transaction receipt polling. Studio owns its built-in account on a separate origin and does not expose a supported cross-origin signing provider. The app prepares exact ABI inputs, imports the already deployed contract into Studio, and tracks the resulting transaction hash. It never reads, stores, or transmits private keys, and does not pretend that a signing handoff is an injected wallet connection.

Pending and ACCEPTED remain provisional. FINALIZED requires a successful execution receipt before success is reported. Reverts, VM errors, canceled transactions, timeouts and undetermined outcomes are distinct. A polling timeout means tracking may resume with the same hash; it does not invite duplicate submission. Finalized contract state is loaded independently from the receipt.

## MVP boundaries

PLOS ONE only, no automatic correction discovery, no PDFs/spreadsheets parsed, no evidence beyond supplied passages, no clinical recommendations, no on-chain funds, no automatic decisions about a claim's truth. A supplied source version label is descriptive; a quote missing from the current publisher document cannot authenticate an old version. Historical verification requires a future authenticated archive adapter. Studionet can reset. Independent validator execution is not a guarantee that models or providers are statistically independent or correct.

## Continued development

Add Crossref/Crossmark notice discovery with authenticated publisher adapters; verify archived source versions; model dataset and author provenance explicitly; add permissionless notice proposals with owner review; expand bounded graphs across multiple reports; add human-reviewed resolution records that preserve the original judgment; migrate to a persistent testnet after compatibility/fee profiling.

Receipt identity is decoded using the SDK calldata decoder: contract recipient, method, and exact prepared ABI arguments must match before the UI can mark the state verified. A corresponding finalized getter then checks the postcondition. This prevents an unrelated finalized transaction from being treated as the user's prepared action.
