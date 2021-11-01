import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from copy import deepcopy
from datetime import datetime

import queries as qr
import templates as tp

endpoint_url = "https://query.wikidata.org/sparql"


def to_date(x):
    dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')
    s = f"{dt.strftime('%d')} {dt.strftime('%B')} {dt.strftime('%Y')}"
    return s


def get_results(qry, labels):
    labels = [x if x else 'itemLabel' for x in labels]
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(qry)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    values = response["results"]["bindings"]

    print(values)
    output = []
    for lb in labels:
        out = [x[lb]['value'] for x in values]
        if len(out) == 1:
            output.append(str(out[0]))
            continue
        out_str = ', '.join(out[:-1]) + ' और ' + out[-1]
        output.append(out_str)

    return output


def use(rule: str, query: str, labels=None, dates=None) -> list:
    if labels is None:
        labels = []
    ct = rule.count(tp.mask)
    labels += (ct - len(labels)) * [None]

    if dates is None:
        dates = []
    dates += (ct - len(dates)) * [None]

    temp = deepcopy(rule)
    response = get_results(query, labels)
    for (text, isDate) in zip(response, dates):
        temp = temp.replace(tp.mask, to_date(text) if isDate else text, 1)
    return [temp]


if __name__ == "__main__":
    result, text = [], f'{tp.name}\n'

    result += use(tp.intro, qr.description, ['des'])
    result += use(tp.alias, qr.alias, ['alt'])
    result += use(tp.occupation, qr.gen_query('P106'))
    result += use(tp.worth, qr.gen_query('P2218'))
    result += use(tp.followers, qr.follower_query, ['sum'])

    text += ' '.join(result) + '\n'
    result = []

    result += use(tp.birth, qr.birth_query, ['dateLabel', 'placeLabel'], [True])
    result += use(tp.edu, qr.gen_query('P69'))
    result += use(tp.citizen, qr.gen_query('P27'))

    text += ' '.join(result) + '\n'
    result = []

    text += '\n' + tp.family + '\n'
    result += use(tp.father, qr.gen_query('P22'))
    result += use(tp.mother, qr.gen_query('P25'))
    result += use(tp.spouse, qr.gen_query('P26'))
    result += use(tp.children, qr.gen_query('P40'))
    result += use(tp.religion, qr.gen_query('P140'))
    result += use(tp.lang, qr.gen_query('P103'))
    result += use(tp.residence, qr.gen_query('P551'))

    text += ' '.join(result) + '\n'
    result = []

    text += '\n' + tp.career + '\n'
    result += use(tp.work_start, qr.gen_query('P2031'), ['item'], [True])
    result += use(tp.film_cnt, qr.film_cnt_query, ['count'])
    result += use(tp.film, qr.film_query, ['fiLabel'])
    result += use(tp.award, qr.gen_query('P166'))

    text += ' '.join(result) + '\n'
    result = []

    result += use(tp.position, qr.gen_query('P39'))
    result += use(tp.event, qr.gen_query('P793'))

    text += ' '.join(result) + '\n'

    print(text)
    print()
    print("Link for image: ", get_results(qr.image_query, ['im'])[0])
