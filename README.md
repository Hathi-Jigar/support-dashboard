# Support Dashboard — digiQC

Gleap bug tracking dashboard for the digiQC support team. View, manage, and close bugs reported through Gleap.

## Dashboard

**[Open Dashboard](https://hathi-jigar.github.io/support-dashboard/)**

## How It Works

1. Gleap bug is raised → GitHub Issue auto-created in `digiqc-hq/product-management`
2. Support opens dashboard → sees all Gleap bugs
3. Support clicks a bug → fills in org, user, platform, version, solution
4. Data saved as structured comment on the GitHub Issue
5. Support clicks "Close Bug" → issue closes in product-management
6. TAT auto-calculated (close date - report date)

## Bug Fields

| Field | Source | Editable? |
|-------|--------|-----------|
| Title | Auto from Gleap issue | No |
| Status | Auto from issue state | Close button |
| Organisation | Support fills | Yes (dropdown + add new) |
| User Name | Support fills | Yes |
| Platform | Support selects | Yes (Android / iOS / Web) |
| Version | Support fills | Yes |
| Report Date | Auto from issue | No |
| Close Date | Auto when closed | No |
| Screenshot | Auto from Gleap | No |
| Description | Auto from Gleap | No |
| Solution Given | Support writes | Yes |
| TAT | Auto calculated | No |
| Handled By | Auto from logged-in user | No |

## Setup (one-time per support member)

1. Create a GitHub account (free)
2. Generate a PAT token with `repo` scope
3. Open the dashboard link
4. Enter your name + token → saved in browser
