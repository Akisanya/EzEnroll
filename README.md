# EzEnroll
Python/Flask web app that adds [RateMyProfessors](https://www.ratemyprofessors.com/) (RMP) support to Pitt Class Search. Given a course, returns course availability (currently set to Fall 2020) and RateMyProfessor data on professors teaching the course.

## Demo
<img src = "https://github.com/Akisanya/EzEnroll/blob/master/demo.gif" alt="demo gif"/>

## Motivation
As a student at Pitt, I've found that registering for classes can be somewhat bothersome. After searching for a course in the class search site, I look at the RMP page for each professor teaching said course. This is a common practice among students which can become overwhelming due to the repeated context switching. In comes EzEnroll. By just typing in the name of a course, you will be directed to a page showing pertinent information (meeting times/location, instructor, class #) for all open sections of the course as well as RMP data (overall rating, number of reviews) for each professor teaching the course.

## Technology Used
<b>Built with</b>
- Python
- Flask
- Selenium
- HTML/CSS
- Modified [RMP Class](https://github.com/Rodantny/Rate-My-Professor-Scraper-and-Search): @Rodantny
