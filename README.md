# Support Dashboard — digiQC

Gleap bug tracking dashboard for the digiQC support team. View, manage, and close bugs reported through Gleap.

## Dashboard

**[Open Dashboard](https://hathi-jigar.github.io/support-dashboard/)**

## How It Works

1. Gleap bug is raised → GitHub Issue auto-created in `digiqc-hq/product-management` with label `🔵 Open`
2. Support opens dashboard → sees all Gleap bugs
3. Support clicks a bug → fills in org, user, phone, platform, version, solution
4. Data saved as structured comment on the GitHub Issue
5. Support clicks "Close Bug" → issue closes in product-management → label changes from `🔵 Open` to `🔒 Closed from Support`
6. TAT auto-calculated (close date - report date)

## What Happens on Close

When support closes a bug from the dashboard:
- GitHub Issue state → `closed`
- Label `🔵 Open` → **removed**
- Label `🔒 Closed from Support` → **added**
- Project board status → syncs automatically via workflow
- Support meta (org, solution, handled by) → saved as comment on the issue

## Bug Fields

| Field | Source | Editable? |
|-------|--------|-----------|
| Title | Auto from Gleap issue | No |
| Status | Auto from issue state | Close button |
| Reported By | Auto from Gleap (`**Reported by:**`) | No |
| Email | Auto from Gleap (mailto link) | No |
| Phone Number | Support fills | Yes |
| Organisation | Support fills | Yes (dropdown + add new) |
| User Name | Auto from Gleap (defaults to Reported By), support can edit | Yes |
| Platform | Auto from Gleap (`systemName` / `sdkType`), support can override | Yes (Android / iOS / Web) |
| Version | Auto from Gleap (`releaseVersionNumber`), support can override | Yes |
| Report Date | Auto from issue created_at | No |
| Close Date | Auto from issue closed_at | No |
| Screenshot | Auto from Gleap (image URL in body) | No |
| Description | Auto from Gleap issue body | No |
| Solution Given | Support writes | Yes |
| TAT | Auto calculated (close date - report date) | No |
| Handled By | Auto from logged-in support user | No |

## Labels

| Label | Meaning | Set by |
|-------|---------|--------|
| `🔵 Open` | Bug is open and unresolved | Auto (Gleap workflow) |
| `🔒 Closed from Support` | Bug closed by support team via dashboard | Dashboard (on close) |
| `🔒 Closed through Gleap` | Bug closed directly in Gleap | Gleap workflow |
| `Gleap` | Bug originated from Gleap | Auto (Gleap workflow) |
| `Bug` | Issue type is a bug | Auto (Gleap workflow) |

## Setup (one-time per support member)

1. Create a GitHub account (free)
2. Generate a PAT token with `repo` scope
3. Open the dashboard link
4. Enter your name + token → saved in browser
