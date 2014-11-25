#!/usr/bin/env python
from urllib import urlencode
import argparse
from subprocess import call
from os import path, mkdir
from time import sleep
from sys import stderr

indices = {
    'QB': 0,
    'RB': 1,
    'WR': 3,
    'TE': 6,
    'K': 0,
    'DST': 0,
}

pts = {
    'QB': 'O',
    'RB': 'O',
    'WR': 'O',
    'TE': 'O',
    'K': 'K',
    'DST': 'DT',
}

max_counts = {
    'QB': 125,
    'RB': 275,
    'WR': 375,
    'TE': 200,
    'K': 75,
    'DST': 50,
}

def main():
    url_list = []
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--position', choices = ['QB', 'RB', 'WR', 'TE',
                                                      'K', 'DST', 'all'])
    parser.add_argument('-w', '--week', type = int)
    parser.add_argument('-u', '--uid')
    parser.add_argument('-c', '--cookie')
    parser.add_argument('-o', '--output-dir')
    args = parser.parse_args()
    
    if args.position == 'all':
        for position in indices:
            url_list += build_url(uid = args.uid,
                                  week = args.week,
                                  position = position,
                                  output_dir = args.output_dir
                                 )
    else:
        url_list = build_url(uid = args.uid,
                             week = args.week,
                             position = args.position,
                             output_dir = args.output_dir
                            )

    if not path.isdir(args.output_dir):
        mkdir(args.output_dir)

    fetch_urls(url_list, args.cookie)

def build_url(uid, week, position, output_dir):
    url_list = []
    base_url = '''http://football.fantasysports.yahoo.com/salcap/'''

    url = base_url + uid + '/editplayers?'
    # buy=1&pt=O&week=${1}&index=0&stage=1&sort=SALARY&count="
    url_params = {
        'buy': 1,
        'pt': pts[position],
        'week': week,
        'index': indices[position],
        'stage': 1,
        'sort': 'SALARY',
    }
    
    params = urlencode(url_params)
    
    for count in range(0, max_counts[position], 25):
        full_url = url + params + '&count=%d' % count
        output_document = path.join(output_dir, position + str(count) + 
                                    '.html')
        url_list.append((full_url, output_document))

    return url_list

def fetch_urls(url_list, cookie_file):    
    f = open('/dev/null', 'w')
    for url in url_list:
        # only update if file doesn't exist
        # TODO: add option to force updating all files
        if not path.isfile(url[1]):
            stderr.write('Fetching %s...\n' % url[1])
            wget_cmd = ['wget','--load-cookies', cookie_file, '--output-document',
                        url[1], url[0]]
            call(wget_cmd, stdout = f, stderr = f)
            sleep(1)
    f.close()

if __name__ == '''__main__''':
    main()
