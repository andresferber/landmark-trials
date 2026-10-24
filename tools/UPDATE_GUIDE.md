# Landmark trials: how to run a scheduled update

This guide is read by each topic's scheduled update task. The task prompt gives the topic
(artifact URL, key, title and what to look for); everything else is here. Andres Ferber, MD
(hematology-oncology, teaches trainees) owns the content; write for an expert.

## 0. Setup
- Call the add_repo tool with owner "andresferber", repo "landmark-trials", access "push".
- `git clone --depth 1 https://github.com/andresferber/landmark-trials ~/landmark-trials`
- Read the artifact with the Artifact tool (action "read") and work from the saved full-page
  file it returns. If that file differs from `~/landmark-trials/source/<key>.html` in content,
  the artifact is the master; mention the difference in the summary.

## 1. Page structure (keep it; add or edit, never rewrite)
All data is in the main `<script>`:
- `T`: one entry per trial: `y` year, `n` name, `s` category, `ph` phase, `d` design,
  `ep` endpoint, `r` result, `N`, `hr`, `fu`, `c` citation, `p` PMID, optional `extra`
  [label, PMID], `b` builds on, `i` changed, `q` open questions, `cm` commentaries
  [[pmid, byline, title]], `reg` regulatory, `gl` guidelines, `acc` access.
  (The MCL page keeps the same information in separate objects M, P, EXTRA, CITE, V, X, R.)
- `REG`: name -> registry IDs (NCT, ISRCTN or EudraCT), from the PubMed DataBank list or abstract.
- `FT`: name -> `["pmc", PMCID]` (free full text, not embargoed), `["doi", DOI]` (publisher page),
  `["doi", DOI, "free"]` (free to read at the publisher, per Unpaywall) or
  `["doi", DOI, "repo", URL]` (legal free copy in a university repository, per Unpaywall; shown as an
  extra "Free copy (repository)" link). For every new `["doi", ...]` entry query
  `https://api.unpaywall.org/v2/<DOI>?email=andresferber@hotmail.com`: best_oa_location host_type
  "publisher" -> "free"; "repository" -> "repo" with url_for_pdf or url (skip URLs on the publisher's
  own domain or pubmed). If Unpaywall cannot be reached, keep `["doi", DOI]`.
- `PAGEKEY`, `PAGETITLE`: topic key and title, used by the per-trial share link and the
  "Report an error" mailto (andresferber@hotmail.com). Abbreviations live in `<details class="gloss">`
  before the footer: add any new abbreviation a new entry introduces.
- `MOA`: key -> one review on how a drug or drug class works and how resistance develops
  `{l label, a first author, j journal, y year, t title, p PMID, pmc PMCID or ""}`; `MOAMAP`: trial name ->
  MOA keys (the new agent the trial tested; a combination can have two). Shown as the "Drug mechanism"
  row. Trials of strategy, transplant, radiotherapy, observation or conventional chemotherapy have none.
  For a new entry, reuse an existing key when the class matches. Once a year (the first update run in
  October), search PubMed for each key (review[pt], last 3 years) and replace a review only when a newer
  one is clearly better. Andres prefers the most up-to-date, comprehensive, high-quality peer-reviewed review; who the authors are does not matter. Mechanism-focused, strong journal, not promotional; free full text preferred
  when quality is comparable. The master list is `tools/moa_master.json`; keep it in sync.
- Pharma-bias rule (Andres): keep the content free of promotional influence. Never use or link
  company-produced educational material for physicians, drug advertising (media, social media or
  journal ads), or company press releases as sources; use generic drug names rather than trade names
  wherever possible (including the glossary and regulatory notes). Allowed: papers with industry
  authors, trial names that come from the sponsor, company code names for drugs (e.g. when there is no
  generic name yet), links to sponsored protocols or registry records, and FDA prescribing information.
  When unsure, ask Andres.
- Every page footer carries the "For education only" disclaimer (class sitedisc). Keep it.
- Independence: this is Andres's independent project, done on his own time and funds. No links or
  references to his employer (Jefferson Health) and no preference for its publications; cite them
  when they are the best fit, like any other source. The only contact address is
  andresferber@hotmail.com, used for "Report an error" and the footer "send a comment" link.
- Perspective (Andres's chosen name for the narrative; `<details class="review">` under the header,
  labelled "Perspective", pilot on rrmm): must open with the disclaimer box (personal perspective, for
  education only, not a guideline or medical advice; care should follow the literature, guidelines,
  prescribing information and the individual patient). Built by
  tools/review/<key>_review.py, where every number comes from a trial entry and [[Trial name]]
  becomes a numbered reference to that trial's card. When an entry changes, update only the
  affected sentences and the "Last updated" date. Small factual edits go live automatically and are
  listed in the summary; rewrites of a section (for example after a new practice-changing trial)
  wait for Andres's approval. While the block says "Pilot draft, pending review", to_weebly.py
  keeps it off the website.
- New drugs to watch (`NEWD`, own tab; pilot on rrmm, built by tools/newdrugs/<key>_newdrugs.py): agents
  with a new mechanism, target or modality not yet approved for the disease (examples Andres gave:
  RNA vaccines, new targets such as menin inhibitors, XPO1 inhibition, BTK degraders), including
  phase 1 when the approach is new and repurposed drugs with credible clinical data. No biosimilars,
  no preclinical-only agents. Each entry: target, modality, evidence label (peer-reviewed phase N, or
  meeting data not yet peer-reviewed), why it matters, key data, safety, next step (phase 3 NCT),
  sources. Lifecycle: when phase 3 results are published, move it to "Moved on to phase 3 results"
  and propose the trial for the landmark list; when development stops or a pivotal trial fails, move
  it to "Discontinued" with reason and date, and remove it after 2 years; review entries with no new
  data for 24 months. Refresh at each scheduled update and in an extra pass after ASH, ASCO, EHA,
  AACR, ESMO and IMS. While wrapped in <!--pilot-start--> markers, to_weebly.py keeps it off the website.
- `TOX`: name -> one line of key toxicity from the abstract (or full paper, marked "(full paper)").
- `CORE`: names of core teaching trials. Andres chooses these: never add or remove names yourself.
  If a new trial looks core-worthy, suggest it in the summary.
- `WATCH`: `{note, items:[{n, nct, ph, d, ep, st, pcd, note}]}`: ongoing trials to watch.
- Values marked "full paper" were checked against the full publication: keep them unless a newer
  paper supersedes them. The evidence tag ("✓ abstract" / "✓ abstract + full paper") is computed
  automatically from those markers.
- Keep the design, the methods footer (update its "Last checked" date) and the small credit line
  under the footer: "Created by Andres Ferber, MD, with the assistance of Claude (Anthropic)."

## 2. What to look for (window: since the topic's last update date in topics.json)
- New PubMed papers: phase 3 and practice-changing phase 2 trials for the topic, and the named
  trials in the task prompt.
- Follow-up of every trial already on the page: search PubMed for papers in the window by each
  registry ID in `REG` (the ID itself as the search term) and by trial name or acronym with first
  author. Long-term follow-up, final OS and important secondary analyses update the existing entry
  (new numbers with their follow-up time; the new paper as `extra`) instead of a new entry.
- New editorials, comments or correspondence on entries (efetch XML CommentsCorrections
  RefType="CommentIn", or editorial/comment publication types). Add to `cm`.
- FDA/EMA actions; NCCN version changes; major meetings (ASH, ASCO, EHA, IMS, ICML) via WebSearch.
- Trials to watch: for each `WATCH` item, query ClinicalTrials.gov
  (`https://clinicaltrials.gov/api/v2/studies/<NCT>?fields=NCTId,BriefTitle,Acronym,OverallStatus,PrimaryCompletionDate,Phases`)
  and update `st` (status) and `pcd` (primary completion, with "(estimated)" when the registry says
  so). When a watched trial publishes its primary results, remove it from `WATCH` and, if it is
  landmark-level, add it to `T`. Add newly started phase 3 trials that could change practice for the
  topic (search `https://clinicaltrials.gov/api/v2/studies?query.cond=<condition>&filter.overallStatus=RECRUITING,ACTIVE_NOT_RECRUITING&query.term=AREA[Phase]PHASE3`);
  keep the list to about 6-10 items. Update `WATCH.note` with the check date.
  If ClinicalTrials.gov cannot be reached, leave `WATCH` unchanged and say so.

How to search PubMed: curl to `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
(esearch.fcgi, efetch.fcgi, esummary.fcgi, elink.fcgi; about 0.4 s between calls).
efetch XML includes CommentsCorrections and DataBank registry numbers; esummary articleids give DOI
and PMCID. Full text: `elink.fcgi?dbfrom=pubmed&db=pmc&id=<PMID>` then `efetch.fcgi?db=pmc&id=<PMCID>`;
use it when available. If PubMed cannot be reached, use WebSearch and say so in the summary.

## 3. Verification rules
- Every new number checked against the PubMed abstract or PubMed Central full text.
- Every new reference: PMID confirmed by journal, volume, pages and first author.
- "not reported in abstract" instead of guessing. Unconfirmed regulatory items: "verify".
  When you confirm one, replace "verify" with the fact and its date. Guideline placements that cannot be
  confirmed because NCCN needs a login are marked "(NCCN not checked)"; never enter a password.
- New entries get `REG` (if any), `FT` and a `TOX` line.
- Interpretive fields (b, i, q, guideline placement) are measured, never overstated.
- Never invent insurance approval rates.
- PDFs needed: if a new or updated paper is not in PubMed Central and an important detail is missing
  from its abstract (OS, key subgroups, toxicity, follow-up), keep "not reported in abstract" and add
  the paper to a "PDFs needed" list with what is missing.

## 4. Publish (only if something changed, including WATCH)
- Update the page, `node --check` the script, and republish to the same artifact URL (pass `url`).
- `python3 ~/landmark-trials/tools/to_weebly.py <page> <key> ~/landmark-trials/topics/<key>.html`;
  check it contains `id="lt-<key>"` and its `<script>` passes `node --check`.
- Copy the page to `~/landmark-trials/source/<key>.html`.
- In `topics.json`, for this key only: set `updated` (YYYY-MM-DD) and `count` (keep its word).
- `cd ~/landmark-trials && node tools/build_index.js` (rebuilds the site-wide search).
- In `news.json`, add one item at the top for each notable change:
  `{"date": "YYYY-MM-DD", "key": "<key>", "slug": "<trial slug, optional>", "text": "<one short sentence>"}`.
  The slug is the trial name lowercased with runs of non-alphanumerics replaced by "-".
  Keep at most 12 items.
- Commit as `Claude <noreply@anthropic.com>` ("Update <key>: <what changed>"), then
  `git fetch origin main && git rebase origin/main && git push origin HEAD:main`. Other topics push
  to the same repository around the same time: if the push is rejected, fetch, rebase and push again
  (up to 3 tries; on a news.json or index.json conflict, take theirs, then re-add your news item and
  rerun build_index.js).
- If you cannot push for another reason, say so and attach `topics/<key>.html` with SendUserFile
  (display "attach").

## 5. Tell Andres (always)
SendUserMessage with a short summary: what was added or changed (trial, source), or
"No new <topic> trials, commentaries, regulatory changes or trial-status changes since <date>."
If the website was updated, add: "The Landmark Trials page on andresferber.org now shows this update."
Mention suggested core trials if any. List sources as markdown links. If "PDFs needed" is not empty,
end with that section (short citation, PubMed link, what is missing) and say he can attach the PDFs in
a reply to this message.

## 6. If Andres replies with PDFs
Read them, fill in the missing details (mark each value "(full paper)"), then publish as in step 4
and confirm what changed.
