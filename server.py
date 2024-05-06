# pip install pandas
# pip install Flask
# pip install nltk
# pip install -U scikit-learn

import pandas as pd
from flask import Flask
from flask import request
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Reading data
data = pd.read_csv('https://raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv', encoding='latin-1')
# Drop unnecessary columns and rename cols
data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
data.columns = ['label', 'text']
data['label'].replace("spam", "Scam", inplace=True)
data['label'].replace("ham", "Legitimate", inplace=True)
# Check missing values
data.isna().sum()
# Check data shape
data.shape
# Create a list text
text = list(data['text'])

# Preprocessing loop
lemmatizer = WordNetLemmatizer()
corpus = []

for i in range(len(text)):
    r = re.sub('[^a-zA-Z]', ' ', text[i])
    r = r.lower()
    r = r.split()
    r = [word for word in r if word not in stopwords.words('english')]
    r = [lemmatizer.lemmatize(word) for word in r]
    r = ' '.join(r)
    corpus.append(r)
# Assign corpus to data['text']
data['text'] = corpus

def model_train(data):
    print("Model Train - Start")
    X = data['text']
    y = data['label']
    # Train-test split (80% train - 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    print('Training Data :', X_train.shape)
    print('Testing Data : ', X_test.shape)

    # Create Bag of Words
    cv = CountVectorizer()
    X_train_cv = cv.fit_transform(X_train)
    X_train_cv.shape
    # Train a Bayes Classifier
    bayes_classifier = GaussianNB()
    bayes_classifier.fit(X_train_cv.toarray(), y_train)
    X_test_cv = cv.transform(X_test)
    pred = bayes_classifier.predict(X_test_cv.toarray())
    print('Accuracy Score :', accuracy_score(y_test, pred))
    print("Model Train - End")

    return cv, bayes_classifier

cv, bayes_classifier = model_train(data)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_call():
    return "Successfully Connected"

@app.route('/get', methods=['GET'])
def get():
    return "GET Request successful"

@app.route('/getresult/<sms>', methods=['POST'])
def get_smsresult(sms):
    # Lemmatize SMS
    sms = re.sub('[^a-zA-Z]', ' ', sms)
    sms = sms.lower()
    sms = sms.split()
    sms = [word for word in sms if word not in stopwords.words('english')]
    sms = [lemmatizer.lemmatize(word) for word in sms]
    sms = ' '.join(sms)
    # Predict nature of SMS
    smslist = [sms]
    sms_cv = cv.transform(smslist)
    prediction = bayes_classifier.predict(sms_cv.toarray())

    return prediction[0]

@app.route('/updatemodel/<sms>', methods=['POST'])
def update_model(sms):
    sms = re.sub('[^a-zA-Z]', ' ', sms)
    sms = sms.lower()
    sms = sms.split()
    sms = [word for word in sms if word not in stopwords.words('english')]
    sms = [lemmatizer.lemmatize(word) for word in sms]
    sms = ' '.join(sms)
    # Add SMS
    data.loc[len(data.index)] = ['spam', sms]
    # Retrain Model with SMS
    cv, bayes_classifier = model_train(data)

    return "Model Updated"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)