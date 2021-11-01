description = """
 SELECT ?des WHERE  {
   wd:Q9570 schema:description ?des;
   FILTER ( lang(?des) = "hi" )
}
 """

alias = """
SELECT ?alt WHERE {
  wd:Q9570 skos:altLabel ?alt . 
  FILTER ( lang(?alt) = "hi" )
}
"""

gen_query = lambda x: f"""
SELECT  ?item ?itemLabel WHERE {{
    wd:Q9570 wdt:{x} ?item.
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "hi,en". }}
}}
"""

birth_query = """
SELECT  ?dateLabel ?placeLabel WHERE {
  wd:Q9570  wdt:P569 ?date;
            wdt:P19 ?place.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "hi,en". }
}
"""

follower_query = """
SELECT  (SUM(?f) AS ?sum) WHERE {
  wd:Q9570  wdt:P8687 ?f.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "hi,en". }
}
"""

film_cnt_query = """
SELECT DISTINCT (COUNT(*) AS ?count) WHERE {
  ?fi wdt:P161 wd:Q9570 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "hi,en". }
}
"""

film_query = """
SELECT ?fiLabel ?perc WHERE {
  ?fi wdt:P161 wd:Q9570;
      wdt:P444 ?pop.
  FILTER regex(str(?pop), "%").
  BIND(xsd:integer(REPLACE(STR(?pop), "\\\\W", "", "i")) AS ?perc) .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "hi,en". }
}
ORDER BY DESC(?perc)
LIMIT 5
"""

image_query = """
SELECT  ?im WHERE {
  wd:Q9570 wdt:P18 ?im
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?im)
LIMIT 1

"""
