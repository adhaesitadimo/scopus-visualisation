import json
import os
import pandas as pd

if __name__ == "__main__":
    data = {'id': [], 'title': [], 'creator': [], 'date': [], 'pubName': [], 'volume': [], 'pageNum': [],
            'citationID': []}
    for file in os.listdir('dumps'):
        print(file)
        with open('dumps/' + file, 'r') as dumps:
            for line in dumps:
                tree = json.loads(line)
                #print(tree['search-results'])
                #print(tree['search-results']['opensearch:startIndex'])
                if int(tree['search-results']['opensearch:totalResults']) > \
                        int(tree['search-results']['opensearch:startIndex']):
                    for article in tree['search-results']['entry']:
                        try:
                            a = article['dc:title']
                            data['id'].append(article['dc:identifier'])
                            data['title'].append(article['dc:title'])
                        except:
                            continue
                        try:
                            data['creator'].append(article['dc:creator'])
                            #print(article['dc:creator'])
                        except:
                            data['creator'].append('unknown')
                            #print('unknown')
                        try:
                            data['date'].append(article['prism:coverDate'])
                            #print(article['prism:coverDate'])
                        except:
                            data['date'].append(file[-8:-5] + '-01-01')
                            #print(file[-8:-5] + '-01-01')
                        try:
                            data['pubName'].append(article['prism:publicationName'])
                            #print(article['prism:publicationName'])
                        except:
                            data['pubName'].append('unknown')
                            #print('unknown')
                        try:
                            data['volume'].append(article['prism:volume'])
                            #print(article['prism:volume'])
                        except:
                            data['volume'].append('unknown')
                            #print('unknown')
                        try:
                            pagerange = str.replace(article['prism:pageRange'], 'S', '')
                            data['pageNum'].append(int(pagerange.split('-')[1]) - int(
                                pagerange.split('-')[0]))
                            #print(int(article['prism:pageRange'].split('-')[1]) - int(
                            #    article['prism:pageRange'].split('-')[0]))
                        except:
                            data['pageNum'].append('unknown')
                            #print('unknown')
                        data['citationID'].append(article['link'][3]['@href'])
                        #print(article['link'][3]['@href'])
                # print(type(tree['search-results']['entry'][0]['dc:identifier']))
                #break
    article_dataset = pd.DataFrame(data=data)
    print(len(data['id']))
    print(len(data['title']))
    article_dataset.to_csv('articles.csv')