"""
Seo checker

Usage:
    seocheck.py <file> [--start-from-line n]

Options:
    -h --help   Show this screen
    --start-from-line n   Skip the first n lines from the file
"""

import csv
import requests

from bs4 import BeautifulSoup

from docopt import docopt


COLUMNS_MAPPING = {
    'url': 1,
    'title': 4,
    # 'meta-keyword': 6,
    'h1': 8
}


def main():
    arguments = docopt(__doc__, version='Seo checker 0.1')
    print(arguments)
    with open(arguments['<file>']) as f:
        reader = csv.reader(f)

        start_from_line = int(arguments.get('--start-from-line', 1)) - 1
        [next(reader) for i in range(start_from_line)]

        for line in reader:
            url = line[COLUMNS_MAPPING['url']]
            print('Processing URL: {}'.format(url))
            response = requests.get(url)
            if response.status_code != 200:
                print('Bad URL')
            soup = BeautifulSoup(response.text)

            # check title
            title = soup.title.string.strip()
            title_expected = line[COLUMNS_MAPPING['title']].strip()
            if title != title_expected:
                print('''
                    Bad title, current: {}
                    expected: {}
                '''.format(title, title_expected))

            # check keywords:
            #keywords = soup.find('meta', attrs={'name': 'keywords'})
            #print(keywords)

            # check h1
            h1 = soup.find('h1').get_text().strip()
            h1_expected = line[COLUMNS_MAPPING['h1']].strip()
            if h1 != h1_expected:
                print('''
                    Bad h1, current: {}
                    expected: {}
                '''.format(h1, h1_expected))


            print('-' * 40)


if __name__ == '__main__':
    main()
