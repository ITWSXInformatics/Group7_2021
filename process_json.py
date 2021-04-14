import json
import pandas

'''
Helper function to create a dictionary, should only be called within this file
'''
def create_dict(vac_dict):
	state_dict = dict()
	for item in vac_dict["data"]:
		if item[8] not in state_dict.keys():
			state_dict[item[8]] = float(item[10])
		else:
			state_dict[item[8]] += float(item[10])
	return state_dict

'''
Converts json files to dictionaries
Takes in nothing, returns dictionary with keys being state name, and the value is the amount of vaccines distributed
Example:
full_vac_dict['Alaska'] = some number
'''
def convert_json():
	with open("Data/janssen_distribution.json") as file:
		janssen_dict = json.loads(file.read())
	
	with open("Data/moderna_distribution.json") as file:
		moderna_dict = json.loads(file.read())
	
	with open("Data/pfizer_distribution.json") as file:
		pfizer_dict = json.loads(file.read())

	for key, value in moderna_dict.items():
		print (key)

	janssen_vaccine_dict = create_dict(janssen_dict)
	moderna_vaccine_dict = create_dict(moderna_dict)
	pfizer_vaccine_dict = create_dict(pfizer_dict)

	full_vac_dict = dict()
	for key in janssen_vaccine_dict.keys():
		full_vac_dict[key] = janssen_vaccine_dict[key]+moderna_vaccine_dict[key]+pfizer_vaccine_dict[key]

	return full_vac_dict

'''
Converts xlsx file to dictionaries through use of panda DataFrame
returns two dictionaries:
1. a condition dictionary showing the underlying conditions per state, condition_dict['Alaska'] = some number
2. a population dictionary containing the population from 2018 that are 18 and older, population_dict['New York'] = some number
'''
def convert_excel():
	data = pandas.read_excel("Data/underlying conditions.xlsx")
	condition_data = pandas.DataFrame(data, columns= ['STATE_NAME', 'county_pop2018_18 and older', 'anycondition_number'])
	condition_dict = dict()
	population_dict = dict()
	for index, row in condition_data.iterrows():
		if row['STATE_NAME'] not in condition_dict.keys():
			condition_dict[row['STATE_NAME']] = float(row['anycondition_number'])
		else:
			condition_dict[row['STATE_NAME']] += float(row['anycondition_number'])
		if row['STATE_NAME'] not in population_dict.keys():
			population_dict[row['STATE_NAME']] = float(row['county_pop2018_18 and older'])
		else:
			population_dict[row['STATE_NAME']] += float(row['county_pop2018_18 and older'])

	return condition_dict, population_dict

'''
Converts csv file to dictionaries through use of panda DataFrame
returns a dictionary containing the covid vaccines in that state
condition_dict['Alabama'] = some number
'''
def convert_csv():
	data = pandas.read_csv("Data/covid19_vaccinations_in_the_united_states.csv", sep='delimiter', header=None, engine='python')
	vaccine_data = pandas.DataFrame(data)
	vaccine_dict = dict()
	count = 0
	for index, row in vaccine_data.iterrows():
		if count >= 3:
			current_data = row.to_string().split(',')
			current_state = current_data[0][4:]
			if current_state not in vaccine_dict.keys():
				vaccine_dict[current_state] = float(current_data[1])
		count += 1

	return vaccine_dict

'''
Main function used to test
'''	
if __name__ == "__main__":
	convert_json()
	convert_excel()
	convert_csv()