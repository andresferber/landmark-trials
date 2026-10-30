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
  (The MCL page keeps the same information in separate objects M, P, EXTRA, CITE, V, X, R.
  V and CITE are applied on top of T, and the card displays them: to change what a reader sees
  on the MCL page, edit V or CITE, not T. If a trial has both, keep them consistent.)
- Card rows: Endpoint, Result and Key toxicity (and Key data / Safety in New drugs to watch) carry the
  classes f-ep, f-res and f-tox, which give them the same subtle tint on every page. Keep those classes
  when editing the card template; tools/newdrugs/install_fieldtint.py adds them to a new page.
- Tabs: clicking an open tab (Trials to watch, New drugs to watch, Drug mechanisms) closes it and returns to
  the trial list; while one is open the tab bar stays pinned at the top (on the website, just below the
  pinned topic title). Build order for a new page: tools/newdrugs/install_tabs.py, install_fieldtint.py,
  tools/mechs/install_mechtab.py, then tools/newdrugs/install_tabpin.py (it fails if the tab handler is missing).
- Drug mechanisms tab: one entry per drug class tested on the page (MOA keys used in MOAMAP), with a
  plain description from tools/mechs/mech_master.json (shared by all pages), the mechanism review and
  the trials that used it. When a new trial brings a new MOA key, write its description in
  mech_master.json (two or three factual sentences, generic names, no promotional sources) and run
  `python3 tools/mechs/install_mechtab.py tools/mechs/mech_master.json source/<key>.html`, which also
  refreshes pages that already have the tab. A page whose MOAMAP uses a key with no description fails
  the script on purpose.
- Perspective bar: a light parchment tint with a gold left stripe (--rv-bg, --rv-stripe, --rv-ink) sets it
  apart from the tab bar; the open reading area stays white. tools/review/install_persptint.py adds it to
  a new page after build_persp.py.
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
- Default sort is "category, newest first" with category subtitles in the list; keep it.
- Every page footer carries the "For education only" disclaimer (class sitedisc). Keep it.
- Independence: this is Andres's independent project, done on his own time and funds. No links or
  references to his employer (Jefferson Health) and no preference for its publications; cite them
  when they are the best fit, like any other source. The only contact address is
  andresferber@hotmail.com, used for "Report an error" and the footer "send a comment" link.
- Perspective (Andres's chosen name for the narrative; `<details class="review">` under the header,
  labelled "Perspective", pilot on rrmm): must open with the disclaimer box (personal perspective, for
  education only, not a guideline or medical advice; care should follow the literature, guidelines,
  prescribing information and the individual patient). Built by
  tools/review/build_persp.py <key> <page> from tools/review/persp_<key>.py (rrmm uses rrmm_review.py), where every number comes from a trial entry and [[Trial name]]
  becomes a numbered reference to that trial's card. When an entry changes, update only the
  affected sentences and the "Last updated" date. Small factual edits go live automatically and are
  listed in the summary; rewrites of a section (for example after a new practice-changing trial)
  wait for Andres's approval. While the block says "Pilot draft, pending review", to_weebly.py
  keeps it off the website.
- Tabs: every page has Landmark trials | Trials to watch | New drugs to watch, plus a "Send a comment"
  mailto link (tools/newdrugs/install_tabs.py installs them).
- New drugs to watch (`NEWD`): one list per disease, shared by its topics (myeloma: smm, ndmm, rrmm;
  follicular lymphoma: flu, flr; mcl). Keep the copies identical when editing. Agents
  with a new mechanism, target or modality not yet approved for the disease (examples Andres gave:
  RNA vaccines, new targets such as menin inhibitors, XPO1 inhibition, BTK degraders), including
  phase 1 when the approach is new and repurposed drugs with credible clinical data. No biosimilars,
  no preclinical-only agents. Each entry: target, modality, evidence label (peer-reviewed phase N, or
  meeting data not yet peer-reviewed), why it matters, key data, safety, next step (phase 3 NCT),
  sources. Lifecycle: when phase 3 results are published, move it to "Moved on to phase 3 results"
  and propose the trial for the landmark list; when development stops or a pivotal trial fails, move
  it to "Discontinued" with reason and date, and remove it after 2 years; review entries with no new
  data for 24 months. Refresh at each scheduled update and in an extra pass after ASH, ASCO, EHA,
  AACR, ESMO and IMS.
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
- New PubMed papers: phase 3 trials, phase 2 trials that meet the phase 2 bar below, and the named
  trials in the task prompt.
- Phase 2 bar (Andres, Oct 30, 2026). Add the primary report of a phase 2 or phase 1/2 trial on the
  topic when (a) it is published in N Engl J Med or Nat Med; or (b) it is published in Blood or
  J Clin Oncol and led to an FDA or EMA approval, changed a guideline, or defined a regimen still in use;
  or (c) in any journal, it was the basis of an approval or is otherwise practice-changing. Phase 1
  dose-escalation reports, secondary or correlative analyses and long-term follow-up do not qualify as
  new entries (follow-up updates the existing card). Search: the topic terms AND
  ("N Engl J Med"[ta] OR "Nat Med"[ta] OR "Blood"[ta] OR "J Clin Oncol"[ta] OR "Lancet"[ta] OR
  "Lancet Oncol"[ta] OR "Lancet Haematol"[ta] OR "JAMA Oncol"[ta]) AND ("Clinical Trial, Phase II"[pt]
  OR "phase 2"[ti] OR "phase II"[ti] OR "phase 1/2"[ti] OR "phase I/II"[ti]), in the window. In the
  summary, list each phase 2 paper considered and why it was added or skipped. On the MCL page, a new
  entry also needs a `V` entry {r, N, fu} (that is what shows "✓ abstract"); tools/review/add_entries.py
  does this and the other objects for a list of entries.
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
  topic (search `https://clinicaltrials.gov/api/v2/studies?query.cond=<condition>&filter.overallStatus=RECRUITING,ACTIVE_NOT_RECRUITING&query.term=AREA[Phase]PHASE3`).
  Also list up to 3 ongoing phase 2 trials designed to support an approval (registrational: single-arm
  or randomized, efficacy primary endpoint such as ORR by independent review, usually industry-sponsored
  with about 80 or more patients, not phase 1/2 dose finding), with `ph` "Phase 2 (registrational)"
  (search the same way with `AREA[Phase]PHASE2 AND AREA[LeadSponsorClass]INDUSTRY`, then judge each).
  When such a trial publishes its primary results, it leaves `WATCH` and is added to `T` if it meets the
  phase 2 bar. Keep the list to about 6-12 items. Update `WATCH.note` with the check date.
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
- In `news.json`, add one item at the top only for a content change a reader would care about
  (a new trial, a major result update, a new drug on the watch lists), or for a major new feature such as a
  new section or a new disease. Never for cosmetic changes (colours, fonts, spacing) or tooling, which would
  make the box less relevant.
  The "What's new" box shows only the newest 2 items. Format:
  `{"date": "YYYY-MM-DD", "key": "<key>", "slug": "<trial slug, optional>", "text": "<one short sentence>"}`.
  The slug is the trial name lowercased with runs of non-alphanumerics replaced by "-".
  Keep at most 6 items in the file.
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
Mention suggested core trials if any.
Add a "Worth a look (not added)" section whenever you found papers or trials that do not meet the rules
(the phase 2 bar, the WATCH criteria, the NEWD criteria) but may interest Andres: for example a notable
phase 2 trial in another journal, a large secondary analysis, an influential single-center series or a
strong meeting abstract. For each give the citation with its PubMed (or registry) link, one line on why
it is interesting, and which rule it misses, and say he can reply "include <name>" to add it. Do not add
these yourself. If none, leave the section out. List sources as markdown links. If "PDFs needed" is not empty,
end with that section (short citation, PubMed link, what is missing) and say he can attach the PDFs in
a reply to this message.

## 6. If Andres replies "include <name>"
Add the trial as a normal entry (verified as in section 3), republish and push as in section 4, and
reply with one line saying it is live.

## 7. If Andres replies with PDFs
Read them, fill in the missing details (mark each value "(full paper)"), then publish as in step 4
and confirm what changed.

## 8. Applying a proofread report
A quarterly scheduled proofread (15th of Jan, Apr, Jul, Oct) runs in a fresh session, reports only,
and sends Andres a findings list. When he brings that list to a session to fix:
- Verify each finding against its source before changing anything; the proofreader can be wrong.
  Say which findings you rejected and why.
- Edit the layer the card actually displays (see section 1), in source/<key>.html, then copy it to
  the working page that is published to the artifact.
- Perspective text lives in tools/review/persp_<key>.py (tools/review/rrmm_review.py for RRMM).
  Edit there and rebuild with build_persp.py (or rrmm_review.py); never hand-edit the rendered
  <details class="review"> block, which the next rebuild overwrites.
- Render every changed page in a headless browser, confirm each corrected text appears and the old
  text is gone, with no script errors. Then publish as in step 4.
- Do not apply fixes on the 1st or 2nd of a month, when the topic updates and health check run.

