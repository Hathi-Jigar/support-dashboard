# Support Dashboard — digiQC

Gleap bug tracking, onboarding, and task management dashboard for the digiQC support team.

**[Open Dashboard](https://hathi-jigar.github.io/support-dashboard/)**

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SUPPORT DASHBOARD                             │
│                  (Single-page HTML + Vanilla JS)                     │
│                                                                      │
│   ┌──────────────┐  ┌───────────────────┐  ┌──────────────────┐     │
│   │  Bug Tracker  │  │ Onboarding Tracker│  │  Task Tracker    │     │
│   │              │  │                   │  │                  │     │
│   │  Gleap Bugs  │  │  Client Lifecycle │  │  Internal Tasks  │     │
│   │  from GitHub │  │  Intro → Go-Live  │  │  for Support     │     │
│   └──────┬───────┘  └────────┬──────────┘  └────────┬─────────┘     │
│          │                   │                      │               │
└──────────┼───────────────────┼──────────────────────┼───────────────┘
           │                   │                      │
           ▼                   ▼                      ▼
┌─────────────────┐  ┌─────────────────┐    ┌─────────────────┐
│  GitHub Issues   │  │ onboarding.json │    │   tasks.json    │
│  digiqc-hq/      │  │ (GitHub repo)   │    │  (GitHub repo)  │
│  product-mgmt    │  └─────────────────┘    └─────────────────┘
└────────┬────────┘
         │
    ┌────┴────┐
    │  Gleap  │  ← Client bug reports auto-create GitHub Issues
    └─────────┘
```

### Data Flow

```
Client reports bug in Gleap
        │
        ▼
Gleap auto-creates GitHub Issue (label: Gleap)
        │
        ▼
GitHub Action adds 🔵 Open label + Bug type     ← gleap-bug-label.yml
        │
        ▼
Support opens dashboard → sees bug in table
        │
        ▼
Support fills: Org, User, Phone, Platform, Version, Solution
        │
        ▼
Data saved as structured comment on GitHub Issue  ← <!-- SUPPORT-META --> marker
        │
        ▼
Support clicks "Close Bug"
        │
        ├── Issue state → closed
        ├── Label 🔵 Open → removed
        ├── Label 🔒 Closed from Support → added
        ├── TAT auto-calculated (close date − report date)
        └── Project board status → syncs automatically
```

---

## Tabs & Features

### 1. Bug Tracker

The primary tab. Displays all Gleap-reported bugs from `digiqc-hq/product-management` GitHub Issues.

#### Stats Bar
| Card | Description |
|------|-------------|
| Total | All bugs in selected date range |
| Open | Unresolved bugs |
| Closed | Resolved bugs |
| Avg TAT | Average turnaround time for closed bugs |

Stats reflect the active date filter — not all-time totals.

#### Filters
| Filter | Type | Description |
|--------|------|-------------|
| All / Open / Closed | Status chips | Filter by issue state |
| Search | Text input | Search by bug title |
| Today | Date preset | Bugs reported today |
| This Week | Date preset | Monday to Sunday of current week |
| Last Week | Date preset | Previous Monday to Sunday |
| This Month | Date preset | 1st to end of current month |
| Last Month | Date preset | 1st to end of previous month |
| Last 30 Days | Date preset | Rolling 30-day window (**default on load**) |
| From / To | Date range | Custom date range picker |

#### Table Columns (15)

| # | Column | Source | Editable |
|---|--------|--------|----------|
| 1 | # | Issue number | No |
| 2 | Bug | Issue title (cleaned from Gleap) | No |
| 3 | Tag | Bug / Knowledge Gap / Feedback / Other | Yes (inline) |
| 4 | Issue Description | Gleap issue body (cleaned) | No |
| 5 | Solution | Support writes | Yes (inline) |
| 6 | Status | Open / Closed badge | Yes (click to toggle) |
| 7 | Platform | Auto from Gleap `systemName` / `sdkType` | Yes (inline) |
| 8 | Version | Auto from Gleap `releaseVersionNumber` | Yes (inline) |
| 9 | Organisation | Support fills from dropdown | Yes (inline + add new) |
| 10 | Reported By | Auto from Gleap `**Reported by:**` | No |
| 11 | Email | Auto from Gleap mailto link | No |
| 12 | Phone | Support fills | Yes (inline) |
| 13 | Reported | Issue `created_at` date | No |
| 14 | TAT | Auto: close − report date (or time since open) | No |
| 15 | Handled By | Auto from logged-in user on save | No |

#### Detail Panel (Side Overlay)

Click "View" on any bug to open a right-side panel with:

**Read-only:** Issue link, Reported By, Email, Gleap link, Report Date, Close Date, Description, Screenshot, TAT

**Editable:** Organisation (dropdown + add new), User Name, Platform, Version, Tag, Solution Given

**Actions:** Save, Close Bug, Reopen Bug

#### Meta Storage

Support metadata is stored as a structured GitHub comment on the issue with a `<!-- SUPPORT-META -->` marker. Fields: Org, User, Phone, Platform, Version, Solution, Tag, Handled By. The comment is created on first save and updated on subsequent saves.

---

### 2. Onboarding Tracker

Tracks client company lifecycle from Introduction Meeting to Go-Live.

**Data source:** `onboarding.json` in the dashboard GitHub repo.

#### Sub-tabs
| Tab | Shows |
|-----|-------|
| Onboarding | Companies not yet live (no `liveSetup` date) |
| Monitoring | Companies live but no dashboard setup |
| Completed | Companies with `dashboardSetup` date set |

#### Company Fields

| Field | Type | Description |
|-------|------|-------------|
| Organisation | Text | Company name |
| Plan Type | Dropdown | Project Based / User Based |
| Purchased | Number | Users or licenses purchased |
| SPOC Name | Text | Single Point of Contact |
| SPOC Phone | Phone + country code | Contact number |
| System Admin | Textarea | Admin name(s) |
| Intro Meet | Date | Introduction meeting date |
| Training Setup | Date | Training session date |
| Live Setup | Date | Go-live date (moves to Monitoring) |
| Dashboard Setup | Date | Dashboard setup date (moves to Completed) |
| Payment | Textarea | Payment status and terms |
| Action Items | Weekly log | Items + week + who added |
| Notes | Textarea | General remarks |
| Usage | Toggles | Inspection / Instruction / Register |
| Expansion | Dropdown + text | Yes/No/Maybe + details + remark |

#### Features
- All fields inline-editable (click to edit, Enter to save, Esc to cancel)
- Action Items: weekly log with auto-calculated week date
- Export as PDF or PNG (Share button)
- Add/delete companies

---

### 3. Task Tracker

Internal task management for the support/product team.

**Data source:** `tasks.json` in the dashboard GitHub repo.

#### Sub-tabs
| Tab | Shows |
|-----|-------|
| Open | Active tasks |
| Hold | Blocked/waiting tasks |
| Completed | Finished tasks |

#### Task Fields

| Field | Type | Description |
|-------|------|-------------|
| Task | Textarea | Task description |
| Status | Dropdown | Open / Hold / Completed |
| Priority | Dropdown | High (red) / Medium (yellow) / Low (blue) |
| Deadline | Date | Optional due date — shows OVERDUE tag if past |
| Remark | Textarea | Notes and progress |
| Assignees | Multi-select chips | From team list |
| Created / Updated | Auto | ISO dates |

**Assignee options:** Jigar, Ankit, Sumant, Nachiket, Gani, Neha, Devops, Mayank, Jay, Varun, Jainik

---

## GitHub Integration

### Repositories

| Repo | Purpose |
|------|---------|
| `digiqc-hq/product-management` | Source of Gleap bug issues (read/write) |
| `Hathi-Jigar/support-dashboard` | Dashboard code + config/data files (read/write) |

### API Endpoints Used

| Action | Endpoint |
|--------|----------|
| Load issues | `GET /repos/digiqc-hq/product-management/issues?labels=Gleap` |
| Load comments | `GET /repos/.../issues/{number}/comments` |
| Update issue | `PATCH /repos/.../issues/{number}` (state, labels) |
| Post/update comment | `POST` or `PATCH /repos/.../issues/comments/{id}` |
| Load/save config | `GET/PUT /repos/Hathi-Jigar/support-dashboard/contents/config.json` |
| Load/save onboarding | `GET/PUT /repos/.../contents/onboarding.json` |
| Load/save tasks | `GET/PUT /repos/.../contents/tasks.json` |

### Labels

| Label | Meaning | Set by |
|-------|---------|--------|
| `🔵 Open` | Bug is open and unresolved | Auto (Gleap workflow) |
| `🔒 Closed from Support` | Bug closed via dashboard or Gleap | Dashboard / Gleap workflow |
| `Gleap` | Bug originated from Gleap | Auto (Gleap workflow) |
| `Bug` | Issue type is a bug | Auto (Gleap workflow) |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| App | Single HTML file (~2500 lines), embedded CSS + JS |
| Framework | None (vanilla JavaScript) |
| Libraries | html2canvas (export), jsPDF (PDF), Inter font |
| Hosting | GitHub Pages |
| Data | GitHub API v3 (Issues + file contents) |
| Auth | GitHub PAT stored in browser localStorage |

---

## File Structure

```
support-dashboard/
├── README.md              ← This file
├── index.html             ← Dashboard application (single-file)
├── config.json            ← Organisation dropdown list
├── onboarding.json        ← Onboarding tracker data
├── tasks.json             ← Task tracker data
├── health/
│   └── index.html         ← Client Health Dashboard (client-facing, Metabase-powered)
└── .github/
    └── workflows/
        └── weekly-health-alert.yml  ← Weekly WhatsApp alerts via MSG91
```

---

## Setup (one-time per support member)

1. Create a GitHub account (free)
2. Generate a PAT token with `repo` scope
3. Open the [dashboard link](https://hathi-jigar.github.io/support-dashboard/)
4. Enter your name + token → saved in browser
5. Dashboard loads all Gleap bugs and displays them

---

## Default View

On load, the Bug Tracker tab shows **Last 30 Days** of bugs with all statuses (All). Stats cards reflect the same date range. Support can switch presets or set custom date ranges as needed.
