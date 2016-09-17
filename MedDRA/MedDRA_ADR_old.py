# Goal of this file: With the listed System Organ classes in the list MedDRA, collect their "Preferred Terms"
# This version was incomplete however, in that it did not paginate through the API queries
#    MedDRA_ADR.py fixes this limitation (still uses similar algorithms)


from urllib2 import Request, urlopen, URLError
import urllib
from openpyxl import load_workbook, Workbook
import json

# Sets up the variables needed to enter recurse()
# the ids list helps to keep track of what MedDRA level the recursion is currently on
def main():

	MedDRA = ["Infections and infestations", "Metabolism and nutrition disorders", "Musculoskeletal and connective tissue disorders", "Neoplasms benign, malignant and unspecified (incl cysts and polyps)", "Pregnancy, puerperium and perinatal conditions", "Psychiatric disorders", 
	"Renal and urinary disorders", "Reproductive system and breast disorders","Respiratory, thoracic and mediastinal disorders", 
	"Skin and subcutaneous tissue disorders", "Vascular disorders"]

	for SOC in MedDRA:

		print(SOC)

		orig = SOC

		correct_SOC = SOC.replace(" ","_").replace(",","")

		name =  "ADR_" + correct_SOC + ".txt"

		file = open(name, "w")

		ids = []

		orig = orig.replace(" ", "%20")

		url = "http://data.bioontology.org/search?q=" + orig +"&ontologies=MEDDRA&apikey=3cb45b79-b7dd-42ab-8f44-394434267e1b"
		request = Request(url)
		response = urlopen(request)
		report = response.read()
		parsed_json = json.loads(report)
		ids.append(parsed_json["collection"][0]["@id"].split("/")[-1])

		

		new_url = parsed_json["collection"][0]["links"]["children"]

		recurse(new_url,ids,[],file)
		file.close()



# ADRs are collected by sending pointers to the same original list from main
# ids are copied from original m_ids, to make sure the lists don't overlap
def recurse(link, m_ids, ADRs, file):

	ids = m_ids[:]


	url = link
	request = Request(url, headers= {"Authorization": "apikey token=3cb45b79-b7dd-42ab-8f44-394434267e1b"})
	response = urlopen(request)
	report = response.read()
	parsed_json = json.loads(report)

	collection = parsed_json["collection"]

#base case: if the "collection" entry is empty, we know that the previous level contained the Preferred Terms (since they have no children)
#       thus, to get their IDs, we go back 2 spots in the ids list, to the level just before the Preferred Terms
#       since it is the level before, this means that every child has to be a Preferred Term; now we can collect

	if collection==[]:

		correct_url = "http://data.bioontology.org/ontologies/MEDDRA/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F" + str(ids[-2]) + "/children"
		correct_request = Request(correct_url, headers= {"Authorization": "apikey token=3cb45b79-b7dd-42ab-8f44-394434267e1b"})
		correct_response = urlopen(correct_request)
		correct_report = correct_response.read()
		correct_parsed = json.loads(correct_report)

		collection = correct_parsed["collection"]

		for i in range(len(collection)):

			if collection[i]["prefLabel"] not in ADRs:

				ADRs.append(collection[i]["prefLabel"])
				file.write(collection[i]["prefLabel"] + "\n")

		print(len(ADRs))

# recursive case: all the terms of the current level are recorded, and applies recurse to each so that every branch is travelled on
#       if the names of the level are already within the ADRs list (this can only happen if we are on the level of "Preferred Terms")
#               to save time, since we know all of the Preferred Terms are collected at once, we can stop the current path and begin backtracking
#       if not, then just continues on looking at the children (depth first search for the tree)
#               eventually backtracks once each leaf has been traversed of a certain path
#       because ids were unique for each call, the backtracked ids list should be unchanged; letting new paths be traversed
	else:

		names = []

		for i in range(len(collection)):

			names.append(collection[i]["prefLabel"])

	
		for i in range(len(collection)):

			if not set(names)<=set(ADRs):

				new_ids = m_ids[:]
				new_ids.append(collection[i]["@id"].split("/")[-1])

				new_url = parsed_json["collection"][i]["links"]["children"]

				recurse(new_url, new_ids, ADRs, file)

			else:

				break

	return ADRs

main()
