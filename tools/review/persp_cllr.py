TITLE = 'The evolution of treatment for relapsed chronic lymphocytic leukemia, 2002–2026'
UPDATED = 'November 12, 2026 · Pilot draft, pending review'
TL_CAPTION = 'Timeline of key trials and US regulatory milestones'

TAKE = [
    'Before targeted therapy, relapsed CLL was treated with chemoimmunotherapy or antibodies, with short remissions, especially in fludarabine-refractory and del(17p) disease.',
    'Ibrutinib improved survival over ofatumumab (RESONATE). The more selective covalent BTK inhibitors are as effective or more, with fewer cardiac events (ELEVATE-RR, ALPINE).',
    'Two years of venetoclax-rituximab established fixed-duration treatment at relapse and improved survival over bendamustine-rituximab (MURANO).',
    'PI3K inhibitors prolonged PFS, but infections, immune-mediated toxicity and a possible survival detriment with duvelisib left them a late-line role at most.',
    'After a covalent BTK inhibitor, the options are venetoclax-based therapy or pirtobrutinib; after both classes, pirtobrutinib if not yet used, or CAR T cells. Remissions there are still short.',
    'Most patients now receive a BTK inhibitor or venetoclax as first treatment, so the choice at relapse depends mainly on what was given before and why it was stopped.',
]

TIMELINE = [
    ('2002', 'Alemtuzumab is active after fludarabine has failed', 'old'),
    ('2010', 'FCR better than FC at relapse (REACH); ofatumumab for refractory disease', 'old'),
    ('2013', 'Ibrutinib gives durable responses whatever the genetic risk (PCYC-1102)', 'young'),
    ('2014', 'Ibrutinib improves survival over ofatumumab (RESONATE); FDA approves ibrutinib and idelalisib-rituximab (Study 116)', 'young'),
    ('2016', 'FDA approves venetoclax for CLL with del(17p) (M13-982); acalabrutinib enters trials (ACE-CL-001)', 'p2'),
    ('2018', 'Fixed-duration venetoclax-rituximab (MURANO); venetoclax works after ibrutinib (M14-032); FDA approves duvelisib (DUO)', 'p2'),
    ('2020', 'Acalabrutinib better than idelalisib-rituximab or bendamustine-rituximab (ASCEND)', 'young'),
    ('2021', 'Acalabrutinib not inferior to ibrutinib, with fewer cardiac events (ELEVATE-RR)', 'young'),
    ('2022', 'FDA warns of a possible increased risk of death with duvelisib', 'rr'),
    ('2023', 'Zanubrutinib superior to ibrutinib (ALPINE); pirtobrutinib after a covalent BTK inhibitor (BRUIN); CAR T cells (TRANSCEND CLL 004)', 'rr'),
    ('2025', 'Pirtobrutinib better than older regimens after a covalent BTK inhibitor (BRUIN CLL-321); FDA traditional approval', 'rr'),
    ('2026', 'Pirtobrutinib compared with ibrutinib (BRUIN CLL-314); fixed-duration pirtobrutinib-venetoclax-rituximab (BRUIN CLL-322)', 'p2'),
]

BODY = """
<h3>Before targeted therapy</h3>
<p>Until 2013, treatment of relapsed CLL repeated what had been used first line. In fit patients, adding rituximab to fludarabine and cyclophosphamide lengthened median PFS from 20.6 to 30.6 months [[REACH (Robak)]]. Once fludarabine had failed, the options were antibodies. Alemtuzumab gave responses in 33% of patients, with a median time to progression of 4.7 months [[Alemtuzumab after fludarabine (Keating)]], and ofatumumab gave a median PFS under 6 months in disease refractory to fludarabine [[Hx-CD20-406 (Wierda)]]. These numbers are the background against which the targeted drugs were judged, and ofatumumab became their comparator.</p>

<h3>BTK inhibitors</h3>
<p>Ibrutinib changed the outlook within two years. In its phase 1b/2 trial, 71% of heavily pretreated patients responded, with or without del(17p), and 75% were progression-free at 26 months [[PCYC-1102 (Byrd)]]. RESONATE then showed better PFS and overall survival than ofatumumab; in the final analysis median PFS was 44.1 months against 8.1 [[RESONATE (Byrd)]]. Adding ibrutinib to bendamustine-rituximab also improved PFS and survival, but HELIOS had no ibrutinib-alone arm, and the combination did not replace ibrutinib alone [[HELIOS (Chanan-Khan)]].</p>
<p>Continuous ibrutinib had two limits. One was toxicity: in the final RESONATE analysis, 21% of patients had hypertension and 12% atrial fibrillation [[RESONATE (Byrd)]]. The other was resistance. Sequencing at relapse found a mutation of BTK at the cysteine where the drug binds (C481S) in 5 of 6 patients, and mutations of PLCG2, just downstream, in 2 [[BTK and PLCG2 resistance mutations (Woyach)]]. That finding is the rationale for the noncovalent inhibitors and the BTK degraders that came later.</p>

<h3>Which BTK inhibitor?</h3>
<p>Acalabrutinib was designed to be more selective. After a phase 1/2 trial with a response rate of 95% [[ACE-CL-001 (Byrd)]], ASCEND showed longer PFS than idelalisib-rituximab or bendamustine-rituximab, with a 42-month PFS of 62% against 19% [[ASCEND (Ghia)]]. Three trials then compared BTK inhibitors directly. In ELEVATE-RR, in patients with del(17p) or del(11q), acalabrutinib was not inferior to ibrutinib, with a median PFS of 38.4 months in both arms and less atrial fibrillation, 9.4% against 16.0% [[ELEVATE-RR (Byrd)]]. In ALPINE, zanubrutinib gave longer PFS than ibrutinib, with a hazard ratio of 0.68 at 42.5 months, and fewer cardiac events [[ALPINE (Brown)]]. In BRUIN CLL-314, which enrolled both relapsed and untreated patients, the response rate with the noncovalent inhibitor pirtobrutinib was not inferior to that with ibrutinib, again with less atrial fibrillation and hypertension; its PFS data are not mature [[BRUIN CLL-314 (Woyach)]].</p>
<p>These trials are the reason acalabrutinib and zanubrutinib are generally preferred to ibrutinib, in relapsed and in untreated disease. Acalabrutinib and zanubrutinib have not been compared with each other.</p>

<h3>Venetoclax and fixed-duration treatment</h3>
<p>Venetoclax kills CLL cells by inhibiting BCL2, without needing p53. In its phase 1 trial 79% of patients responded and 20% reached complete remission; tumor lysis syndrome in the first cohorts led to the weekly dose ramp-up still in use [[M12-175 (Roberts)]]. Given continuously to patients with del(17p), it produced responses in 79.4%, and with six years of follow-up median PFS was 28.2 months [[M13-982 (Stilgenbauer)]]. MURANO turned it into a fixed-duration treatment: two years of venetoclax with rituximab for the first six months gave a 2-year PFS of 84.9% against 36.3% with bendamustine-rituximab. In the final analysis, median PFS was 54.7 months against 17.0, and 7-year survival 69.6% against 51.0% [[MURANO (Seymour)]]. Patients with undetectable MRD at the end of treatment had the longest remissions, and retreatment with the same regimen produced responses in 72% of 25 patients [[MURANO (Seymour)]].</p>
<p>MURANO enrolled almost no patients previously treated with a BTK inhibitor. The evidence that venetoclax works after ibrutinib came from a phase 2 trial, with a response rate of 65% [[M14-032 (Jones)]], and from VENICE-1, where complete remission was reached by 35% of patients not previously treated with a B-cell receptor pathway inhibitor and 27% of those who were [[VENICE-1 (Kater)]]. A phase 1b trial then combined pirtobrutinib with venetoclax for a fixed 25 cycles, with or without rituximab, with responses in 93.3% and 100% of 25 patients [[BRUIN phase 1b: pirtobrutinib-venetoclax (Roeker)]]. BRUIN CLL-322 took the triplet to a randomized trial against venetoclax-rituximab, in which 80% of patients had received a covalent BTK inhibitor: adding pirtobrutinib raised 24-month PFS from 72% to 87% [[BRUIN CLL-322 (Davids)]]. Whether the doublet without rituximab does as well is being studied.</p>

<h3>PI3K inhibitors: a cautionary story</h3>
<p>Idelalisib with rituximab was highly effective in frail patients with relapsed CLL, with a hazard ratio for progression of 0.15 and better survival at 12 months than rituximab alone [[Study 116 (Furman)]]. But combining it with bendamustine-rituximab or with ofatumumab brought more serious infections and more deaths from adverse events [[Study 115 (Zelenetz)]] [[Study 119 (Jones)]], and in ASCEND two thirds of patients stopped idelalisib-rituximab because of adverse events [[ASCEND (Ghia)]]. Duvelisib improved PFS over ofatumumab, 13.3 against 9.9 months [[DUO (Flinn)]]; in 2022 the FDA warned that the final survival analysis pointed the other way, and its advisory committee judged the balance of benefit and risk unfavorable. A third drug of the class, umbralisib, was tested with ublituximab in UNITY-CLL, which has not been published in full; umbralisib was withdrawn in 2022. The lesson went beyond CLL: PFS can improve while survival does not, and drugs for a disease with long survival need randomized data on overall survival.</p>

<h3>After a BTK inhibitor, and after both classes</h3>
<p>Pirtobrutinib binds BTK reversibly, at a site not affected by the usual resistance mutation. In patients already treated with a BTK inhibitor, 73.3% responded and median PFS was 19.6 months [[BRUIN (Mato)]]. The randomized trial that followed, in patients all previously treated with a covalent BTK inhibitor, showed a median PFS of 14 months against 8.7 with idelalisib-rituximab or bendamustine-rituximab, with no difference in survival [[BRUIN CLL-321 (Sharman)]]. The second number matters as much as the first: older regimens do little after a BTK inhibitor.</p>
<p>For patients whose disease has progressed on a BTK inhibitor and after venetoclax, lisocabtagene maraleucel produced complete remissions in 18%, and in a later cohort given with ibrutinib in 45% [[TRANSCEND CLL 004 (Siddiqi)]]. Allogeneic transplant remains an option for selected fit patients at this stage and for Richter transformation, which is not covered here and will be a separate section. Maintenance after chemoimmunotherapy, with lenalidomide or an anti-CD20 antibody, prolonged PFS in randomized trials but lost its place when continuous and fixed-duration targeted therapy arrived.</p>

<h3>Where we are now</h3>
<p>This is a personal summary, not a guideline; NCCN placements were not checked against the current document.</p>
<ul>
<li><b>Before treatment:</b> repeat FISH for del(17p) and TP53 sequencing, since both can be acquired; relapse alone is not an indication to treat.</li>
<li><b>After chemoimmunotherapy only:</b> a continuous BTK inhibitor (acalabrutinib or zanubrutinib) or fixed-duration venetoclax-rituximab, chosen as in first-line treatment.</li>
<li><b>After a fixed-duration venetoclax regimen with a long remission:</b> a BTK inhibitor, or venetoclax-based retreatment [[MURANO (Seymour)]].</li>
<li><b>After a covalent BTK inhibitor stopped for intolerance:</b> another BTK inhibitor or venetoclax-based therapy.</li>
<li><b>After progression on a covalent BTK inhibitor:</b> venetoclax-based therapy or pirtobrutinib [[M14-032 (Jones)]] [[BRUIN CLL-321 (Sharman)]].</li>
<li><b>After both a covalent BTK inhibitor and venetoclax:</b> pirtobrutinib if not yet used, lisocabtagene maraleucel, a clinical trial, and transplant evaluation in fit patients [[BRUIN (Mato)]] [[TRANSCEND CLL 004 (Siddiqi)]].</li>
<li><b>PI3K inhibitors and chemoimmunotherapy:</b> late-line options at most.</li>
</ul>

<h3>Open questions</h3>
<ul>
<li><b>Sequence:</b> venetoclax-based therapy or pirtobrutinib first after a covalent BTK inhibitor? No trial has compared them.</li>
<li><b>Pirtobrutinib earlier:</b> if a noncovalent inhibitor is used first, or in a fixed-duration triplet, what works at the next relapse [[BRUIN CLL-314 (Woyach)]] [[BRUIN CLL-322 (Davids)]]?</li>
<li><b>Retreatment:</b> how often, and after how long a remission, can a fixed-duration regimen be repeated?</li>
<li><b>Disease refractory to both classes:</b> remissions are short with every current option; this is where BTK degraders and other new agents are being tested.</li>
<li><b>Survival:</b> most recent trials show PFS gains without survival differences, with crossover; the PI3K story is the reason to keep asking for survival data.</li>
<li><b>Richter transformation:</b> not covered here; it will be a separate section built later.</li>
</ul>

<h3>What is coming</h3>
<p>Ongoing phase 3 trials (listed under Trials to watch) test BTK degraders against pirtobrutinib (BGB-16673-304, NX-5948-306) and against older regimens after both drug classes (CaDAnCe-302), the BCL2 inhibitor sonrotoclax with an anti-CD20 antibody against venetoclax-rituximab (BGB-11417-303), and the noncovalent BTK inhibitor nemtabrutinib with venetoclax against venetoclax-rituximab (BELLWAVE-010). Early data on these agents are under New drugs to watch.</p>
"""
