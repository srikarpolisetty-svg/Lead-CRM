# Lead Generation CRM

A fully custom, single-file CRM built in vanilla HTML/CSS/JS to manage a 400+ lead cold-call pipeline — no frameworks, no database, no dependencies. Paired with a Python automation layer for bulk record management and a client-facing website delivery system.

---

## Why I Built This

Most CRM tools are built for teams with budgets. I needed something I could open in a browser, update in seconds, and carry across sessions without touching a server. So I built one.

The goal was a pipeline tool that matched exactly how I work: tab through lead stages, log call outcomes fast, see live stats at a glance, and never lose context between sessions. Everything runs from a single `.html` file.

---

## Architecture

### Single-File CRM (`crm.html`)

The entire application lives in one HTML file. No build step. No server. Open it in any browser and it works.

**Tab system** — four stages with independent record counts:
- `📞 Yet To Call` — uncontacted leads queued for outreach
- `⭐ Warm` — prospects who expressed interest, flagged for follow-up
- `📵 No Answer` — attempted contacts, grouped by call date
- `💀 Dead` — bad numbers, DNC, and disqualified leads

**Live stat counters** — header stats reflect current record counts across all tabs. Updated programmatically on every write.

**Status badge system** — color-coded badges per record: `Warm — Call Back`, `No Answer`, `Bad Number`, `Not Interested`, `DNC`. Each badge maps to a CSS class for instant visual scanning.

**Date-segmented history** — call sessions are grouped under date labels (`── 5/29/26 CALLS`) so activity is traceable across multiple days without a separate log.

**Phone formatting** — all numbers stored in `(4XX) XXX-XXXX` format with a dedicated `.phone` class for consistent rendering.

---

### Python Automation Layer (`scripts/bulk_update.py`)

Manually updating hundreds of HTML records is a bottleneck. The automation layer treats the HTML file as a structured document and rewrites it programmatically.

**Key engineering decisions:**

**Multi-tbody detection problem** — HTML tables with complex structures produce multiple `<tbody>` elements. Naively indexing by position (`tbodies[4]`) breaks when the DOM shifts. Instead, I use a Counter-based detection method: find all `warm-row` elements, count parent occurrences, and select the tbody with the highest frequency. This is O(n) and position-independent.

```python
all_warm = soup.find_all('tr', class_='warm-row')
counts = Counter(id(tr.parent) for tr in all_warm)
warm_tbody = next(tr.parent for tr in all_warm
                  if id(tr.parent) == counts.most_common(1)[0][0])
```

**Attribute corruption from repeated parse/serialize cycles** — BeautifulSoup's serializer introduces double-quote corruption (`class=""warm-row""`) on repeated read/write cycles. Fixed with a regex normalization pass applied on both load and save:

```python
html = re.sub(r'=""([^"]*?)""', r'="\1"', html)
```

**Atomic stat updates** — every write operation closes with a stat sync that updates both the header counters and tab button labels simultaneously, keeping the UI consistent regardless of which records changed.

---

### Lead Verification Pipeline

Before any lead enters the CRM, it passes a two-step verification process:

1. **Directory check** — confirm the Yelp listing has no website link (`website: null`, no `biz_website` anchor element)
2. **Web search check** — search `"[Business Name]" [City] GA` and scan results for any standalone domain. Safe results (Yelp, BBB, Facebook, Angi, Thumbtack, etc.) pass. Any real domain (`businessname.com`, GoDaddy sites, etc.) eliminates the lead.

**Phone mismatch rule** — if a website is found but its listed phone differs from the lead's phone, it's likely a different business with a similar name. Lead is kept.

**Source validation** — phone numbers cross-referenced across 2+ directories before entry. Single-source numbers flagged with a note. Numbers resolving to a different business are eliminated.

This pipeline kept the lead list clean across 400+ records and reduced bad-number call rate significantly.

---

### Client Website Delivery (`demo_site/`)

Warm prospects receive a same-day demo website built to their business. Each site is a semantic, mobile-responsive single-page HTML/CSS deliverable — no CMS, no dependencies, ships as a single file.

`demo_site/index.html` — example delivery for a residential cleaning company:
- Dark teal brand theme with Poppins font via Google Fonts
- Sections: nav, hero, services, about, reviews, CTA, contact form, footer
- All CTAs wired to `tel:` links for direct mobile calls
- Fully responsive with CSS Grid and Flexbox

---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS |
| Automation | Python 3, BeautifulSoup4 |
| Data pipeline | Web scraping, regex, multi-source cross-referencing |
| Delivery | Semantic HTML/CSS, mobile-responsive layout |

---

## Project Scale

- **400+** leads sourced, verified, and tracked
- **260+** outreach attempts logged with outcomes
- **23** warm prospects generated
- **10+** lead batches processed through the verification pipeline
- **Multiple** client demo sites delivered

---

## File Structure

```
lead-crm/
├── crm.html              # Full CRM — open in any browser
├── demo_site/
│   └── index.html        # Example client website deliverable
├── scripts/
│   └── bulk_update.py    # BeautifulSoup automation library
└── README.md
```
