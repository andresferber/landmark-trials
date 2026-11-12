TITLE = 'The evolution of first-line treatment of diffuse large B-cell lymphoma, 2000–2026'
UPDATED = 'November 11, 2026'
TL_CAPTION = 'Timeline of key trials and US regulatory milestones'

TAKE = [
    'Adding rituximab to CHOP improved survival at every age and risk level, and R-CHOP every 21 days for 6 cycles became the reference regimen.',
    'For 15 years nothing improved on it: dose density, a different anti-CD20 antibody, infusional chemotherapy, upfront transplant and maintenance all failed to improve survival.',
    'Less treatment is enough for favourable limited-stage disease: 4 cycles of R-CHOP, guided by risk factors or by interim PET.',
    'Adding a targeted drug chosen by cell of origin (bortezomib, ibrutinib, lenalidomide) failed in phase 3 trials.',
    'Three phase 2 trials of targeted drugs with R-CHOP, or given before it (E1412, GUIDANCE-01, Smart Start), suggest that matching a drug to the genetic subtype may work; none has been confirmed in phase 3.',
    'Polatuzumab vedotin in place of vincristine (POLARIX) and tafasitamab-lenalidomide added to R-CHOP (frontMIND) each improved PFS, so far without an overall survival benefit.',
]

TIMELINE = [
    ('2000', 'Gene-expression profiling separates germinal centre and activated B-cell-like DLBCL', 'rr'),
    ('2002', 'R-CHOP improves survival in older patients (GELA LNH-98.5)', 'young'),
    ('2006', 'R-CHOP confirmed in young good-prognosis patients (MInT) and in the US intergroup trial; no benefit from rituximab maintenance', 'young'),
    ('2008', 'Six cycles, not eight (RICOVER-60)', 'young'),
    ('2011', 'R-miniCHOP for patients over 80', 'old'),
    ('2013', 'R-CHOP-14 no better than R-CHOP-21; upfront transplant improves PFS but not survival (S9704)', 'young'),
    ('2017', 'Obinutuzumab no better than rituximab (GOYA)', 'young'),
    ('2019', 'Four cycles for favourable limited stage (FLYER); DA-EPOCH-R no better than R-CHOP; ibrutinib and bortezomib add-on trials negative', 'old'),
    ('2021', 'Lenalidomide add-on negative in phase 3 (ROBUST) but improves PFS in randomized phase 2 (E1412)', 'p2'),
    ('2022', 'Pola-R-CHP improves PFS (POLARIX); first-line CAR-T tested in high-risk disease (ZUMA-12)', 'p2'),
    ('2023', 'FDA approves polatuzumab vedotin with R-CHP for untreated DLBCL', 'p2'),
    ('2023', 'Phase 2: drug chosen by genetic subtype added to R-CHOP (GUIDANCE-01); rituximab, lenalidomide and ibrutinib before chemotherapy (Smart Start)', 'p2'),
    ('2026', 'Tafasitamab-lenalidomide with R-CHOP improves PFS (frontMIND); PET-adapted 4 cycles in low-risk disease (LNH2009-1B)', 'p2'),
]

BODY = """
<h3>A curable disease with one regimen for twenty years</h3>
<p>Diffuse large B-cell lymphoma is curable with first-line treatment in most patients, and those who are not cured do poorly. The history of first-line therapy since 2000 has three parts: the arrival of rituximab, a long series of failed attempts to improve on R-CHOP, and, since 2022, the first positive add-on trials.</p>

<h3>Rituximab changes the standard</h3>
<p>In patients aged 60 to 80, adding rituximab to 8 cycles of CHOP raised the complete response rate from 63% to 76% and improved survival, and at 10 years overall survival was 43.5% vs 27.6% [[GELA LNH-98.5 (Coiffier)]]. The US intergroup trial confirmed the benefit in older patients and showed that rituximab maintenance adds nothing after R-CHOP [[ECOG 4494 / CALGB 9793 (Habermann)]]. MInT extended the result to young patients with good-prognosis disease, with a 3-year event-free survival of 79% vs 59% [[MInT (Pfreundschuh)]], and RICOVER-60 showed that six cycles were as good as eight [[RICOVER-60 (Pfreundschuh)]].</p>

<h3>More intensity did not help</h3>
<p>Giving R-CHOP every 14 days was no better than every 21 days, in adults of all ages [[UK R-CHOP 14 vs 21 (Cunningham)]] and in older patients [[LNH03-6B (Delarue)]]. Extra rituximab early in treatment did not improve outcome [[HOVON-84 (Lugtenburg)]], and the glycoengineered antibody obinutuzumab was not better than rituximab [[GOYA (Vitolo)]]. Infusional dose-adjusted EPOCH-R was more toxic than R-CHOP and no more effective [[Alliance/CALGB 50303 (Bartlett)]]. High-dose therapy with autologous transplant in first remission was not superior to conventional therapy in young high-risk patients [[DSHNHL 2002-1 (Schmitz)]], and in SWOG S9704 it improved 2-year PFS (69% vs 55%) but not overall survival [[SWOG S9704 (Stiff)]]. The one exception was R-ACVBP, which improved 3-year overall survival (92% vs 84%) in patients under 60 with an age-adjusted IPI of 1, at the cost of more toxicity [[LNH03-2B: R-ACVBP (Récher)]].</p>

<h3>Less treatment for favourable disease, and adapted treatment for the very old</h3>
<p>In non-bulky limited-stage disease, radiotherapy after R-CHOP did not improve event-free survival [[LYSA/GOELAMS 02-03 (Lamy)]]. In young patients with no risk factors, 4 cycles of R-CHOP were non-inferior to 6, with a 3-year PFS of 96% [[FLYER (Poeschel)]]. PET-directed therapy gave similar results without an age limit in a US trial [[SWOG S1001 (Persky)]], and a randomized trial in low-risk patients up to age 80 showed that stopping at 4 cycles after a negative PET was non-inferior to 6 cycles [[LNH2009-1B (Michot)]]. Interim PET predicts outcome, but intensifying chemotherapy for PET-positive patients did not help [[PETAL (Dührsen)]].</p>
<p>For patients over 80, reduced-dose R-miniCHOP gave a 2-year overall survival of 59% and became the standard [[R-miniCHOP (Peyrade)]]; adding lenalidomide to it added toxicity without benefit [[SENIOR (Oberic)]]. Lenalidomide maintenance after R-CHOP prolonged PFS in patients aged 60 to 80 but not survival, and was not adopted [[REMARC (Thieblemont)]].</p>

<h3>Biology: from cell of origin to genetic subtypes</h3>
<p>Gene-expression profiling divided DLBCL into germinal centre and activated B-cell-like disease, with different survival [[Cell of origin by gene expression (Alizadeh)]], and an immunohistochemical algorithm brought the distinction into routine pathology [[Hans algorithm (Hans)]]. Clinical risk is still estimated with the IPI and its revisions [[R-IPI (Sehn)]] [[NCCN-IPI (Zhou)]], and CNS risk with the CNS-IPI [[CNS-IPI (Schmitz)]]. MYC rearrangement carries a poor prognosis mainly when combined with BCL2 or BCL6 rearrangement and an immunoglobulin partner [[MYC rearrangement and partner gene (Rosenwald)]]. Genomic studies have since defined genetic subtypes that cut across cell of origin [[Genetic subtypes of DLBCL (Schmitz)]].</p>
<p>Acting on cell of origin was disappointing. Bortezomib added to R-CHOP did not improve PFS, although a later analysis suggested a benefit in activated B-cell and molecular high-grade disease [[REMoDL-B (Davies)]]. Ibrutinib did not improve event-free survival in non-GCB disease, helping patients under 60 and harming older ones [[PHOENIX (Younes)]], and lenalidomide did not improve PFS in activated B-cell disease [[ROBUST (Nowakowski)]].</p>
<p>Three phase 2 trials point to other ways of matching a drug to the biology, none confirmed in phase 3. In ECOG-ACRIN E1412, lenalidomide with R-CHOP improved 3-year PFS (73% vs 61%) across subtypes, at the price of more cytopenias, in the same year that the negative ROBUST trial used a lower dose and enrolled only activated B-cell disease [[ECOG-ACRIN E1412 (Nowakowski)]]. In GUIDANCE-01, 128 patients had a drug chosen by genetic subtype added to R-CHOP; the complete response rate was 88% vs 66% and 2-year PFS 88% vs 63%, with more thrombocytopenia and febrile neutropenia, although the added drug differed by subtype and the benefit of each cannot be separated [[GUIDANCE-01 (Zhang)]]. Smart Start gave rituximab, lenalidomide and ibrutinib for two cycles without chemotherapy to 60 patients with non-germinal centre disease: the response rate was 86.2% before any chemotherapy and 2-year PFS 91.3%, but there was no control arm [[Smart Start (Westin)]].</p>

<h3>The first positive add-on trials</h3>
<p>POLARIX replaced vincristine with polatuzumab vedotin in patients with an IPI of 2 to 5: 2-year PFS was 76.7% vs 70.2% (HR 0.73), and at 5 years 64.9% vs 59.1%, without a significant difference in overall survival [[POLARIX (Tilly)]]. frontMIND added tafasitamab and lenalidomide to R-CHOP in high-intermediate and high-risk disease: 2-year PFS was 71.1% vs 62.9% (HR 0.75), with more grade 3 or higher adverse events (87% vs 76%) and immature survival data [[frontMIND (Lenz)]]. In double-expressor lymphoma, a trial in China reported better event-free survival with the histone deacetylase inhibitor tucidinostat added to R-CHOP (HR 0.72) [[DEB (Xu)]]. First-line CAR-T has been tested only in a single-arm trial in high-risk disease, with complete responses in 78% [[ZUMA-12 (Neelapu)]].</p>

<h3>Where we are now</h3>
<p>Summarized at a high level; NCCN placement was not checked against the current document.</p>
<ul>
<li><b>Favourable limited stage:</b> 4 cycles of R-CHOP, by risk factors [[FLYER (Poeschel)]] or interim PET [[SWOG S1001 (Persky)]] [[LNH2009-1B (Michot)]], usually without radiotherapy.</li>
<li><b>Advanced stage or IPI 2 or higher:</b> 6 cycles of R-CHOP or pola-R-CHP [[POLARIX (Tilly)]].</li>
<li><b>Over 80 or frail:</b> R-miniCHOP [[R-miniCHOP (Peyrade)]].</li>
<li><b>At diagnosis:</b> IPI, cell of origin, FISH for MYC rearrangement, and an estimate of CNS risk [[CNS-IPI (Schmitz)]].</li>
</ul>

<h3>Open questions</h3>
<ul>
<li><b>Who benefits from pola-R-CHP:</b> no overall survival benefit so far, and exploratory analyses point to activated B-cell disease and higher IPI.</li>
<li><b>Which add-on:</b> polatuzumab and tafasitamab-lenalidomide have not been compared, and combinations with bispecific antibodies are in phase 3.</li>
<li><b>Selection by biology:</b> whether genetic subtypes will succeed where cell of origin failed.</li>
<li><b>CNS prophylaxis:</b> the CNS-IPI identifies risk, but no intervention is proven to lower it.</li>
<li><b>High-grade and double-hit lymphoma:</b> treated with intensive regimens on non-randomized data.</li>
</ul>

<h3>What is coming</h3>
<p>Ongoing phase 3 trials (listed under Trials to watch) add CD20×CD3 bispecific antibodies to first-line chemoimmunotherapy: glofitamab with pola-R-CHP (GO44145), epcoritamab with R-CHOP (EPCORE DLBCL-2) and odronextamab with CHOP (OLYMPIA-3). Others test golcadomide (GOLSEEK-1), acalabrutinib in non-GCB disease (ESCALADE) and zilovertamab vedotin (waveLINE-010) with R-CHOP or R-CHP, first-line axicabtagene ciloleucel in high-risk disease (ZUMA-23), and polatuzumab or acalabrutinib with reduced-dose chemotherapy in older patients (POLAR BEAR, ARCHED).</p>
"""
