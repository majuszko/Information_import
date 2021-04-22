#!/usr/bin/python
import argparse
import pandas as pd
import xml.etree.ElementTree as et
from pathlib import Path

def parse_XML(xml_file, df_cols):
    rows = []
    it = et.iterparse(xml_file)
    for _, el in it:
        prefix, has_namespace, postfix = el.tag.rpartition('}')
        if has_namespace:
            el.tag = postfix
    root = it.root
    for node in root.iter():
        res = []
        for el in df_cols[0:]:
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else:
                res.append(None)
        rows.append({df_cols[i]: res[i] for i, _ in enumerate(df_cols)})
    out_df = pd.DataFrame(rows, columns=df_cols)
    out_df = out_df.dropna(how='all')
    out_df = out_df.fillna(method='ffill').fillna(method='bfill')
    out_df = out_df.drop_duplicates(keep='first')
    return out_df

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('type', type=str)
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    type = str(args.type)
    file = Path(args.file)

    df_cols_aaa = ["flstkennz", "flaeche", "landschl", "kreisschl", "gmdschl", "gemaschl"]
    df_cols_nas = ["flurstueckskennzeichen", "amtlicheFlaeche", "land", "kreis", "gemeinde", "gemarkungsnummer"]

    types = ["aaa", "nas"]

    if type==types[0]:
        print(parse_XML(file, df_cols_aaa))
    if type==types[1]:
        print(parse_XML(file, df_cols_nas))
    if type not in types:
        print("Invalid data format")