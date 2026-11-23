# Reviewer walkthrough

1. Open the public RetractionTrace website. The default workspace reads the deployed contract's finalized state, rather than local fixture outcomes.
2. Review the sample report: five claim inputs and three cited papers. The report is illustrative; its claims are not clinical recommendations. The PLOS correction and three source publications are real.
3. Select C1 to inspect the original scoring macro dependency and the official correction excerpt. The notice says the macro contains errors.
4. Select C2/C3 to inspect why the correction does not change the article's reported analysis or the structure of its summary measures. The notice explicitly states the erroneous macro was not used in analysis.
5. Select C4 to see a claim linked only to a different paper. It is outside this notice's dependency graph.
6. Select C5 to see an intentionally unverifiable input passage. Its absence from publisher evidence must produce insufficient evidence, never a fabricated citation.
7. Open Evidence library. Inspect each exact committed passage and the live publisher-match flags recorded in the assessment.
8. Open Audit trail. Verify report, notice, source document and assessment hashes. Follow transaction links to inspect successful execution and the validator round.
9. Open Transaction workspace. To create your own report, choose `register_report`, use a new ID, and edit its claims and source passages. Prepare the arguments, open the deployed contract in Studio, and send with the built-in account in Normal (Full Consensus) mode. Do not redeploy.
10. Paste the resulting hash into RetractionTrace. Pending and accepted transactions remain provisional. After finalized successful execution, the app verifies recipient, decoded arguments and resulting finalized state against the prepared call.
11. Continue with `link_claim_sources`, then `submit_notice`, then `assess_impact`. Load your report by ID in the report reader. The same built-in account must own and write that report.

For a live correction, the official publisher JATS must identify a correction/retraction and the target DOI through related-article metadata. Arbitrary text, an unrelated notice DOI, an unsupported publisher, and a quote that is absent from the official notice are rejected.

## Status coverage

The real published correction demonstrates affected macro claims, unaffected article claims, an unrelated paper, and unverifiable evidence. It does not establish independent support for the exact original macro and should not be forced into SUPPORT_WEAKENED. Independent-support and retraction branches are covered by clearly identified mocked-boundary tests; this document does not claim those two scenarios were validated against a real retraction or independent replication on the network.
