#!/usr/bin/python2.7

from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
import csv
import re

PROJECTIONS_URL = '''http://fantasynews.cbssports.com/fantasyfootball/stats/weeklyprojections/'''


def YahooScore(projection, position):
    if position == 'DST':
        # Sack - 3 - 1 pt
        # Interception - 0 - 2 pt
        # Fumble Recovery - 1 - 1 pt
        # Touchdown - 4 - 6 pt
        # Safety - 5 - 2 pt
        # Points Allowed - 6 - Range
        fantasy_pts = projection[3] + 2.0 * projection[0] + projection[1] + 6.0 * projection[4] + 2.0 * projection[5]
        points_allowed = projection[6]
        if points_allowed == 0: fantasy_pts += 10.0
        elif points_allowed <= 6: fantasy_pts += 7.0
        elif points_allowed <= 13: fantasy_pts += 4.0
        elif points_allowed <= 20: fantasy_pts += 1.0
        elif points_allowed <= 34: fantasy_pts -= 1.0
        elif points_allowed >= 35: fantasy_pts -= 4.0
    elif position == 'K':
        fantasy_pts = projection[3]
    elif position == 'RB':
        # TD - 3 & 7 - 6 pts
        # Rush Yds - 1 - 1/20 pts
        # Rec Yds - 5 - 1/20 pts
        # 2-pt - NA - 2
        # Fum Lost - 8 - -2
        fantasy_pts = 6.0 * (projection[3] + projection[7]) + (projection[1] + projection[5])/20.0 - 2.0 * projection[8]
    elif position == 'WR':
        # TD - 3 - 6 pts
        # Rec Yds - 1 - 1/20 pts
        # Fum Lost - 4 - -2
        fantasy_pts = 6.0 * projection[3] + projection[1]/20.0 - 2.0 * projection[4]
    elif position == 'TE':
        fantasy_pts = 6.0 * projection[3] + projection[1]/20.0 - 2.0 * projection[4]
    else:
        fantasy_pts =  6.0 * (projection[3] + projection[10]) + (1.0/50.0) * (projection[2]) - 2.0 * (projection[4]) + (1.0/20.0) * (projection[8]) - 2.0 * (projection[11])

    return fantasy_pts


def ShortName(name, i):    
    return '%s. %s' %(name[0:i], ' '.join(name.split()[1:]))

def CBSProjections(params = ('QB', '1', '')):
    url_values = '/'.join(params)
    full_url = PROJECTIONS_URL + url_values + '''?&print_rows=9999'''

    data = urlopen(full_url)
    soup = BeautifulSoup(data)

    # find <table class = "data">
    table = soup.find('table', 'data')
    
    labels = table.find('tr', 'label')
    column_names = []
    for td in labels.findAll('td'):
        column_names.append(''.join(td.find(text=True)))
    
    rows = table.findAll('tr', {'class': re.compile(r'row[12]')})
    ProjectedPoints = {}
    for tr in rows[1:]:
        name_team = tr.find('td', {'align': 'left'}).findAll(text=True)
        name = name_team[0]
        s = re.search(r'\&nbsp\;(?P<team>[a-zA-Z]+)',name_team[1])
        team = s.group('team')
      
        cols = tr.findAll('td', {'align': 'center'})
        projection = []
        for td in cols:
            projection.append(''.join(td.find(text=True)))
        projected_points = YahooScore(map(float,projection), params[0])
        if params[0] == 'DST':
            ProjectedPoints[(team, params[0])] = projected_points
        else:
            shortKey = (ShortName(name.strip(),1), team, params[0])
            key = (name.strip(), team, params[0])
            if key in ProjectedPoints or shortKey in ProjectedPoints:
                sys.stderr.write('''*** DUPLICATE KEY DETECTED ***\n''')
                sys.stderr.write(str(key))
            ProjectedPoints[key] = projected_points
	    # ProjectedPoints[shortKey] = projected_points

    return ProjectedPoints


def SaveProjections(filename, projections):
    """Write projections to filename as a comma seperated values file"""
    column_names, player_projections = projections
    with open(filename, 'wb') as f:
        projections_writer = csv.writer(f)
        projections_writer.writerow(column_names)
        projections_writer.writerows(player_projections)
        f.close()


def main():
    projections = CBSProjections(('QB', '2', ''))
    save_projections('CBS-QB.csv', projections)

if __name__ == '''__main__''':
    main()
