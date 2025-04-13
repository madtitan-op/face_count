import csv
import os

file_name = "student_data.csv"
file_exists = os.path.isfile(file_name) 

def csv_data(data):
    
    with open(file_name,mode="a",newline='') as file :
        fieldname =["name","roll",'face_encodings']
        csv_writer = csv.DictWriter(file,fieldnames = fieldname)
        
        if not file_exists:
            csv_writer.writeheader()

        for row in data:
            row['face_encodings'] = row['face_encodings'][0].tolist() # converting numpy array into list to store in csv file  
            csv_writer.writerow(row)
        