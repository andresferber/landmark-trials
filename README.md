# Landmark trials

Educational reference of practice-changing trials in hematologic malignancies, created by Andres Ferber, MD, with the assistance of Claude (Anthropic). Content is updated on a per-topic schedule (monthly to quarterly).

## How it works

- `topics.json` lists the topics shown on the website, in order. `group` sets the coloured group heading (see `GROUP_COLORS` in `loader.js`).
- `topics/<key>.html` holds each topic's self-contained website section, generated from the topic's full page with `tools/to_weebly.py`.
- `source/<key>.html` is the full page for each topic, the same file published as the topic's Claude artifact. It is the master copy of the content kept here as a backup.
- `loader.js` builds the accordion on any page that includes:

```html
<div id="landmark-trials"></div>
<script src="https://andresferber.github.io/landmark-trials/loader.js"></script>
```

- `index.html` is a standalone page showing the same content.

## Backup and restore

Every change is a commit, so every earlier version of every file is kept in this repository's history. To restore a topic's full page, take `source/<key>.html` from the version wanted and republish it to the topic's artifact; to restore the website section, take `topics/<key>.html`. The whole repository can be downloaded as a ZIP from the green "Code" button on GitHub.

## Content conventions (use these for every new topic)

Each topic page is one HTML file with:

- **Data**: a JavaScript array `T`, one entry per trial: `y` year, `n` name, `s` category, `ph` phase, `d` design, `ep` endpoint, `r` result, `N`, `hr`, `fu`, `c` citation, `p` PMID, optional `extra` [label, PMID], `b` builds on, `i` what it changed, `q` open questions, `cm` commentaries [[pmid, byline, title]], `reg` regulatory, `gl` guidelines, `acc` access. (The MCL page predates this layout and keeps the same information in separate objects.)
- **Registry numbers**: object `REG` mapping each entry name to its registry IDs (ClinicalTrials.gov NCT, ISRCTN or EudraCT), taken from the paper's PubMed record. Shown as links next to the source and used by the monthly update to find later follow-up publications.
- **Full-text links**: object `FT` mapping each entry name to `["pmc", PMCID]` (free full text in PubMed Central, not embargoed) or `["doi", DOI]` (publisher page), taken from the PubMed record; DOI entries carry a third value "free" or "repo" when Unpaywall finds a legal free copy (see tools/UPDATE_GUIDE.md).
- **Share, report, abbreviations**: each trial has a copy-link button (deep link `#t-<key>-<slug>`) and a "Report an error" mailto to andresferber@hotmail.com; each page ends with an abbreviations list (`details.gloss`).
- **Drug mechanism** (`MOA`, `MOAMAP`): one recent review per drug or drug class on mechanism of action and resistance, linked in each trial card; refreshed yearly (see tools/UPDATE_GUIDE.md). Master list: `tools/moa_master.json`.
- **Pharma-bias rule**: no company-produced educational material, advertising or press releases as sources, and generic names rather than trade names wherever possible. Industry-authored papers, sponsor trial names, company drug codes, sponsored protocol links and FDA prescribing information are fine. Details in tools/UPDATE_GUIDE.md.
- **Disclaimer**: every page footer states that the content is for education only and is not medical advice or a guideline.
- **Independence**: an independent project of Andres Ferber, MD; no employer links or preference for any institution's publications. Contact: andresferber@hotmail.com (report an error, comments).
- **Perspective** (pilot on relapsed myeloma): a collapsible personal perspective on how management evolved (past, present and future), opening with an education-only disclaimer, with a timeline and numbered references to the trial cards; see tools/UPDATE_GUIDE.md.
- **Which trials are included**: phase 3 trials, key risk models and consensus statements, and phase 2 trials that meet the phase 2 bar (Oct 30, 2026): published in N Engl J Med or Nat Med; or in Blood or J Clin Oncol when they led to an FDA/EMA approval, changed a guideline or defined a regimen still in use; or, in any journal, the basis of an approval or otherwise practice-changing. Follow-up papers update the existing card. Each page's methods footer states this.
- **Borderline candidates**: papers or trials that miss the rules but may interest Andres are listed in the update summary under "Worth a look (not added)", with why and which rule they miss; they are added only if he replies "include <name>".
- **Key toxicity** (`TOX`), **core trials** (`CORE`, chosen by Andres) and **trials to watch** (`WATCH`: ongoing phase 3 trials plus up to 3 ongoing phase 2 trials designed to support an approval): see tools/UPDATE_GUIDE.md.
- **Verification rules**: every number checked against the PubMed abstract or PubMed Central full text; "not reported in abstract" rather than a guess; PMIDs confirmed by journal, volume, pages and first author; unconfirmed regulatory statements marked "verify"; guideline placements that need NCCN (login) marked "(NCCN not checked)"; no invented insurance approval rates.
- **Credit line** in small type under the footer: "Created by Andres Ferber, MD, with the assistance of Claude (Anthropic)."

## Search and news

`index.json` (built by `node tools/build_index.js` from `source/`) powers the search across all topics on the website; `news.json` feeds the "What's new" box.

## Scheduled updates

A scheduled task per topic runs on the 1st of the month on its own schedule: monthly for newly diagnosed and relapsed myeloma; every 2 months (Jan, Mar, May, Jul, Sep, Nov) for MCL and relapsed FL; quarterly (Jan, Apr, Jul, Oct) for smoldering myeloma and untreated FL. A health check runs on the 2nd of each month. It searches PubMed (including follow-up publications of every trial on the page, by registry number and name), FDA/EMA, NCCN and major meetings; updates the artifact; regenerates `topics/<key>.html`; copies the page to `source/<key>.html`; updates `topics.json`; and pushes here. Papers that need a PDF are listed in the monthly summary. The full procedure is in `tools/UPDATE_GUIDE.md`, which the scheduled tasks follow.

## Adding a topic

Build the full page following the conventions above, publish it as an artifact, then add `source/<key>.html`, `topics/<key>.html` and an entry in `topics.json`, and create its monthly task. The website picks it up automatically.
