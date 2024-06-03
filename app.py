import os
from flask import Flask, request, render_template
import models

fingerprint_path = ""
iris_path = ""
people = ['Adam', 'Brian', 'Charlie', 'Dennis', 'Elijah', 'Dev', 'Alex', 'Siri', 'Liana', 'Adah', 'Sam', 'Jacob', 'Mitchell', 
          'Chloe', 'Mathew', 'Amelia', 'Olivia', 'Sophia', 'Jasmine', 'Marcus', 'Ethan', 'Isabella', 'Emily', 'Henry', 'Steve', 
          'Ben', 'Max', 'Noah', 'Lucas', 'Benjamin', 'Abigail', 'Gracy', 'Jameson', 'Natalia', 'Ava', 'Logan', 'Harper', 'Joy', 
          'Bob', 'Will', 'Gabriel', 'Jonathan', 'John', 'Alexander', 'Charlotte' ] # update later
status = ''
outputString = ''
scores = []

def cleanDirectory():
    directory_path = 'temp/'

    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            os.remove(file_path)
            print(f"The file {file_path} has been deleted successfully.")
        print(f"All files in the directory {directory_path} have been deleted.")
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
    except PermissionError:
        print(f"You do not have permission to delete files in the directory {directory_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to compare fingerprint and iris images to determine if they belong to the same person

def verify_person(fingerprint_path, iris_path):
    result = False

    fp_match_person, fp_confidence = models.verifyFingerprint(fingerprint_path)
    iris_img_type, iris_match_person, iris_confidence = models.verifyIris(iris_path)

    if fp_confidence > 50 and iris_confidence > 50: # maybe there's a better way to do this?
        if fp_match_person == iris_match_person:
            result = True

    return result, fp_match_person, fp_confidence, iris_img_type, iris_confidence


app = Flask(__name__)

@app.route('/')
def index():
    global scores
    scores = []
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global scores, status, outputString, people

    fingerprint_file = request.files['fingerprint']
    iris_file = request.files['iris']

    # Save the images temporarily
    fingerprint_file.save(os.path.join('temp', fingerprint_file.filename))
    iris_file.save(os.path.join('temp', iris_file.filename))

    fingerprint_path = f'temp/{fingerprint_file.filename}'
    iris_path = f'temp/{iris_file.filename}'

    result, fp_match_person, fp_confidence, iris_img_type, iris_confidence = verify_person(fingerprint_path, iris_path)

    print(f'Result: {result} Class:{fp_match_person} Fingerprint Confidence: {fp_confidence} Iris Type: {iris_img_type} Iris Confidence: {iris_confidence}')

    scores.append(fp_confidence)
    scores.append(iris_confidence)
    if result:
        status = "Authorised Person"
        outputString = f'Fingerprint and {iris_img_type} that were uploaded belong to {people[int(fp_match_person) - 1]}'
    else:
        status = "Unauthorised Person"
        outputString = "Could not authenticate"

    # Remove temporary images
    cleanDirectory()

    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    global status, outputString, scores
    return render_template('result.html', status = status, outputString = outputString, scores = scores)

@app.route('/visualization')
def visualize():
    return render_template('visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
