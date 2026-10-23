# Landmark trials

Educational reference of practice-changing trials in hematologic malignancies, created by Andres Ferber, MD, with the assistance of Claude (Anthropic). Content is updated monthly.

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
- **Verification rules**: every number checked against the PubMed abstract or PubMed Central full text; "not reported in abstract" rather than a guess; PMIDs confirmed by journal, volume, pages and first author; unconfirmed regulatory or guideline statements marked "verify"; no invented insurance approval rates.
- **Credit line** in small type under the footer: "Created by Andres Ferber, MD, with the assistance of Claude (Anthropic)."

## Monthly updates

A scheduled task per topic runs on the 1st of each month. It searches PubMed (including follow-up publications of every trial on the page, by registry number and name), FDA/EMA, NCCN and major meetings; updates the artifact; regenerates `topics/<key>.html`; copies the page to `source/<key>.html`; updates `topics.json`; and pushes here. Papers that need a PDF are listed in the monthly summary.

## Adding a topic

Build the full page following the conventions above, publish it as an artifact, then add `source/<key>.html`, `topics/<key>.html` and an entry in `topics.json`, and create its monthly task. The website picks it up automatically.
