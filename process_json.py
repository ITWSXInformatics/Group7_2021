import json
import pandas
import statistics
import plotly.express as px

'''
Helper function to create a dictionary, should only be called within this file
'''
def create_dict(vac_data, dosages):
	state_dict = dict()
	vac_frame = None
	if (dosages == 1):
		vac_frame = pandas.DataFrame(vac_data, columns = ['Jurisdiction', '1st Dose Allocations'])
	else:
		vac_frame = pandas.DataFrame(vac_data, columns = ['Jurisdiction', '2nd Dose Allocations'])
	for index, row in vac_frame.iterrows():
		if row['Jurisdiction'] not in state_dict.keys():
			if dosages == 1:
				state_dict[row['Jurisdiction']] = float(row['1st Dose Allocations'])
			else:
				state_dict[row['Jurisdiction']] = float(row['2nd Dose Allocations'])
		else:
			if dosages == 1:
				state_dict[row['Jurisdiction']] += float(row['1st Dose Allocations'])
			else:
				state_dict[row['Jurisdiction']] += float(row['2nd Dose Allocations'])

	return state_dict

'''
Converts json files to dictionaries
Takes in nothing, returns dictionary with keys being state name, and the value is the amount of vaccines distributed
Example:
full_vac_dict['Alaska'] = some number
'''
def convert_states():
	#with open("Data/janssen_distribution.json") as file:
	#	janssen_dict = json.loads(file.read())
	
	#with open("Data/moderna_distribution.json") as file:
	#	moderna_dict = json.loads(file.read())
	
	#with open("Data/pfizer_distribution.json") as file:
	#	pfizer_dict = json.loads(file.read())

	#for key, value in moderna_dict.items():
	#	print (key)

	janssen_data = pandas.read_csv("Data/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Janssen.csv")
	moderna_data = pandas.read_csv("Data/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Moderna.csv")
	pfizer_data = pandas.read_csv("Data/COVID-19_Vaccine_Distribution_Allocations_by_Jurisdiction_-_Pfizer.csv")

	janssen_vaccine_dict = create_dict(janssen_data,1)
	moderna_vaccine_dict = create_dict(moderna_data,2)
	pfizer_vaccine_dict = create_dict(pfizer_data,2)

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
	data = pandas.read_excel("Data/underlying conditions.xlsx", engine="openpyxl")
	condition_data = pandas.DataFrame(data, columns= ['STATE_NAME', 'county_pop2018_18 and older', 'anycondition_number'])
	condition_dict = dict()
	for index, row in condition_data.iterrows():
		if row['STATE_NAME'] not in condition_dict.keys():
			condition_dict[row['STATE_NAME']] = float(row['anycondition_number'])
		else:
			condition_dict[row['STATE_NAME']] += float(row['anycondition_number'])

	return condition_dict

def convert_population():
	population_dict = dict()
	name_file = open('Data/state_name.txt');
	names = name_file.read()
	data_file = open('Data/census_2010.txt');
	data = data_file.read()

	name_array = names.split("\n");
	data_array_out = data.split("\n");

	for i in range(len(name_array)):
		data_array_inner = data_array_out[i].split(" ")
		name = name_array[i]
		population = float(data_array_inner[len(data_array_inner)-1].replace(",", ""))
		population_dict[name] = population
	return population_dict

'''
Converts csv file to dictionaries through use of panda DataFrame
returns a dictionary containing the covid vaccines in that state
condition_dict['Alabama'] = some number
'''
def convert_csv():
	data = pandas.read_csv("Data/covid19_vaccinations_in_the_united_states.csv", header=1, engine='python')
	age_distribution = pandas.read_csv("Data/age_distribution.csv", header=1, usecols=[0,1,2,3,4,5,6,7,8], engine='python')
	minority_population = pandas.read_csv("Data/Minority_Population/ACSDT5Y2019.B03002_data_with_overlays_2021-08-03T103112.csv")
	education_levels = pandas.read_csv("Data/Education_Levels/ACSST1Y2019.S1501_data_with_overlays_2021-07-27T000423.csv")
	income_levels = pandas.read_csv("Data/Median_Income/ACSST1Y2019.S1902_data_with_overlays_2021-08-25T131622.csv")
	mobility_levels = pandas.read_csv("Data/Mobility_Report/2021_US_Region_Mobility_Report.csv")

	mobility_data = pandas.DataFrame(mobility_levels)
	mobility_dict = dict()

	minority_data = pandas.DataFrame(minority_population)
	minority_dict = dict()

	education_data = pandas.DataFrame(education_levels)
	education_dict = dict()

	vaccine_data = pandas.DataFrame(data)
	vaccine_dict = dict()

	age_dist_data = pandas.DataFrame(age_distribution)
	age_dict = dict()

	income_level_data = pandas.DataFrame(income_levels)
	income_dict = dict()

	for index, row in mobility_data.iterrows():
		if row['date'] == '2021-05-01' and isinstance(row['sub_region_2'],float) and isinstance(row['sub_region_1'],str):
			total_mobility = row['retail_and_recreation_percent_change_from_baseline']+row['grocery_and_pharmacy_percent_change_from_baseline']+row['parks_percent_change_from_baseline']+row['transit_stations_percent_change_from_baseline']+row['workplaces_percent_change_from_baseline']+row['residential_percent_change_from_baseline']
			mobility_dict[row['sub_region_1']] = total_mobility

	count = 0
	for index, row in income_level_data.iterrows():
		if (count > 0):
			per_capita = float(row['S1902_C03_019E'])
			if row['NAME'] == 'New York State':
				income_dict['New York'] = per_capita
			else:
				income_dict[row['NAME']] = per_capita
		count += 1

	count = 0
	for index, row in minority_data.iterrows():
		if (count > 0):
			total_african_american = float(row['B03002_004E'])+float(row['B03002_014E'])
			if row['NAME'] == 'New York State':
				minority_dict['New York'] = total_african_american
			else:
				minority_dict[row['NAME']] = total_african_american
		count += 1

	count = 0
	for index, row in education_data.iterrows():
		if (count > 0):
			total_under_highschool = float(row['S1501_C01_002E'])+float(row['S1501_C01_007E'])+float(row['S1501_C01_008E'])+float(row['S1501_C01_009E'])
			if row['NAME'] == 'New York State':
				education_dict['New York'] = total_under_highschool
			else:
				education_dict[row['NAME']] = total_under_highschool
		count += 1


	count = 0
	for index, row in age_dist_data.iterrows():
		if (count > 1):
			if index[6] == 'New York State':
				age_dict['New York'] = float(index[6])
			else:
				age_dict[index[0]] = float(index[6])
		count += 1;

	count = 0
	for index, row in vaccine_data.iterrows():
		print(index[0])
		if count > 0:
			current_state = index[0]
			current_data = float(index[24])+float(index[25])+float(index[26])
			if current_state == 'New York State':
				current_state = 'New York'
			if current_state not in vaccine_dict.keys():
				vaccine_dict[current_state] = current_data
		count += 1
	return vaccine_dict, age_dict, education_dict, minority_dict, income_dict, mobility_dict




def countyPop():
	data = pandas.read_csv("Data/county census data 2019.csv", sep='delimiter', header=None, engine='python')


#data at county level: underlying conditions, population
# data needed: vaccine distribution, prior vcaccination (maybe we can extrapolate this?)
#def rankCounties():


def ranking(states):

	abbreviations = {
	'Alabama' : 'AL',
	'Alaska' : 'AK',
	'Arizona' :'AZ',
	'Arkansas' : 'AR',
	'California' : 'CA',
	'Colorado' : 'CO',
	'Connecticut' : 'CT',
	'Delaware' : 'DE',
	'District of Columbia' : 'DC',
	'Florida' : 'FL',
	'Georgia' : 'GA',
	'Hawaii' : 'HA',
	'Idaho' : 'ID',
	'Illinois' : 'IL',
	'Indiana' : 'IN',
	'Iowa' : 'IA',
	'Kansas' : 'KS',
	'Kentucky' : 'KY',
	'Louisiana' : 'LA',
	'Maine' : 'ME',
	'Maryland' : 'MD',
	'Massachusetts' : 'MA',
	'Michigan' : 'MI',
	'Mississippi' : 'MS',
	'Missouri' : 'MO',
	'Minnesota' : 'MN',
	'Montana' : 'MT',
	'Nebraska' : 'NE',
	'Nevada' : 'NV',
	'New Hampshire' : 'NH',
	'New Jersey' : 'NJ',
	'New Mexico' : 'NM',
	'New York' : 'NY',
	'North Carolina' : 'NC',
	'North Dakota' : 'ND',
	'Ohio' : 'OH',
	'Oklahoma' : 'OK',
	'Oregon': 'OR',
	'Pennsylvania' : 'PA',
	'Rhode Island' : 'RI',
	'South Carolina' : 'SC',
	'South Dakota': 'SD',
	'Tennessee' : 'TN',
	'Texas' : 'TX',
	'Utah' : 'UT',
	'Vermont' : 'TV',
	'Virginia' : 'VA',
	'Washington' : 'WA',
	'West Virginia' : 'WV',
	'Wisconsin' : 'WI',
	'Wyoming' : 'WY'
	}
	
	shippedDict = convert_states()
	conditionDict = convert_excel()
	vaccineDict, age_dict, education_dict, minority_dict, income_dict, mobility_dict = convert_csv()
	populationDict = convert_population()
	ranking_frame = pandas.DataFrame(columns = ['State', 'Rank'])

	total_morbidity_factor = 0

	income_list = list(income_dict.values())

	median_val = statistics.median(income_list)

	print(median_val)

	for state in states:
		total_morbidity_factor += conditionDict[state]*age_dict[state]*minority_dict[state]*populationDict[state]

	dataArr = []

	max = 0
	max_state = ''

	for state in states:
		shippedData = shippedDict[state]
		conditionData = conditionDict[state]
		populationData = populationDict[state]
		vaccineData = vaccineDict[state]
		ageData = age_dict[state]
		educationData = education_dict[state]
		minorityData = minority_dict[state]
		incomeData = income_dict[state]
		mobilityData = mobility_dict[state]

		#state_morbidity_factor = conditionData*ageData*minorityData*incomeData*populationData

		cond_factor = conditionData/populationData
		age_factor = ageData/populationData
		minority_factor = minorityData/populationData
		education_factor = educationData/populationData

		#higher percentage of minority will affect poorly
		#low income affect poorly
		#higher percentage of age affect porly
		#higher percentage condition affect poorly
		#higher percentage low education affect poorly

		population_affected = cond_factor*populationData+minority_factor*populationData+education_factor*populationData

		mortalityIndex = population_affected/populationData

		mobility_factor = 0

		if mobilityData <= 0:
			mobility_factor = 1
		elif mobilityData > 0 and mobilityData < 50:
			mobility_factor = 1.5
		else:
			mobility_factor = 2

		mortalityIndex *= mobility_factor

		income_factor = 0

		if incomeData < median_val:
			income_factor = 1.5
		else:
			income_factor = 1

		mortalityIndex *= income_factor

		vaccineIndex = shippedData/(populationData - vaccineData)

		rank = mortalityIndex/vaccineIndex

		if rank > max:
			max = rank
			max_state = state

		stateStats = {"name": state, "Underlying conditions (number)": conditionData, "Population": populationData, "Rank": rank}

		ranking_frame = ranking_frame.append({'State': abbreviations[state], 'Rank': rank}, ignore_index=True)
		dataArr.append(stateStats)

	color_states = ranking_frame.loc[:,'State'].values

	fig = px.choropleth(ranking_frame['Rank'], locations = color_states, color = 'Rank', locationmode="USA-states", scope="usa")
	fig.show()

	print(max)
	print(max_state)

	#state_df = pandas.DataFrame.from_dict(ranking_dict, orient = 'index')

	ranking_frame.to_csv("ranking_data.csv")
	#json_out = open("ranking_data_out.json", "w")
	#json.dump(dataArr, json_out);

	return(dataArr)

'''
Main function used to test
'''	
if __name__ == "__main__":
	#convert_states()
	#convert_excel()
	#convert_csv()

	state_dict = convert_population()
	states = state_dict.keys()

	ranking(states)