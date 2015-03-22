# coding=utf-8

from rdflib import RDF, RDFS, OWL
from rdflib.term import URIRef, Literal

from owllib.ontology import Ontology
from owllib.entities import Class


ont = Ontology()
ont.load(location='ont/syntax.n3')
uri = URIRef('123')
label = Literal('测试', lang='zh-hans')
# cls = Class()
# cls.triples.add((uri, RDF.type, OWL.Class))
# cls.triples.add((uri, RDFS.label, label))
# ont.classes.add(cls)
# ont.sync_entity_to_graph(cls)
ont.classes.add(Class(uri, None, {label}))
ont.sync_to_graph()
ont.sync_from_graph()

for cls in ont.classes:
	if cls.is_named:
		print(cls.labels)
		for s, p, o in cls.triples:
			print(s, p, o)

ont.graph.serialize('ont/test.n3', format='n3')