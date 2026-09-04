# build_risk_lists.py — consolidate seven standing risk/essential-service lists into one CSV.
#
# Sources (all vendored in data/raw/ or fetched pages, access 2026-08-14; see DATA_NOTES.md):
#   1. US  NSM-22 (2024-04-30) — 16 critical infrastructure sectors            [essential_services]
#   2. NATO seven baseline resilience requirements                             [essential_services]
#   3. Finland Security Strategy for Society — seven vital functions           [essential_services]
#   4. UK  National Risk Register 2025 — risk summaries, contents pp.2-3      [risk_register]
#   5. SWE MSB NRSB 2025 — Tabell 1, p.27 (26 threats)                        [risk_register]
#   6. Lloyd's RDS Scenario Specification, January 2026 — contents + §1.2     [insurance_scenarios]
#   7. WEF Global Risks Report 2026 — Figure 3 top-10 by severity, 2y & 10y   [perception_survey]
#
# Transcription is manual-with-page-refs (lists, not series). The `sector_map` column is OUR
# judgment call mapping each item to the napkin sector set — it is an input to the napkin
# tally, not a fact from the source. `cross_cutting` items are excluded from sector tallies.
#
# House rule note: UK NRR 2025 states "89 risks, within 9 risk themes" (p.11 of the PDF text);
# both the contents pages and a page-title sweep of pp.27-186 yield 88 titled risk summaries.
# We record the 88 transcribed; the one-risk gap is unresolved and reported, not patched.

import pandas as pd

OUT = "data/risk_lists.csv"

SECTORS = [
    "food_agriculture", "energy", "water", "health_social_care", "transport_logistics",
    "communications_it", "finance_insurance", "construction_housing", "manufacturing",
    "defense_public_safety", "education_research", "media_arts_culture",
    "government_admin", "professional_business", "retail_leisure",
]

rows = []

def add(source, jurisdiction, year, list_type, category, item, item_en, ref, sector_map, url):
    for s in sector_map.split(";"):
        assert s in SECTORS + ["cross_cutting"], f"unknown sector {s} for {item}"
    rows.append(dict(source=source, jurisdiction=jurisdiction, year=year, list_type=list_type,
                     category=category, item=item, item_en=item_en, ref=ref,
                     sector_map=sector_map, url=url))

# ---------------------------------------------------------------- 1. US NSM-22 (CISA sectors)
U_NSM = "https://bidenwhitehouse.archives.gov/briefing-room/presidential-actions/2024/04/30/national-security-memorandum-on-critical-infrastructure-security-and-resilience/"
for item, sector in [
    ("Chemical", "manufacturing"),
    ("Commercial Facilities", "retail_leisure"),
    ("Communications", "communications_it"),
    ("Critical Manufacturing", "manufacturing"),
    ("Dams", "water;energy"),
    ("Defense Industrial Base", "defense_public_safety;manufacturing"),
    ("Emergency Services", "defense_public_safety"),
    ("Energy", "energy"),
    ("Financial Services", "finance_insurance"),
    ("Food and Agriculture", "food_agriculture"),
    ("Government Services and Facilities", "government_admin"),
    ("Healthcare and Public Health", "health_social_care"),
    ("Information Technology", "communications_it"),
    ("Nuclear Reactors, Materials, and Waste", "energy"),
    ("Transportation Systems", "transport_logistics"),
    ("Water and Wastewater Systems", "water"),
]:
    add("NSM-22 critical infrastructure sectors", "US", 2024, "essential_services",
        "critical infrastructure sector", item, item, "NSM-22 sector list", sector, U_NSM)

# ---------------------------------------------------------------- 2. NATO baseline requirements
U_NATO = "https://www.nato.int/cps/en/natohq/topics_132722.htm"
for item, sector in [
    ("Assured continuity of government and critical government services", "government_admin"),
    ("Resilient energy supplies", "energy"),
    ("Ability to deal effectively with uncontrolled movement of people", "government_admin;defense_public_safety"),
    ("Resilient food and water resources", "food_agriculture;water"),
    ("Ability to deal with mass casualties and disruptive health crises", "health_social_care"),
    ("Resilient civil communications systems", "communications_it"),
    ("Resilient transport systems", "transport_logistics"),
]:
    add("NATO seven baseline requirements", "NATO", 2016, "essential_services",
        "baseline resilience requirement", item, item, "Resilience & civil preparedness topic page", sector, U_NATO)

# ---------------------------------------------------------------- 3. Finland vital functions
U_FIN = "https://turvallisuuskomitea.fi/en/security-strategy-for-society/vital-functions/"
for item, sector in [
    ("Leadership", "government_admin"),
    ("International and EU activities", "government_admin"),
    ("Defence capability", "defense_public_safety"),
    ("Internal security", "defense_public_safety"),
    ("Economy, infrastructure and security of supply", "energy;food_agriculture;transport_logistics;finance_insurance"),
    ("Functional capacity of the population and services", "health_social_care;government_admin"),
    ("Psychological resilience", "media_arts_culture;education_research"),
]:
    add("Finland Security Strategy for Society — vital functions", "FI", 2017, "essential_services",
        "vital function of society", item, item, "Security Committee vital-functions page", sector, U_FIN)

# ---------------------------------------------------------------- 4. UK National Risk Register 2025
U_NRR = "https://assets.publishing.service.gov.uk/media/67b5f85732b2aab18314bbe4/National_Risk_Register_2025.pdf"
uk = [
    # (theme, item, pdf page, sector_map)
    ("Terrorism", "International terrorist attack", 29, "defense_public_safety"),
    ("Terrorism", "Northern Ireland related terrorism", 30, "defense_public_safety"),
    ("Terrorism", "Terrorist attacks in venues and public spaces: explosive devices", 31, "defense_public_safety"),
    ("Terrorism", "Terrorist attacks in venues and public spaces: marauding attacks", 32, "defense_public_safety"),
    ("Terrorism", "Malicious maritime incident", 33, "transport_logistics;defense_public_safety"),
    ("Terrorism", "Malicious rail incident", 34, "transport_logistics;defense_public_safety"),
    ("Terrorism", "Malicious aviation incident", 35, "transport_logistics;defense_public_safety"),
    ("Terrorism", "Strategic hostage taking", 36, "defense_public_safety"),
    ("Terrorism", "Assassination of a high-profile public figure", 38, "defense_public_safety;government_admin"),
    ("Terrorism", "Chemical, Biological, Radiological and Nuclear (CBRN) attacks", 40, "defense_public_safety;health_social_care"),
    ("Terrorism", "Conventional attack: gas infrastructure", 42, "energy"),
    ("Terrorism", "Cyber attack: gas infrastructure", 43, "energy;communications_it"),
    ("Terrorism", "Conventional attack: electricity infrastructure", 44, "energy"),
    ("Terrorism", "Cyber attack: electricity infrastructure", 45, "energy;communications_it"),
    ("Terrorism", "Conventional attack: civil nuclear", 46, "energy"),
    ("Terrorism", "Cyber attack: civil nuclear", 47, "energy;communications_it"),
    ("Terrorism", "Conventional attack: fuel supply infrastructure", 48, "energy"),
    ("Terrorism", "Cyber attack: fuel supply infrastructure", 49, "energy;communications_it"),
    ("Terrorism", "Attack on government", 50, "government_admin"),
    ("Cyber", "Cyber attack: health and social care system", 52, "health_social_care;communications_it"),
    ("Cyber", "Cyber attack: transport sector", 54, "transport_logistics;communications_it"),
    ("Cyber", "Cyber attack: telecommunications systems", 55, "communications_it"),
    ("State threats", "Malicious attacks: UK financial CNI", 58, "finance_insurance"),
    ("State threats", "Cyber attack: UK retail bank", 59, "finance_insurance;communications_it"),
    ("State threats", "Total loss of transatlantic telecommunications cables", 60, "communications_it"),
    ("Geographic and diplomatic risks", "Disruption of Russian gas supplies to Europe", 62, "energy"),
    ("Geographic and diplomatic risks", "Disruption to global oil trade routes", 63, "energy;transport_logistics"),
    ("Accidents and systems failures", "Major adult social care provider failure", 65, "health_social_care"),
    ("Accidents and systems failures", "Insolvency of supplier(s) of critical services to the public sector", 67, "government_admin;professional_business"),
    ("Accidents and systems failures", "Insolvency affecting fuel supply", 69, "energy"),
    ("Accidents and systems failures", "Rail accident", 71, "transport_logistics"),
    ("Accidents and systems failures", "Large passenger vessel accident", 73, "transport_logistics"),
    ("Accidents and systems failures", "Major maritime pollution incident", 75, "transport_logistics;water"),
    ("Accidents and systems failures", "Incident (grounding/sinking) of a vessel blocking a major port", 77, "transport_logistics;food_agriculture"),
    ("Accidents and systems failures", "Accident involving high-consequence dangerous goods", 79, "transport_logistics;manufacturing"),
    ("Accidents and systems failures", "Aviation collision", 81, "transport_logistics"),
    ("Accidents and systems failures", "Malicious drone incident", 83, "transport_logistics;defense_public_safety"),
    ("Accidents and systems failures", "Disruption of space-based services", 84, "communications_it"),
    ("Accidents and systems failures", "Loss of Positioning, Navigation and Timing (PNT) services", 86, "communications_it;transport_logistics"),
    ("Accidents and systems failures", "Simultaneous loss of all fixed and mobile forms of communication", 88, "communications_it"),
    ("Accidents and systems failures", "Failure of the National Electricity Transmission System (NETS)", 90, "energy"),
    ("Accidents and systems failures", "Regional failure of the electricity network", 92, "energy"),
    ("Accidents and systems failures", "Failure of gas supply infrastructure", 94, "energy"),
    ("Accidents and systems failures", "Civil nuclear accident", 96, "energy"),
    ("Accidents and systems failures", "Radiation release from overseas nuclear site", 98, "energy;health_social_care"),
    ("Accidents and systems failures", "Radiation exposure from transported, stolen or lost goods", 100, "health_social_care;defense_public_safety"),
    ("Accidents and systems failures", "Technological failure at a systemically important retail bank", 102, "finance_insurance"),
    ("Accidents and systems failures", "Technological failure at a UK critical financial market infrastructure", 104, "finance_insurance"),
    ("Accidents and systems failures", "Accidental fire or explosion at an onshore major hazard (COMAH) site", 106, "manufacturing"),
    ("Accidents and systems failures", "Accidental large toxic chemical release from an onshore major hazard (COMAH) site", 108, "manufacturing;health_social_care"),
    ("Accidents and systems failures", "Accidental fire or explosion on an offshore oil or gas installation", 110, "energy"),
    ("Accidents and systems failures", "Accidental fire or explosion at an onshore fuel pipeline", 112, "energy"),
    ("Accidents and systems failures", "Accidental fire or explosion at an onshore major accident hazard pipeline", 114, "energy"),
    ("Accidents and systems failures", "Accidental work-related (laboratory) release of a hazardous pathogen", 116, "health_social_care;education_research"),
    ("Accidents and systems failures", "Reservoir/dam collapse", 118, "water;energy"),
    ("Accidents and systems failures", "Water infrastructure failure or loss of drinking water", 120, "water"),
    ("Accidents and systems failures", "Food supply contamination", 122, "food_agriculture"),
    ("Accidents and systems failures", "Major fire", 124, "defense_public_safety;construction_housing"),
    ("Natural and environmental hazards", "Wildfire", 127, "defense_public_safety;food_agriculture"),
    ("Natural and environmental hazards", "Volcanic eruption", 129, "cross_cutting"),
    ("Natural and environmental hazards", "Earthquake", 131, "cross_cutting"),
    ("Natural and environmental hazards", "Humanitarian crisis overseas: natural hazard event", 133, "government_admin"),
    ("Natural and environmental hazards", "Disaster response in Overseas Territories", 135, "government_admin;defense_public_safety"),
    ("Natural and environmental hazards", "Severe space weather", 137, "energy;communications_it"),
    ("Natural and environmental hazards", "Storms", 139, "energy;construction_housing"),
    ("Natural and environmental hazards", "High temperatures and heatwaves", 141, "health_social_care;water;energy"),
    ("Natural and environmental hazards", "Low temperatures and snow", 143, "energy;transport_logistics;health_social_care"),
    ("Natural and environmental hazards", "Coastal flooding", 145, "water;construction_housing"),
    ("Natural and environmental hazards", "Fluvial flooding", 147, "water;construction_housing"),
    ("Natural and environmental hazards", "Surface water flooding", 149, "water;construction_housing"),
    ("Natural and environmental hazards", "Drought", 151, "water;food_agriculture"),
    ("Natural and environmental hazards", "Poor air quality", 153, "health_social_care"),
    ("Human, animal and plant health", "Pandemic", 156, "health_social_care"),
    ("Human, animal and plant health", "Outbreak of an emerging infectious disease", 158, "health_social_care"),
    ("Human, animal and plant health", "Animal disease: major outbreak of foot and mouth disease", 160, "food_agriculture"),
    ("Human, animal and plant health", "Animal disease: major outbreak of highly pathogenic avian influenza", 162, "food_agriculture;health_social_care"),
    ("Human, animal and plant health", "Animal disease: major outbreak of African horse sickness", 164, "food_agriculture"),
    ("Human, animal and plant health", "Animal disease: major outbreak of African swine fever", 166, "food_agriculture"),
    ("Human, animal and plant health", "Major outbreak of plant pest: Xylella fastidiosa", 168, "food_agriculture"),
    ("Human, animal and plant health", "Major outbreak of plant pest: Agrilus planipennis", 170, "food_agriculture"),
    ("Societal", "Public disorder", 173, "defense_public_safety"),
    ("Societal", "Industrial action", 175, "cross_cutting"),
    ("Societal", "Reception and integration of British Nationals arriving from overseas", 177, "government_admin"),
    ("Conflict and instability", "Deliberate disruption of UK space systems and space-based services", 180, "communications_it;defense_public_safety"),
    ("Conflict and instability", "Attack on a UK ally or partner outside NATO or a mutual security agreement requiring international assistance", 182, "defense_public_safety"),
    ("Conflict and instability", "Attack against a NATO ally or UK deployed forces, which meets the Article 5 threshold", 183, "defense_public_safety"),
    ("Conflict and instability", "Conventional attack on the UK mainland or overseas territories", 184, "defense_public_safety"),
    ("Conflict and instability", "Nuclear miscalculation not involving the UK or its allies", 185, "defense_public_safety"),
]
for theme, item, page, sector in uk:
    add("UK National Risk Register 2025", "UK", 2025, "risk_register", theme, item, item,
        f"NRR 2025 p.{page}", sector, U_NRR)

# ---------------------------------------------------------------- 5. Sweden MSB NRSB 2025, Tabell 1
U_MSB = "https://rib.msb.se/filer/pdf/31068.pdf"
msb = [
    ("Biologiska hot", "Epidemi", "Epidemic", "health_social_care"),
    ("Biologiska hot", "Epizooti", "Epizootic (major animal disease outbreak)", "food_agriculture"),
    ("Natur- och miljöhot", "Skogs- och vegetationsbrand", "Forest and vegetation fire", "defense_public_safety;food_agriculture"),
    ("Natur- och miljöhot", "Skyfall", "Cloudburst / extreme rainfall", "water;construction_housing"),
    ("Natur- och miljöhot", "Solstorm", "Solar storm", "energy;communications_it"),
    ("Natur- och miljöhot", "Storm", "Storm", "energy;construction_housing"),
    ("Natur- och miljöhot", "Värmebölja och torka", "Heatwave and drought", "water;food_agriculture;health_social_care"),
    ("Teknologiska hot", "Dammhaveri", "Dam failure", "water;energy"),
    ("Teknologiska hot", "It-incident", "IT incident", "communications_it"),
    ("Teknologiska hot", "Kemikalieolycka", "Chemical accident", "manufacturing;health_social_care"),
    ("Teknologiska hot", "Kärnteknisk olycka", "Nuclear accident", "energy"),
    ("Teknologiska hot", "Maritim olycka", "Maritime accident", "transport_logistics"),
    ("Teknologiska hot", "Nätsammanbrott i elsystemet", "Collapse of the electricity grid", "energy"),
    ("Sociala och ekonomiska hot", "Händelse utomlands", "Incident abroad", "government_admin"),
    ("Sociala och ekonomiska hot", "Okontrollerade befolkningsrörelser", "Uncontrolled population movements", "government_admin;defense_public_safety"),
    ("Sociala och ekonomiska hot", "Störning i internationella handelsflöden", "Disruption of international trade flows", "transport_logistics;food_agriculture;manufacturing"),
    ("Sociala och ekonomiska hot", "Våldsamt upplopp", "Violent riot", "defense_public_safety"),
    ("Säkerhetshot", "CBRN-attentat", "CBRN attack", "defense_public_safety;health_social_care"),
    ("Säkerhetshot", "Cyberangrepp", "Cyberattack", "communications_it"),
    ("Säkerhetshot", "Otillbörlig informationspåverkan", "Improper information influence", "media_arts_culture;government_admin"),
    ("Säkerhetshot", "Sabotage mot kritisk infrastruktur", "Sabotage of critical infrastructure", "energy;water;communications_it;transport_logistics"),
    ("Säkerhetshot", "Terrorattentat", "Terrorist attack", "defense_public_safety"),
    ("Militära hot", "Väpnat angrepp – Strid utanför Sverige inom ramen för Nato", "Armed attack – combat outside Sweden within NATO", "defense_public_safety"),
    ("Militära hot", "Väpnat angrepp – Fjärrangrepp", "Armed attack – long-range strike", "defense_public_safety"),
    ("Militära hot", "Väpnat angrepp – Strid på svenskt territorium", "Armed attack – combat on Swedish territory", "defense_public_safety"),
    ("Militära hot", "Väpnat angrepp – Kärnvapenangrepp", "Armed attack – nuclear attack", "defense_public_safety"),
]
for cat, item, item_en, sector in msb:
    add("MSB Nationell risk- och sårbarhetsbedömning 2025", "SE", 2025, "risk_register",
        cat, item, item_en, "NRSB 2025 Tabell 1, p.27", sector, U_MSB)

# ---------------------------------------------------------------- 6. Lloyd's RDS January 2026
U_RDS = "https://assets.lloyds.com/media-651c0e64-c1d0-4f97-90f7-883c69fe2ef2/7b37ea26-64e2-4a67-915b-36168145a1b2/2.%20RDS%20Scenario%20Specification%20-%20January%202026%20(1).pdf"
rds = [
    ("Compulsory", "Two events – North East windstorm", "cross_cutting"),
    ("Compulsory", "Two events – South Carolina windstorm", "cross_cutting"),
    ("Compulsory", "Florida windstorm – Miami-Dade", "cross_cutting"),
    ("Compulsory", "Florida windstorm – Pinellas", "cross_cutting"),
    ("Compulsory", "Gulf of Mexico windstorm (onshore and offshore energy)", "energy"),
    ("Compulsory", "European windstorm", "cross_cutting"),
    ("Compulsory", "Japanese typhoon", "cross_cutting"),
    ("Compulsory", "California earthquake – Los Angeles", "cross_cutting"),
    ("Compulsory", "California earthquake – San Francisco", "cross_cutting"),
    ("Compulsory", "New Madrid earthquake", "cross_cutting"),
    ("Compulsory", "Japanese earthquake", "cross_cutting"),
    ("Compulsory", "UK flood", "water;construction_housing"),
    ("Compulsory", "Terrorism – Rockefeller Center", "defense_public_safety"),
    ("Compulsory", "Terrorism – One World Trade Center", "defense_public_safety"),
    ("Compulsory", "Alternative scenario A", "cross_cutting"),
    ("Compulsory", "Alternative scenario B", "cross_cutting"),
    ("Compulsory", "Cyber – Major data security breach", "communications_it"),
    ("Compulsory", "Cyber – Business Blackout II (power grid cyber outage)", "energy;communications_it"),
    ("Compulsory", "Cyber – Cloud Cascade (major cloud provider failure)", "communications_it"),
    ("Compulsory", "Cyber – Ransomware Contagion", "communications_it"),
    ("Syndicate-specific", "Marine scenarios", "transport_logistics"),
    ("Syndicate-specific", "Loss of major complex", "manufacturing;energy"),
    ("Syndicate-specific", "Aviation collision", "transport_logistics"),
    ("Syndicate-specific", "Satellite risks", "communications_it"),
    ("Syndicate-specific", "Liability risks", "finance_insurance"),
    ("Syndicate-specific", "Political risks", "government_admin"),
]
for cat, item, sector in rds:
    add("Lloyd's Realistic Disaster Scenarios (January 2026)", "Lloyd's market", 2026,
        "insurance_scenarios", cat, item, item, "RDS Scenario Specification 2026, contents + §1.2", sector, U_RDS)

# ---------------------------------------------------------------- 7. WEF Global Risks Report 2026, Fig. 3
U_WEF = "https://reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf"
wef_2y = [
    ("Geoeconomic confrontation", "government_admin;finance_insurance"),
    ("Misinformation and disinformation", "media_arts_culture;communications_it"),
    ("Societal polarization", "cross_cutting"),
    ("Extreme weather events", "cross_cutting"),
    ("State-based armed conflict", "defense_public_safety"),
    ("Cyber insecurity", "communications_it"),
    ("Inequality", "cross_cutting"),
    ("Erosion of human rights and/or of civic freedoms", "government_admin"),
    ("Pollution", "health_social_care;water"),
    ("Involuntary migration or displacement", "government_admin"),
]
wef_10y = [
    ("Extreme weather events", "cross_cutting"),
    ("Biodiversity loss and ecosystem collapse", "food_agriculture"),
    ("Critical change to Earth systems", "cross_cutting"),
    ("Misinformation and disinformation", "media_arts_culture;communications_it"),
    ("Adverse outcomes of AI technologies", "communications_it;government_admin"),
    ("Natural resource shortages", "water;energy;food_agriculture"),
    ("Inequality", "cross_cutting"),
    ("Cyber insecurity", "communications_it"),
    ("Societal polarization", "cross_cutting"),
    ("Pollution", "health_social_care;water"),
]
for rank, (item, sector) in enumerate(wef_2y, 1):
    add("WEF Global Risks Report 2026", "global", 2026, "perception_survey",
        f"top-10 severity, 2-year horizon (rank {rank})", item, item, "GRR 2026 Figure 3, p.9", sector, U_WEF)
for rank, (item, sector) in enumerate(wef_10y, 1):
    add("WEF Global Risks Report 2026", "global", 2026, "perception_survey",
        f"top-10 severity, 10-year horizon (rank {rank})", item, item, "GRR 2026 Figure 3, p.9", sector, U_WEF)

# ---------------------------------------------------------------- write + report
df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(f"wrote {OUT}: {len(df)} items from {df.source.nunique()} sources")
print(df.groupby(["source"]).size().to_string())
assert (df[df.source.str.startswith("MSB")].shape[0]) == 26
assert (df[df.source.str.startswith("NSM")].shape[0]) == 16
assert (df[df.source.str.startswith("NATO")].shape[0]) == 7
assert (df[df.source.str.startswith("Finland")].shape[0]) == 7
print("UK NRR items transcribed:", df[df.source.str.startswith('UK')].shape[0],
      "(document states 89; see header note)")
