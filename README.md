# Visualising Scopus paper universe
This is Scopus graph visualisation project for Applied Graph Theory and Visualisation bachelors' course. The aim is to gain visual understanding of Scopus by drawing co-autorships and citation graphs. The project consists of the following stages:

Data acquiring (<i>scraping</i> part):

1. <i>scrape_article_xmldata.py</i> makes requests using Scopus Web Api and writes binary xml(JSON) dump into text file

2. <i>xml_parser.py</i> parses available dumps for ID, title, authors, publication date, publisher, volume, number of pages and citations and collects them into Pandas dataset

#TODO TODO TODOO
