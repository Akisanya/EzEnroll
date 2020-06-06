from flask import Flask, render_template, request, redirect, url_for
from RMPClass import RateMyProfScraper
from ClassSearchScraper import PittClassSearch

# Pitt RMP ID 1247
PittRMP = RateMyProfScraper(1247)
app = Flask(__name__)

# home page


@app.route('/', methods=['POST', 'GET'])
def getCourse():
    # if the form is being summited
    if request.method == 'POST':
        text = request.form['course']
        # redirect to the results page
        return redirect(url_for('getResults', courseName=text.split()[0].upper(), courseNum=text.split()[1]))

    # go to the home page
    else:
        return render_template('index.html')


# results page
@app.route('/<string:courseName>+<string:courseNum>')
def getResults(courseName, courseNum):
    Pitt = PittClassSearch(courseName + " " + courseNum)

    # redirect to error page if course is invalid
    if(not Pitt.isValid()):
        return redirect(url_for('error'))

    # else fill the professor dictionary and render the result template
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


# error page
@app.route('/error')
def error():
    return render_template('error.html', error_msg="Course filled or not found")


if __name__ == '__main__':
    app.run(debug=True)
