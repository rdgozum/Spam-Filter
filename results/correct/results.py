import os

# --- GLOBAL VARIABLES -------------------------------------------------------------------------------------------------

directory = {
			'ham':"./dataset/test/ham/",
			'spam': "./dataset/test/spam/"
			}

results = {}

# --- FUNCTIONS --------------------------------------------------------------------------------------------------------

def get_result(directory, category):
	# get all files in directory
	for file in os.listdir(directory):
		results[file] = [file, category]
		print file, results[file]

# --- MAIN -------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	get_result(directory['ham'], "ham")
	get_result(directory['spam'], "spam")

	keys = results.keys()
	keys.sort()
	answers = open("answers.txt", "w")
	for key in keys:
		print results[key]
		answers.write(key + " - " + results[key][1] + "\n")

	answers.close()
