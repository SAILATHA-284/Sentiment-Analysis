from flask import Flask, render_template,request
from textblob import TextBlob 
import csv 
import os

app= Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')

def index():
    return render_template('index.html',result=None)

@app.route('/analyse', methods=['POST'])

def analyse():
    text= request.form['text']
    blob= TextBlob(text)
    polarity= blob.sentiment.polarity
    
    if polarity > 0:
        sentiment = "Postive 😊"
        response = "Thank you for your positive feedback! We appreciate your kind words."
    elif polarity < 0:
        sentiment = "Negative 😠"
        response = "Sorry to hear about your experience. We will try to improve our service."
    else:
        sentiment = "Neutral 😐"
        response = "Thank you for your input! We are here to help if needed."
    return render_template('index.html',result=sentiment,text=text,polarity=polarity,response=response)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return render_template('index.html', result=None, error="No file selected.")

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(filepath)

    reviews = []
    if uploaded_file.filename.endswith('.csv'):
        with open(filepath, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                reviews.extend(row)  
    elif uploaded_file.filename.endswith('.txt'):
        with open(filepath, encoding='utf-8') as f:
            reviews = [line.strip() for line in f if line.strip()]
    positive = negative = neutral = 0
    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            positive += 1
        elif polarity < 0:
            negative += 1
        else:
            neutral += 1
    total = positive + negative + neutral

    return render_template(
        'index.html',
        bulk_result=True,
        total=total,
        positive=positive,
        negative=negative,
        neutral=neutral
    )

if __name__=='__main__':
    app.run(debug=True)
