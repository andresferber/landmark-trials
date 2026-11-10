# Prognosis tab previews (not live)

Prepared November 9, 2026 for Andres's review. Nothing here is loaded by the website.

- `smm_entries.py`: Prognosis data for smoldering myeloma. No new cards: PROG records for the seven
  existing Definition & risk entries, and PROGMAP for QuiRedex.
- `rrmm_entries.py`: Prognosis data for relapsed myeloma. Adds a "Risk & response" category with five
  cards (three shared with ndmm; two new: t(11;14) and venetoclax, early relapse), PROG and PROGMAP.
  The page also needs `risk` added to SETTINGS, CLS and `order`, and a `.tag.risk` style.
- `myeloma_markers_preview.json`: the shared Markers to watch list plus three candidates (genomic
  predictors in smoldering myeloma, soluble BCMA, antigen-loss mutations). Citation counts not yet added.

To go live after approval: run the entries script on `source/<key>.html`, then
`python3 tools/prognosis/install_progtab.py tools/prognosis/myeloma_markers.json source/<key>.html`
(merge approved markers into `myeloma_markers.json` first and rerun on every page with the tab), move the
scripts up to `tools/prognosis/`, and extend the Prognosis section of `tools/UPDATE_GUIDE.md` to smm and rrmm.
