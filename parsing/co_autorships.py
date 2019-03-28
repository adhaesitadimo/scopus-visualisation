from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc, AbsDoc
from tqdm import tqdm
import json
import pandas as pd

## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'])


def autorships(dataset_name, aut_dump_name):
    data = pd.read_csv(dataset_name)
    ids = data['scopusID'].values

    with open(aut_dump_name, 'w') as aut:
        num = 0
        for id in tqdm(ids):
            scp_doc = AbsDoc(scp_id=id.split(':')[1])
            if scp_doc.read(client):
                scp_doc.write()
            else:
                print("Read document failed.")
                aut.write('None' + u'\r\n')
                continue
            num += 1
            try:
                aut.write(';'.join([':'.join([i['ce:indexed-name'], i['@auid']])
                                    for i in scp_doc.data['authors']['author']]) + u'\r\n')
            except:
                aut.write('None' + u'\r\n')
