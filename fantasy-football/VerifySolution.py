#!/usr/bin/env python

import argparse
import csv
import os.path
import re
import sys

def main():
    parser = argparse.ArgumentParser(description = '''Buils integer linear program for Salary Cap Fantasy football''')
    parser.add_argument('-f', '--file', help='which week to solve for')
    parser.add_argument('-s', '--sol', help='solution file from lp_solve -S2')
    args = parser.parse_args()
    team = ParseSolution(args)
    VerifySolution(args, team)
    
def ParseSolution(args):
    team = {}
    pattern = re.compile(r'^([A-Z]{1,3})(\d+).+1$')
    f = open(args.sol, 'r')
    for line in f:
        result = pattern.match(line)
        if result:
            k = result.group(1)
            v = int(result.group(2))
            team.setdefault(k,[]).append(v)
    f.close()
    return team

def VerifySolution(args, team):
    total_salary = 0.0
    total_points = 0.0

    counts = {}

    f = open(args.file,'r')
    fieldnames = ('points', 'salary', 'name', 'team', 'position')
    reader = csv.DictReader(
        open(args.file, 'r'),
	fieldnames = fieldnames)

    team_str = []
    for row in reader:
        if row['position']:
            k = row['position'].strip()
	    key = '''(u'%s', u'%s', u'%s')''' % (
	        row['name'].strip(), row['team'].strip(), k)
        else:
            k = row['team'].strip()
	    key = '''(u'%s', u'%s')''' % (row['name'].strip(),
	        row['team'].strip())
        points = float(row['points'].strip())
        salary = float(row['salary'].strip('$'))

        counts[k] = counts.setdefault(k, 0) + 1

        if counts[k] in team[k]:
            team_str.append('%s: %.2f' %(key, salary))
            total_salary += salary
            total_points += points
    print '#!/usr/bin/python\n\nteam = {\n    ' + ',\n    '.join(team_str) + ',}'
    sys.stderr.write('''Cost: %.2f\n''' %(total_salary))
    sys.stderr.write('''Projected Points: %.2f\n''' %(total_points))

        
if __name__ == '''__main__''':
    main()
