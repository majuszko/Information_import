#!/usr/bin/python
import argparse
import pandas as pd
import xml.etree.ElementTree as eT
from pathlib import Path


def parse_xml(xml_file, df_cols):
    rows = []
    it = eT.iterparse(xml_file)
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


def set_format(form, xmlfile) -> bool:
    df_cols_aaa = ['flstkennz', 'flaeche', 'landschl', 'kreisschl', 'gmdschl', 'gemaschl']
    df_cols_nas = ['flurstueckskennzeichen', 'amtlicheFlaeche', 'land', 'kreis', 'gemeinde', 'gemarkungsnummer']

    forms = ['aaa', 'nas']

    if form == forms[0]:
        print(parse_xml(xmlfile, df_cols_aaa))
        return True
    if form == forms[1]:
        print(parse_xml(xmlfile, df_cols_nas))
        return True
    if form not in forms:
        print('Invalid data format')
        return False


def test_parse_xml():
    xml = 'testfile.xml'
    parse = parse_xml(xml, ['to', 'from', 'heading', 'body'])
    d = {'to': ['Tove'], 'from': ['Jani'], 'heading': ['Reminder'], 'body': ["Don't forget me this weekend!"]}
    df = pd.DataFrame(data=d)
    assert parse.equals(df)


def test_set_format():
    assert set_format('aaa', 'testfile.xml')
    assert not set_format('ooo', 'testfile.xml')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('type', type=str)
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    f = str(args.type)
    file = Path(args.file)

    set_format(f, file)
