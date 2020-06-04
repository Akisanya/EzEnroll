from flask import Flask, render_template, request
from RMPClass import RateMyProfScraper
from ClassSearchScraper import PittClassSearch

# Pitt ID 1247
PittRMP = RateMyProfScraper(1247)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getCourse():
    text = request.form['course']
    Pitt = PittClassSearch(text)
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

        print(profDict)

    return render_template('results.html', profDict=profDict)


if __name__ == '__main__':
    app.run(debug=True)
