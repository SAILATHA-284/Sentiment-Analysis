from flask import Flask, render_template,request
from textblob import TextBlob 

app= Flask(__name__)

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

if __name__=='__main__':
    app.run(debug=True)
