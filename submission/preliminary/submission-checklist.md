# Preliminary Round Submission Checklist

Checklist status: Updated after PPTX deck generation  
Submission channel: Official UMHackathon website only

## 1. Deliverables Package

| Deliverable | Working source | Final export | Status |
| --- | --- | --- | --- |
| Product Requirement Document (PRD) | [PRD draft](./PRD.md) | PDF | In progress |
| System Analysis Document (SAD) | [SAD draft](./SAD.md) | PDF | In progress |
| Code repository | Public GitHub repository | URL | https://github.com/khaisernong/ASEM-Talint |
| Quality Assurance Testing Document (QATD) | [QATD draft](./QATD.md) | PDF | In progress |
| Preliminary round pitch deck | [Generated PPTX deck](./ASEM-Talint-10-minute-presentation.pptx), [pitch deck outline](./pitch-deck-outline.md), [pitch deck script](./pitch-deck-script.md), and [deck generator](./generate_pitch_deck.py) | PPTX or PDF deck | PPTX generated; ready for visual review/export |
| 10-minute pitching video with prototype demonstration | [Video demo runbook](./video-demo-runbook.md) | MP4 or MOV | In progress |

## 2. Content Gate Before Exporting PDFs

- confirm Z.AI GLM remains explicit in the product narrative, architecture narrative, and demo narrative
- confirm optional ILMU references are clearly labeled non-judge-path
- confirm every external article, handbook, data source, template, or borrowed idea is cited visibly
- confirm unsupported numbers are either removed or marked `UNSPECIFIED` or `ASSUMPTION`
- confirm the PRD, SAD, QATD, deck, and video all describe the same shipped workflow

## 3. Repository Gate

- confirm the public repository URL still points to the submitted snapshot
- verify no secrets, tokens, or private links are committed
- verify README setup instructions still match the current code path
- verify the repository shows Z.AI as the primary reasoning path
- verify tests pass on the branch or snapshot being submitted

## 4. Demo and Video Gate

- confirm the recorded environment is using the judged Z.AI route
- confirm `/health` shows the live Z.AI route ready before recording
- confirm the video length is 10 minutes or less
- confirm the demo includes a working prototype interaction, not only slides
- confirm the recorded screen does not expose secrets or unrelated personal data

## 5. Final Submission Gate

- export the PRD, SAD, and QATD to PDF
- verify [ASEM-Talint-10-minute-presentation.pptx](./ASEM-Talint-10-minute-presentation.pptx) opens cleanly
- verify the video file plays correctly in MP4 or MOV format
- verify all final file names are human-readable and consistent
- verify citations remain visible after export to PDF
- verify the public repository link is reachable without additional private access
- have one team member perform a final cross-check because only one official submission attempt is allowed

## 6. Submission Rule Reminder

- submission must be made through the official UMHackathon website only
- each team receives one final submission attempt
- after final submission, changes are not allowed
- do not automate the final website submission

## 7. Recommended Final Manual Sequence

1. Freeze the repository snapshot and rerun tests.
2. Export PRD, SAD, and QATD to PDF.
3. Review or revise [ASEM-Talint-10-minute-presentation.pptx](./ASEM-Talint-10-minute-presentation.pptx), then export a PDF version if needed.
4. Check every citation and public link one last time.
5. Record the 10-minute demo video against the same repository snapshot and deck.
6. Upload the full package to the official UMHackathon website once.

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [README preliminary submission section](../../README.md)
- [PRD draft](./PRD.md)
- [SAD draft](./SAD.md)
- [QATD draft](./QATD.md)
