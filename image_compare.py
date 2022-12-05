#comapre the images, and check if they are similar, if they are similar then return True, else if they are different return False
# return True if the image is above 31% in deviation
def compare_images(input_image, input_image_list): #checks if the image passes the test
    image = input_image.copy()
    for reference_image in input_image_list.copy():
        deviation = 0
        for y, pixel_row in enumerate(reference_image): # for every pixel check if they are similar
            for x, pixel in enumerate(pixel_row):
                if image[y][x] != pixel:
                        deviation += 1
        deviation = deviation/(len(image))**2
        #51% because canvas background is mostly white
        if deviation <= 0.31: #below 31% deviation means that they are quite similar
            return True #yes it is similar
    return False #if is not similar return False

