# Preliminary Round Submission Checklist

Checklist status: Working draft  
Submission channel: Official UMHackathon website only

## 1. Deliverables Package

| Deliverable | Working source | Final export | Status |
| --- | --- | --- | --- |
| Product Requirement Document (PRD) | [PRD draft](./PRD.md) | PDF | In progress |
| System Analysis Document (SAD) | [SAD draft](./SAD.md) | PDF | In progress |
| Code repository | Public GitHub or approved source link | URL | `UNSPECIFIED` public link |
| Quality Assurance Testing Document (QATD) | [QATD draft](./QATD.md) | PDF | In progress |
| Preliminary round pitch deck | [Pitch deck outline](./pitch-deck-outline.md) and [pitch deck script](./pitch-deck-script.md) | PPTX or PDF deck | In progress |
| 10-minute pitching video with prototype demonstration | [Video demo runbook](./video-demo-runbook.md) | MP4 or MOV | In progress |

## 2. Content Gate Before Exporting PDFs

- confirm Z.AI GLM remains explicit in the product narrative, architecture narrative, and demo narrative
- confirm optional ILMU references are clearly labeled non-judge-path
- confirm every external article, handbook, data source, template, or borrowed idea is cited visibly
- confirm unsupported numbers are either removed or marked `UNSPECIFIED` or `ASSUMPTION`
- confirm the PRD, SAD, QATD, deck, and video all describe the same shipped workflow

## 3. Repository Gate

- create or confirm the public repository URL
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
- verify the pitch deck file opens cleanly
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
3. Finalize the deck and record the 10-minute demo video.
4. Check every citation and public link one last time.
5. Upload the full package to the official UMHackathon website once.

## References

- [UMHackathon 2026 Official Handbook](../../UMHackathon%202026%20Official%20Handbook.pdf)
- [README preliminary submission section](../../README.md)
- [PRD draft](./PRD.md)
- [SAD draft](./SAD.md)
- [QATD draft](./QATD.md)
