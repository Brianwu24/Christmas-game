import numpy as np
from glob import glob
import tensorflow
from tensorflow.keras.models import load_model

class AI_Judges():
    def __init__(self):
        self.judges = {}
        self.model_files = glob('CNN/models/*.h5')
        for model_number in range(len(self.model_files)):
            name = self.model_files[model_number].split("\\")[-1] #get the name of the model from the file name
            name = name[:-3] #remove .h5 from sting
            self.judges[name] = load_model(self.model_files[model_number]) #load the model and append the name and model(tensorflow) to the dict
    def judge(self, model_key, input_image):
        input_image = np.array(input_image.copy(), np.int16).reshape(-1, 13, 13, 3) #reshape, and convert to np array for inferencing
        output = self.judges[model_key].predict(input_image).squeeze() #squeeze() for faster processing
        return output


if __name__ == "__main__":
    #test if each model works for its respective dataset
    file = "CNN/Dataset/Chadwick/21.npz"
    data = np.load(file, allow_pickle=True)
    image = data["inputs"]
    print(data["outputs"])
    judges = AI_Judges()
    print(judges.judge("Chadwick",image))
