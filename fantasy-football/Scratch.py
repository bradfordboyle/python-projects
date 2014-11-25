#!/usr/bin/env python

import argparse
import pickle
import os.path
import sys
import YahooPrices
import CBSProjections

POSITIONS = ('QB', 'RB', 'WR', 'TE', 'K', 'DST')

def main():
    parser = argparse.ArgumentParser(description = '''Scrape data from CBS
                                     Fantasy Football Projections and downloaded
                                     Yahoo Salary Cap Football pages and combine
                                     them''')
    parser.add_argument('-w', '--week',
                        help = 'wich week of CBS data to scrape')
    args = parser.parse_args()
    PullData(args)

def PullData(args):
    data_directory = 'week' + args.week
    yahoo_filename = os.path.join(data_directory, 'yahoo_prices.txt') 
    sys.stderr.write('''Pulling Out Yahoo Prices...\n''')
    try:
        price_data = open(yahoo_filename, 'r')
        yahoo_prices = pickle.load(price_data)
        price_data.close()
    except IOError as e:
        yahoo_prices = YahooPrices.YahooPrices(data_directory)
        price_data = open(yahoo_filename, 'w')
        pickle.dump(yahoo_prices, price_data)
        price_data.close()
    
    sys.stderr.write('''Loading current team...\n''')
    try:
        team = __import__(data_directory + '.team', fromlist = ['team'])
        team = getattr(team, 'team')
    except ImportError:
        sys.stderr.write('Unable to load team\n')
        team = {}
        raise
    
    cbs_projections = {}
    
    for position in POSITIONS:
        sys.stderr.write('''Pulling Out CBS Projections for %s...\n'''
                         %(position))
        cbs_filename = os.path.join(data_directory, '%s.txt' %(position))

        try:
            cbs_data = open(cbs_filename, 'r')
            cbs_projections[position] = pickle.load(cbs_data)
            cbs_data.close()
        except:
            sys.stderr.write('''Downloading CBS Projections for %s...\n'''
                             %(position))
            cbs_projections[position] = CBSProjections.CBSProjections((position,
                                                                       args.week,
                                                                       ''))
            cbs_data = open(cbs_filename, 'w')
            pickle.dump(cbs_projections[position], cbs_data)
            cbs_data.close()
    
        for player in cbs_projections[position]:
            if position != 'DST':
                name = CBSProjections.ShortName(player[0], 1)
                key = (name, player[1], player[2])
            else:
                key = player
            
            if key in yahoo_prices:
                price = yahoo_prices[key]
            
                # if key in team:
                #     sys.stderr.write('''%s - %.2f - %.2f\n''' %(key, team[key],
                #                                                 price))
                #     if team[key] < price:
                #         price = team[key]
                #         sys.stderr.write('''Actual price $%.2f\n''' % price)
                if key in team and team[key] < price: price = team[key]
                print '''%.2f, %.2f, %s''' % (
                    cbs_projections[position][player], price,
                    ', '.join(key))
            elif position != 'DST':
                name = CBSProjections.ShortName(player[0], 2)
                key = (name, player[1], player[2])
                if key in yahoo_prices:
                    price = yahoo_prices[key]
                    if key in team and team[key] < price: price = team[key]
                    print '''%.2f, %.2f, %s''' % (
                        cbs_projections[position][player], price,
                        ', '.join(key))
                else:
                    sys.stderr.write(
                        '\t### %s NOT FOUND USING KEY %s###\n' % (
                            str(player), key
                        )
                    )
            if key in team:
                sys.stderr.write("%s\tPrice: $%.2f\n" % (key, price))


if __name__ == '''__main__''':
    main()
