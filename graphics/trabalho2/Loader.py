from subprocess import check_output
import cv2

class Loader():
    application_directory = "./appImage/appImage"
    image_dictionary = {"maxmin2": "./imagens/maxmin2.pgm",
    					"maxmin": "./imagens/maxmin.pgm",
    					"crater": "./imagens/crater.pgm",
    					"crater2": "./imagens/crater2.pgm",
    					"crater3": "./imagens/crater3.pgm",
    					"crater4": "./imagens/crater4.pgm"}

    def __init__(self):
        a = 0

    def get_map(self, use_script=True, image="crater2"):
        if use_script:
            return self.extract_image_C(image)
        else:
            return self.extract_image_python(image)

    def extract_image_python(self, image):
        image_map = cv2.imread(self.image_dictionary[image], 0)

        max_value = 0
        min_value = 255

        for column in range(len(image_map)):
            for row in range(len(image_map[column])):
                if image_map[column][row] > max_value:
                    max_value = image_map[column][row]

                if image_map[column][row] < min_value:
                    min_value = image_map[column][row]

        return min_value, max_value, image_map

    def extract_image_C(self, image_name):
        result = check_output([self.application_directory, self.image_dictionary[image_name]])

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

        return minimum, maximum, image_map


if __name__ == "__main__":
    map = Loader()

    result = map.get_map(use_script=False)
