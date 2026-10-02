# Lead Generation CRM

A fully custom browser-based CRM built in vanilla HTML/CSS/JS — no frameworks, no database, no dependencies. Built to manage a 400+ lead cold-call pipeline targeting Atlanta-area small businesses.

## Features

- **Tabbed navigation** — Yet To Call, Warm, No Answer, Dead tabs with live record counts
- **Status badge system** — color-coded badges (Warm, No Answer, Bad Number, DNC) per record
- **Live stat counters** — header stats update dynamically as records move between tabs
- **Date-segmented history** — call sessions grouped by date with section labels
- **Single-file architecture** — entire CRM runs as one `.html` file, no server needed

## Automation Scripts

Python scripts using BeautifulSoup to automate bulk record updates:

- Parse and rewrite the HTML file programmatically across hundreds of records
- Handle multi-tbody DOM structures using a counter-based tbody detection method
- Resolve attribute corruption from repeated parse/serialize cycles (double-quote normalization)
- Update stat counters and tab buttons automatically after every batch write

## Demo Site

`demo_site/` contains an example client-facing single-page website delivered as part of the project — a cleaning company site built in semantic HTML/CSS with a dark teal theme, mobile-responsive layout, and service/review/contact sections.

## Tech Stack

`HTML · CSS · JavaScript · Python · BeautifulSoup · DOM manipulation`

## Structure

```
lead-crm/
├── crm.html          # The CRM — open in any browser
├── demo_site/
│   └── index.html    # Example client deliverable
└── scripts/
    └── bulk_update.py # BeautifulSoup automation
```
