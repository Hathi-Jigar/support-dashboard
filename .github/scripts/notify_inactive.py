import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date

# Validate webhook
webhook = os.environ.get("GOOGLE_CHAT_WEBHOOK", "").strip()
if not webhook:
    print("ERROR: GOOGLE_CHAT_WEBHOOK secret is not set!")
    sys.exit(1)
print(f"Webhook OK (length={len(webhook)})")

# Load Metabase response
try:
    with open("/tmp/result.json") as f:
        raw = json.load(f)
except Exception as e:
    print(f"Failed to load result.json: {e}")
    sys.exit(1)

# Parse rows
if isinstance(raw, list):
    rows = raw
elif "data" in raw:
    cols = [c["name"] for c in raw["data"]["cols"]]
    rows = [dict(zip(cols, r)) for r in raw["data"]["rows"]]
else:
    print(f"Unexpected structure: {list(raw.keys())}")
    sys.exit(1)

print(f"Total rows: {len(rows)}")
if rows:
    print(f"Columns: {list(rows[0].keys())}")

# Detect org name column
ORG_COL = None
for candidate in ["Organization Name", "organization_name", "Organisation Name", "name", "Name"]:
    if rows and candidate in rows[0]:
        ORG_COL = candidate
        break
if not ORG_COL:
    ORG_COL = list(rows[0].keys())[0] if rows else "col0"
print(f"Using column: {ORG_COL}")

# Filter inactive > 5 days
alerts   = [r for r in rows if r.get("inactive_days") and float(r["inactive_days"]) > 5]
critical = [r for r in alerts if float(r["inactive_days"]) > 30]
high     = [r for r in alerts if 14 < float(r["inactive_days"]) <= 30]
watch    = [r for r in alerts if  5 < float(r["inactive_days"]) <= 14]

print(f"Alerts: {len(alerts)} | Critical: {len(critical)} | High: {len(high)} | Watch: {len(watch)}")

if not alerts:
    print("No alerts today. All orgs active within 5 days.")
    sys.exit(0)

# Build Google Chat card widgets
widgets = []
for r in alerts:
    days = float(r["inactive_days"])
    org  = r.get(ORG_COL, "Unknown")
    if   days > 30: emoji, lbl = "\U0001f534", "Critical"
    elif days > 14: emoji, lbl = "\U0001f7e0", "High"
    else:           emoji, lbl = "\U0001f7e1", "Watch"
    widgets.append({
        "decoratedText": {
            "topLabel": f"{emoji} {lbl}",
            "text": f"<b>{org}</b>",
            "bottomLabel": f"{int(days)} days inactive"
        }
    })

# Summary widget
summary_widget = {
    "columns": {
        "columnItems": [
            {"widgets": [{"decoratedText": {"topLabel": "\U0001f534 Critical >30d", "text": f"<b>{len(critical)}</b>"}}]},
            {"widgets": [{"decoratedText": {"topLabel": "\U0001f7e0 High >14d",     "text": f"<b>{len(high)}</b>"}}]},
            {"widgets": [{"decoratedText": {"topLabel": "\U0001f7e1 Watch >5d",     "text": f"<b>{len(watch)}</b>"}}]}
        ]
    }
}

# Full payload
payload = {
    "cardsV2": [{
        "card": {
            "header": {
                "title": "digiQC Inactivity Report",
                "subtitle": f"{date.today().strftime('%d %b %Y')} - {len(alerts)} org(s) inactive > 5 days",
                "imageType": "CIRCLE"
            },
            "sections": [
                {
                    "header": f"Inactive Orgs ({len(alerts)})",
                    "collapsible": True,
                    "uncollapsibleWidgetsCount": 5,
                    "widgets": widgets
                },
                {
                    "header": "Summary",
                    "widgets": [summary_widget]
                },
                {
                    "widgets": [{
                        "buttonList": {
                            "buttons": [{
                                "text": "Open Metabase",
                                "onClick": {
                                    "openLink": {
                                        "url": "http://metabase-v2.digiqc.com/public/question/e9331eaf-825d-46f8-a865-64f6727b3801"
                                    }
                                }
                            }]
                        }
                    }]
                }
            ]
        }
    }]
}

# Send to Google Chat
data = json.dumps(payload).encode()
req = urllib.request.Request(
    webhook,
    data=data,
    headers={"Content-Type": "application/json"}
)
try:
    resp = urllib.request.urlopen(req)
    print(f"Alert sent! HTTP {resp.status} | {len(alerts)} org(s) flagged.")
except urllib.error.HTTPError as e:
    print(f"Webhook error: {e.code} - {e.read().decode()}")
    sys.exit(1)
except urllib.error.URLError as e:
    print(f"URL error: {e.reason}")
    sys.exit(1)
