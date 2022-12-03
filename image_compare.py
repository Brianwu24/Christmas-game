import numpy as np

#comapre the images, and check if they are similar, if they are similar then return True, else if they are different return False
# return True if the image is above 21% in similarity
def compare_images(input_image, input_image_list): #checks if the image passes the test
    image = input_image.copy()
    for reference_image in input_image_list.copy():
        deviation = np.mean(image != reference_image)
        if deviation <= 0.21: #below 21% mean that they are similar
            return True #yes it is similar
    return False #if is not similar return False

