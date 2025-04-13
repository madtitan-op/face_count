import csv
import numpy as np
class reader:
    def csv_read ():
    #reading s_data.csv file
        with open('student_data.csv',mode='r',newline='') as file:
            csv_reader = csv.DictReader(file)
            #converting it into list
            
            #converting the csv file into list
            rows = list(csv_reader)
            

            for data in rows:
                data['face_encodings']=np.array( eval(data['face_encodings']))# converting the string into numpy array 
            
            return rows