#!/usr/bin/env python

import argparse
import csv
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description = '''Buils integer linear program for Salary Cap Fantasy football''')
    parser.add_argument('-f', '--file', help='which week to solve for')
    args = parser.parse_args()
    BuildLPModel(args)
    
def BuildLPModel(args):
    objective = []
    salary_constraint = []
    position_constraints = {
            'QB': [],
            'RB': [],
            'WR': [],
            'TE': [],
            'K': [],
            'DST': [],
            }
    position_limits = {
            'QB': 1,
            'RB': 2,
            'WR': 3,
            'TE': 1,
            'K': 1,
            'DST': 1,
            }
    binary = []
    fieldnames = ('points', 'salary', 'name', 'team', 'position')
    counts = {}
    reader = csv.DictReader(
            open(args.file, 'r'),
            fieldnames = fieldnames)
    for row in reader:
        if row['position']:
            position = row['position'].strip()
        else:
            position = row['team'].strip()

        points = float(row['points'])
        salary = float(row['salary'].strip('$'))
        
        counts[position] = counts.get(position, 0) + 1
        variable = position + '%d' %(counts[position])
        objective.append('%.2f %s' %(points, variable))
        salary_constraint.append('%.2f %s' %(salary, variable))
        position_constraints[position].append('%s' %(variable))
        binary.append('%s' %(variable))
    
    print 'max:',
    print ' + '.join(objective) + ';'
    
    print 'salary_constraint: 100 >=',
    print ' + '.join(salary_constraint) + ';'
    
    for k, v in position_constraints.iteritems():
        print '%s: %d =' %(k, position_limits[k]),
        print ' + '.join(v) + ';'
    
    print 'bin ',
    print ' '.join(binary) + ';'

        
if __name__ == '''__main__''':
    main()
