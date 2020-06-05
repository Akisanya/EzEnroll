from flask import Flask, render_template, request
from RMPClass import RateMyProfScraper
from ClassSearchScraper import PittClassSearch

# Pitt ID 1247
PittRMP = RateMyProfScraper(1247)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask


@app.route('/', methods=['POST'])
def getCourse():
    text = request.form['course']
    # converts course code to upercase
    Pitt = PittClassSearch(text.split()[0].upper() + " " + text.split()[1])
    profDict = Pitt.getProfDict()

    for key in profDict:
        if(PittRMP.SearchProfessor(key)):
            profDict[key]['RMPRating'] = PittRMP.getProfessorDetail(
                'overall_rating')
            profDict[key]['numReviews'] = PittRMP.getProfessorDetail(
                'tNumRatings')
        else:
            profDict[key]['RMPRating'] = 'Unavailable'
            profDict[key]['numReviews'] = 'Unavailable'

    return render_template('results.html', profDict=profDict)


if __name__ == '__main__':
    app.run(debug=True)
