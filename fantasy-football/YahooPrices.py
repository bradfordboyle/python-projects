#!/usr/bin/python2.7

from BeautifulSoup import BeautifulSoup
import glob
import re
import os
import sys


def YahooPrices(path = '.'):
    file_extension = '*.html'
    file_glob = os.path.join(path, file_extension)
    yahoo_prices = {}
    prog = re.compile(r'\((?P<team>[a-zA-Z]+) - (?P<pos>[a-zA-Z]+)\)')
    for infile in glob.iglob(file_glob):
        sys.stderr.write('''\t%s...\n''' %(infile))
        with open(infile, 'r') as f:
            soup = BeautifulSoup(f)
            f.close()
    
        table = soup.findAll('table', {'class':
                                       re.compile(r'\bysf-team-stats-table\b')})[-1]
        table_body = table.find('tbody')
        rows = table_body.findAll('tr')
    
        for tr in rows:
	    name = tr.find('td', 'name').find(text=True)
            team_pos = tr.find('em', {'class': 'player-team-pos'}).find(text=True)
            # TODO: Compile regex for faster performance
            s = prog.search(team_pos)
            team = s.group('team').upper()
            position = s.group('pos').upper()
            salary = tr.find('td', 'salary').find(text=True)
            if position == 'DEF':
                yahoo_prices[(team, 'DST')] = float(salary.strip('$'))
            else:
                last_name = name.strip().split()[1]
                key = (name.strip(), team, position)
                if key in yahoo_prices:
                    sys.stderr.write('''*** DUPLICATE KEY DETECTED ***\n''')
                    sys.stderr.write('''%s\n''' %(str(key)))
                yahoo_prices[key] = float(salary.strip('$'))
    
    return yahoo_prices
      #print '''%s, %s, %s, %s''' %(name.strip(), team, position, salary.strip())
