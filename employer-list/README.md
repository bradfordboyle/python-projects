employer-list
=============

In October, Drexel Universit's SCDC host a career fair where the list of
attending employers was distributed as an Excel spread sheet. A minor annoyance
was that all of the majors that an employer was interested in were lumped into
one string. This made it somewhat difficult to search/filter the list. This
script reads in the Excel spreadsheet and builds up a sqlite database.
Currently the bash script accepts a major (i.e., electrical engineering) and
returns a list of all employers looking to hire electrical engineers full time.
This can be tweaked for internships and/or sponsoring international students.

Going forward, I would like to turn this into a Flask app so that everyone can
search/filter the full employer list and get a personalized list to focus on.
