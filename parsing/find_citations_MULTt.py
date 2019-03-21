import pandas as pd
import urllib
from argparse import ArgumentParser
from http.cookiejar import CookieJar
from scrapy.selector import Selector
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing
import time


def get_citations_for_page(url, buf, artid):
    req = urllib.request.Request(url, headers={'User-Agent': "Chrome/35.0.1916.47"})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(req).read()

    res = Selector(text=html).xpath('//*[@class="searchArea"]/td[1]/a/@href')
    citations = []
    for ref in res:
        cit_url = ref.get()
        citation_id = cit_url.split('eid=')[1].split('&origin')[0]
        citations.append(citation_id)
    buf.append(artid+':::'+'|'.join(citations) + u'\r\n')
    return citations


if __name__ == '__main__':
    parser = ArgumentParser(description='Scopus citations finder')
    parser.add_argument('start', help='dataset citaion parsing start', type=int)
    parser.add_argument('finish', help='dataset citaion parsing finish', type=int)
    parser.add_argument('dump_name', help='citations dump file name')

    args = parser.parse_args()
    articles = pd.read_csv('./articles.csv')
    citation_ids = articles['citationID'].values
    artids = articles['scopusID'].values
    num_cores = 4
    with open(args.dump_name, 'w') as citations:
        batch = num_cores * 4
        for j in range(args.start, args.finish, batch):
            buf=[]
            Parallel(n_jobs=num_cores, backend="threading")(
                delayed(get_citations_for_page)(citation_ids[i],buf, artids[i]) for i in range(j, j + batch))
            citations.write(''.join(buf))
            time.sleep(0.5)
            print(j)