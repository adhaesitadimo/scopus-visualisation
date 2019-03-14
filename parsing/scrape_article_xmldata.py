import time
import urllib
from argparse import ArgumentParser
from tqdm import tqdm
from scrapy.http import HtmlResponse

#apikey = 'e171400828c955f27fb5036c8ffeffa2'


def get_page(start, subject, date):
    url = 'https://api.elsevier.com/content/search/scopus?start={start}&count=25' \
          '&query=all%28gene%29&date={date}&sort=citedby-count&subj={subject}&apiKey={key}'.format(start=start,
                                                                                                   key=args.apikey,
                                                                                                   date=date,
                                                                                                   subject=subject)
    req = urllib.request.Request(url, headers={'User-Agent': "Chrome/35.0.1916.47"})
    html = urllib.request.urlopen(req).read()
    #html_response = HtmlResponse(url, body=html)
    #print(html)
    return html


if __name__ == '__main__':
    parser = ArgumentParser(description='Scopus pages scraper')
    parser.add_argument('apikey', help='your api key')
    parser.add_argument('startpage', help='which request page starts search', type=int)
    parser.add_argument('finishpage', help='which request page finishes search', type=int)
    parser.add_argument('subject', help='paper subject')
    parser.add_argument('date', help='publication date')
    parser.add_argument('dump_name', help='xml dump file name')

    args = parser.parse_args()
    for year in range(2010, 2018):
        print(year)
        with open('xmldump' + str(year) + args.subject + '.txt', 'wb') as dumps:
            for start in tqdm(range(args.startpage, args.finishpage, 25)):
                try:
                    dump = get_page(start, args.subject, year)
                    # print(type(dump))
                    dumps.write(dump + b'\r\n')
                    time.sleep(1)
                except:
                    break
