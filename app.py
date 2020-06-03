from flask import Flask, render_template, request
from RMPClass import RateMyProfScraper
from ClassSearchScraper import PittClassSearch

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getCourse():
    text = request.form['course']
    Pitt = PittClassSearch(text)
    profDict = Pitt.getProfDict()
    return render_template('results.html', profDict=profDict)


if __name__ == '__main__':
    app.run(debug=True)
