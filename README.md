# CZ4171-Course-Project

Iot Device emulated on Android Studio. Model inference on flask server in python. Program detects fraudulent and legitimate SMSs. Uses public data set from https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv. Uses scikit's Gaussian Naive Bayes Classifier with accuracy of 0.8860986547085202. Log output from terminal with accuracy score provided in Terminal Log.txt.

## Getting Started

### Dependencies

* pandas
* Flask
* nltk
* scikit-learn

### Executing program

* Run the python program to start the server
* Create a Virtual Device and run app on Android Studio.
* Paste SMS into input text field.
* Click "Send HTTP GET" to test HTTP GET request. Reception and response reflected on python server.
* Click "Check SMS" to perform model inference on SMS. Server returns result on emulator interface.
* Click "Report Spam" to pass SMS to server as training data. Server will retrain model.

## Authors

Eugene Lim @eugenelzj99

## Acknowledgments

ReadMe Template
* [DomPizzie](https://github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
