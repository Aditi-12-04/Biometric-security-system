#  How it works? 
1. User uploads fingerprint image and either left or right iris image. 
2. User clicks on upload 
3. User clicks on authenticate to view results

# What happens when user clicks upload button? 
The fingerprint and iris image are saved in the temp directory and the file path for both is saved in a variable. The verify_person() method is called with fingerprint img path and iris img path passed as parameters. 
What does the verify_person() method do? – we set the result variable to False at first. 
The fingerprint image is passed to the verify_fingerprint() for the machine learning model (trained only on fingerprint data) to identify the closest match. It gets the possible class label and the confidence score (a measure of how confident the model is about the prediction).  
In a similar manner the iris path is passed to verify_iris() method where we have 2 models. One model trained only on left iris images and another only on the right iris images. We take class label and confidence score from both models (because we don’t know if the user uploads left iris img or the right img). Once we obtain both confidence scores, we check the highest confidence score among the two. Then we return a string (either ‘Left Iris’ or ‘Right Iris’), the class label and confidence score.  
Now once we are back in the verify_person() method and we have these data: fingerprint match(i.e the finger print matched with which person in the dataset), the confidence score in the prediction for fingerprint, the iris image that the user uploaded (left or right), iris match (i.e the iris matched with which person in the dataset) and the confidence score for iris prediction.  
Now we check if the fingerprint match confidence score and iris match score are greater than 50. This is done so that if the model is not sure about the prediction, there is a possibility that the class label it predicted may be wrong. If both the scores are above 50, we check if the fingerprint match and iris match both match with same person. We don’t want to authenticate when fingerprint matches with someone and iris matches with someone else. If both the predictions match, we set the result flag to True 
The result, fingerprint match, fingerprint confidence score, iris img type (left or right) and iris confidence score data is returned to the authenticate method. 
