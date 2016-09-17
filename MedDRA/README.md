# MedDRA - Medical Dictionary for Regulatory Activities

## Some Vocab:
SOC - System Organ Class
ADR - Adverse Drug Reaction (project really uses ADEs, but I misnamed these)
ADE - Adverse Drug Event
PT - Preferred Terms (synonymous to ADE, but this is how MedDRA classifies them)
LLT - Lower level terms (synonyms to PTs, the PTs actually classify LLT according to MedDRA hierarchy)

## Structure of MedDRA:

Contains a hierarchy of terms which I will list: (starting from topmost to bottom)

System Organ Class
Higher Level Group Term
Higher Level Term
Preferred Term
Lower Level Term



Only 21 SOCs were looped through using the BioPortal API (so not a complete SOC - ADE database extractor)

BioPortal did NOT map the lower level terms, however I was able to add those in by scraping the information from their PT webpages.

Due to the hierarchal system, the entries are all connected through branches of trees, and the following files recursively traverse the branches of each SOC to reach the desired PTs.

### MedDRA_ADR.py
Most recent version that collects every ADE. The only difference is that it is able to paginate through the query results. (Much quicker too, since old file already collected most of the ADEs)

### MedDRA_ADR_old.py
Collected the ADEs from the desired SOCs and saved each in their own .txt files.


### Contact me if you want a copy of the collected data. It will be in .xlsx (Excel) format.
