"""Three phase 2 trials added to untreated DLBCL on Nov 11, 2026 at Andres's request ("include"): they
miss the phase 2 bar and were listed under "Worth a look (not added)" on Nov 10, 2026. Verified against
the PubMed abstracts; E1412 toxicity and dose from the PubMed Central full text. Applied by
tools/review/add_entries.py."""

DLBU = [
 dict(y=2021, n="ECOG-ACRIN E1412 (Nowakowski)", s="nov", ph="Phase 2 (randomized)",
  d="Lenalidomide 25 mg on days 1–10 with R-CHOP (R2CHOP) vs R-CHOP for 6 cycles; untreated DLBCL, stage II bulky to IV, IPI ≥2; all cell-of-origin subtypes, with no biomarker selection at entry (dose and selection: full paper)",
  ep="PFS in all patients; co-primary PFS in ABC DLBCL",
  r="3-year PFS 73% vs 61% (one-sided P=.03); 3-year OS 83% vs 75% (HR 0.67, one-sided P=.05). ORR 97% vs 92% (P=.06); CR 73% vs 68% (P=.43). ABC subtype: PFS HR 0.67 (one-sided P=.1)",
  N="349 enrolled; 280 evaluable", hr="0.66 (95% CI 0.43–1.01)", fu="3.0 yr", c="J Clin Oncol 2021;39:1329", p=33555941,
  b="Single-arm phase 2 studies suggested that lenalidomide with R-CHOP was most active in ABC DLBCL.",
  i="A signal-seeking randomized phase 2 trial in which lenalidomide improved PFS across subtypes. It was published alongside the negative phase 3 ROBUST trial, which used a lower dose (15 mg on days 1–14) and enrolled only centrally confirmed ABC disease.",
  q="Why did E1412 and ROBUST differ: dose and schedule, patient selection, or chance in a phase 2 trial? The result did not change practice.",
  cm=[[33621123, "Davies AJ, J Clin Oncol 2021", "Precision Medicine in DLBCL: Are We There Yet?"]],
  reg="No regulatory action; no first-line DLBCL indication for lenalidomide.", gl="Not a standard regimen (NCCN not checked).", acc="—",
  tox="Grade ≥3 thrombocytopenia 34% vs 13%, anaemia 29% vs 20%, febrile neutropenia 25% vs 14% (R2CHOP vs R-CHOP); treatment-related deaths 2 vs 7 (full paper)",
  reg_ids=["NCT01856192"], ft=["pmc", "PMC8078264"], moa=["imidL"]),
 dict(y=2023, n="Smart Start (Westin)", s="nov", ph="Phase 2",
  d="Rituximab, lenalidomide 25 mg on days 1–10 and continuous ibrutinib 560 mg (RLI) for two 21-day cycles without chemotherapy, then RLI with standard chemotherapy for 6 cycles; untreated non-GCB DLBCL; single arm",
  ep="ORR after 2 cycles of RLI alone; CR rate at the end of RLI with chemotherapy",
  r="ORR 86.2% after 2 chemotherapy-free cycles; CR 94.5% at the end of treatment; 2-year PFS 91.3% and OS 96.6%",
  N="60", hr="single arm", fu="31 mo", c="J Clin Oncol 2023;41:745", p=35952327,
  b="PHOENIX and ROBUST each added one targeted drug to full R-CHOP and were negative; laboratory and clinical data suggested that lenalidomide and ibrutinib act together in non-GCB disease.",
  i="Showed that a targeted combination given before any chemotherapy produces a high response rate in newly diagnosed non-GCB DLBCL. Its successor, Smart Stop (NCT04978584), tests rituximab, lenalidomide, acalabrutinib and tafasitamab before and with chemotherapy.",
  q="Single-arm trial of 60 patients, not confirmed in a randomized trial. Can chemotherapy be shortened or omitted in patients who respond to the targeted drugs alone?",
  cm=[[36049146, "Kahl BS, J Clin Oncol 2023", "Management of Diffuse Large B-Cell Lymphoma: Are We Getting Smarter?"]],
  reg="No regulatory action.", gl="Investigational (NCCN not checked).", acc="—",
  tox="not reported in abstract",
  reg_ids=["NCT02636322"], ft=["pmc", "PMC10489211"], moa=["imidL", "btk"]),
 dict(y=2023, n="GUIDANCE-01 (Zhang)", s="nov", ph="Phase 2 (randomized)",
  d="R-CHOP alone or with a targeted agent chosen by simplified genetic subtyping (R-CHOP-X); newly diagnosed intermediate- or high-risk DLBCL. The registry record lists ibrutinib, lenalidomide, tucidinostat (chidamide) and decitabine as the added agents; the abstract does not say which was given for each subtype",
  ep="Complete response rate",
  r="CR 88% vs 66% (P=0.003); ORR 92% vs 73% (P=0.005); 2-year PFS 88% vs 63% (P<0.001); 2-year OS 94% vs 77% (P=0.001)",
  N="128", hr="not reported in abstract", fu="not reported in abstract", c="Cancer Cell 2023;41:1705", p=37774697,
  b="Phase 3 trials that chose the added drug by cell of origin were negative (REMoDL-B, PHOENIX, ROBUST); the genetic subtypes described in 2018 offered a finer way to match a drug to the biology.",
  i="Randomized phase 2 evidence that adding a drug matched to the genetic subtype can improve on R-CHOP, with a subtyping algorithm simple enough to run before treatment.",
  q="Needs phase 3 confirmation. The experimental arm pooled several drugs, so the contribution of each is unknown. Can subtyping be done quickly enough in routine practice?",
  cm=[[37774696, "Hahn CK, Cancer Cell 2023", "Genetically informed therapy for lymphoma: the discomfiting benefit of lumping splits"]],
  reg="No regulatory action.", gl="Investigational (NCCN not checked).", acc="—",
  tox="not reported in abstract",
  reg_ids=["NCT04025593"], ft=["doi", "10.1016/j.ccell.2023.09.004", "free"], moa=["btk", "imidL"]),
]

PAGES = {"dlbu": DLBU}
