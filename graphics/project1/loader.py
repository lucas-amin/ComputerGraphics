import sys, os
from subprocess import check_output 

class Map():
	application_directory = "../../2019cglib/applications/appImage"
	image_dictionary = {"maxmin2": "../../2019cglib/applications/imagens/maxmin2.pgm"}

	def __init__(self):
		a = 0

	def get_map(self):
		result = check_output([self.application_directory, self.image_dictionary["maxmin2"]])

		# Decode binary into string
		str_result = result.decode()[:-1]

		# Split string into list
		image_map = str_result.split("\n")

		# Get the first two items from the list
		minimum = image_map.pop(0)
		maximum = image_map.pop(0)

		for i in range(len(image_map)):
		# The numbers comes in format "12 13 14 ", so it is necessary to split the last space using [:-1]
			image_map[i] = image_map[i][:-1].split(" ")

		return image_map


if __name__ == "__main__":
	map = Map()

	result = map.get_map()


	print(result)