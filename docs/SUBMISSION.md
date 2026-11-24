# GenLayer Project Explorer submission

## Identity

- **Project name:** RetractionTrace
- **Subtitle:** Research Correction Impact Tracker
- **Suggested topic tags:** DeSci, research integrity, evidence provenance (choose the nearest available Explorer categories).
- **Logo:** [512 × 512 PNG](../public/logo.png), under 2 MB.
- **Application date:** 2026-11-24
- **Website:** https://retractiontrace.wirymink515.chatgpt.site
- **Repository:** https://github.com/amzar1st/RetractionTrace-Research-Correction-Impact-Tracker
- **Network:** GenLayer Studionet, chain ID 61999
- **Contract:** [0xCf5d49Ac30E8cc703683F38e0De0A50F492C795d](https://explorer-studio.genlayer.com/address/0xCf5d49Ac30E8cc703683F38e0De0A50F492C795d)

## Short description

RetractionTrace traces official research corrections and retractions to the individual claims that cite the changed evidence. GenLayer validators independently verify publisher notices, check exact source passages, and assess whether each claim is unaffected, needs review, retains independent support, or lacks sufficient evidence. Versioned on-chain records preserve the judgment and supporting evidence.

## Problem and target users

Research funders, DAO reviewers and research teams need to know when an upstream correction changes the evidence supporting a report. A blanket retraction flag misses unaffected claims and can imply falsehood without justification. RetractionTrace records claim-level dependencies and makes the impact decision auditable.

## What is built

A deployed Intelligent Contract and public frontend supporting report registration, exact claim-source passage links, official publisher-notice verification, semantic impact assessment, claim status/history, source-match flags and audit exports. The transaction workspace prepares exact ABI inputs for Studio's built-in account, tracks the returned hash, distinguishes consensus/finality from execution success, matches recipient and arguments, and verifies finalized state. No MetaMask or private-key extraction is required.

## Why GenLayer is central

The key decision is semantic: does a changed passage bear on this particular claim, and does independent supporting evidence remain? Ordinary deterministic code cannot resolve that relationship. Each validator independently fetches publisher evidence and derives an assessment. The equivalence principle compares the relationship, independently supporting source IDs and controlling cited passage IDs; exact quote checks and deterministic status rules constrain the result. Consensus changes the contract state that the frontend reads.

## Verified demonstration

The sample report contains five claims and three real PLOS ONE papers. Official correction DOI 10.1371/journal.pone.0199469 identifies errors in a supporting macro while explicitly preserving the article's analysis. Finalized outcomes: C1 REVIEW_REQUIRED; C2/C3/C4 UNAFFECTED; C5 INSUFFICIENT_EVIDENCE. C5 is intentionally unverifiable. These are illustrative report inputs, not clinical advice or endorsed research findings.

All four write methods and deployment finalized successfully in NORMAL consensus mode. A duplicate assessment intentionally failed and preserved the original record. The frontend was tested against both successful and failed transactions. There are 35 passing automated tests, successful live GenVM schema validation, deployed-source equality, finalized-state checks and reviewer screenshots.

## Transaction evidence

| Operation | Execution result | Evidence |
| --- | --- | --- |
| deploy | FINISHED_WITH_RETURN | [Transaction](https://explorer-studio.genlayer.com/tx/0x18688a042be78a30286cf900d244a8b10f5e0d799e96697b98f069d517760220) |
| register_report | FINISHED_WITH_RETURN | [Transaction](https://explorer-studio.genlayer.com/tx/0x8ab2552f9e7571fbec701b0f53ca4e1b4b0758c7cf312ceca43cdb02f473b5ec) |
| link_claim_sources | FINISHED_WITH_RETURN | [Transaction](https://explorer-studio.genlayer.com/tx/0xd1f01eaa60317fa22f8473a5d9994aae00a6a0bd8fd2d71225e3c878a8953ba5) |
| submit_notice | FINISHED_WITH_RETURN | [Transaction](https://explorer-studio.genlayer.com/tx/0x9bec90564fe8f114cc6b9e37619d6b3f64a21ab0447895c8137b8ecfe113e4d4) |
| assess_impact | FINISHED_WITH_RETURN | [Transaction](https://explorer-studio.genlayer.com/tx/0xc33d59d3645f78ebe7aaf0e15b1f8f90f2651190759c76b22a842b10932a1ef8) |
| assess_impact_duplicate_rejection | FINISHED_WITH_ERROR | [Transaction](https://explorer-studio.genlayer.com/tx/0xb6f219cd26d43f39caacdedd8bfd933f6aa8c627901d6c1c267837d6801ee25f) |

## Evidence commitments

- Source SHA-256: `db2e06c8f6c3558d3139ecd8e9585ce62e0f52e31ea5f370f62af66c8cc37708`
- Report hash: `0c7f72d0c61681e8dfde96895bc1709c36a2162de70e0a2c3bc3f47e9910ec26`
- Notice document SHA-256: `71d448e31584e432aa0d0857f4b98122b3995d613bec11536619975535fced41`
- Assessment hash: `9f65c42829ac3d5f716008264445fb788b0baa30b84e729a6f9bf654bcdc7d0b`
- Full evidence: [verification manifest](../public/verification.json), [finalized state snapshot](verified-state.json), [validation report](TESTING.md).
- Screenshots: [overview](screenshots/overview.jpg), [claim evidence](screenshots/claim-evidence.jpg).
- Review steps: [demo walkthrough](DEMO.md).

## Boundaries and continued development

PLOS ONE only in this MVP; up to five claims and three cited papers per report. Notices are manually registered. Studionet can reset. Registered version labels do not authenticate an unavailable historical file. Independent-support and retraction paths have mocked-boundary test coverage; a real retraction/replication transaction is not claimed. Consensus is not a guarantee of scientific correctness or model independence. No production security audit is claimed.

Next steps are authenticated source-version archives, Crossref/Crossmark discovery, dataset provenance, reviewed resolution records and a persistent-network deployment after compatibility and fee profiling.

This package prepares the Project Explorer application; it does not claim the application was submitted or accepted.

## Immutable reviewed implementation

- Implementation commit: [`f4146d3f9cf531f4772161bca73b761367ac8751`](https://github.com/amzar1st/RetractionTrace-Research-Correction-Impact-Tracker/commit/f4146d3f9cf531f4772161bca73b761367ac8751)
- Exact deployed source: [retractiontrace.py](https://github.com/amzar1st/RetractionTrace-Research-Correction-Impact-Tracker/blob/f4146d3f9cf531f4772161bca73b761367ac8751/contracts/retractiontrace.py)
- Test and evidence snapshot: [reviewed tree](https://github.com/amzar1st/RetractionTrace-Research-Correction-Impact-Tracker/tree/f4146d3f9cf531f4772161bca73b761367ac8751)

Subsequent documentation/provenance commits do not change the verified contract source.
