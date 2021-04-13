import json
import pandas

def create_dict(vac_dict):
	state_dict = dict()
	for item in vac_dict["data"]:
		if item[8] not in state_dict.keys():
			state_dict[item[8]] = float(item[10])
		else:
			state_dict[item[8]] += float(item[10])
	return state_dict

def convert_json():
	with open("janssen_distribution.json") as file:
		janssen_dict = json.loads(file.read())
	
	with open("moderna_distribution.json") as file:
		moderna_dict = json.loads(file.read())
	
	with open("pfizer_distribution.json") as file:
		pfizer_dict = json.loads(file.read())

	for key, value in moderna_dict.items():
		print (key)

	janssen_vaccine_dict = create_dict(janssen_dict)
	moderna_vaccine_dict = create_dict(moderna_dict)
	pfizer_vaccine_dict = create_dict(pfizer_dict)

	full_vac_dict = dict()
	for key in janssen_vaccine_dict.keys():
		full_vac_dict[key] = janssen_vaccine_dict[key]+moderna_vaccine_dict[key]+pfizer_vaccine_dict[key]

	print(full_vac_dict)

if __name__ == "__main__":
	convert_json()