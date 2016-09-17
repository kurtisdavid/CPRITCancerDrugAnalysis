# openFDA

###Initial Remarks
Thank you to openFDA for getting my project started. However, due to the limitations of the queries, I had to write my own scripts to get the data we needed.

Take a look into their page if you want to consider doing a project similar: https://open.fda.gov/


###File Order

To replicate the process, I suggest going through the files in this order:

__accumulate.py__ - Goes through each JSON file of FAERS provided by openFDA and accumulates the total number of reports where a certain ADE-Drug relationship was found.

__prelim.py__ - Prepped the resultant JSON file in accumulate.py to only save the relationships related to our ACME drug dataset and those with > 10 counts.

__contingency_table.py__ - Calculates the Proportional Reporting Ratios based on the ADE-Drug counts extracted from accumulate.py and prelim.py

### Example Data

I also added some databases that are needed for the project; contact me if you want to look at what the .py files result in making.

__acmeSynonyms.xlsx__ - provided the synonyms for the drug set I worked on. Special thanks to my group for providing this beforehand.

__ADE_Database.xlsx__ - most recent version of the ADEs collected from each SOC that also contains the LLTs

__SOC_counts_MAIN.txt__ - contains the total number of associated reports between the ADEs of each SOC and a certain drug


