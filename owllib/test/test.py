from unittest import TestCase, main
from codecs import open

from rdflib import RDF, OWL
from rdflib.term import URIRef

from owllib.test.model import OWLOntology, OWLClass


class TestOntology(TestCase):
	def test_init(self):
		OWLOntology()

	def test_version(self):
		ont = self.test_load()
		v1 = ont.version
		ont.add(ont.IRI, RDF.type, OWL.Class)
		v2 = ont.version
		self.assertNotEqual(v1, v2)

	def test_load(self, location='../ont/test.n3'):
		f = open(location, encoding='utf-8')
		ont = OWLOntology.load(file=f, owlFormat='n3')
		f.close()
		return ont

	def test_classes(self):
		ont = self.test_load()
		for c in ont.classes:
			print(c)

	def test_individual(self):
		ont = self.test_load()
		for i in ont.individuals:
			print(i)


class TestClass(TestCase):
	@property
	def ontology(self):
		return TestOntology().test_load()

	def test_init(self):
		ont = OWLOntology()
		IRI = URIRef('123')
		OWLClass(ont, IRI)
		OWLClass(ont, IRI)
		OWLClass(ont, IRI)
		for c in self.ontology.classes:
			print(c)

	def test_type(self):
		cls = OWLClass(OWLOntology())
		self.assertEqual(cls.type, OWL.Class)

	def test_individuals(self):
		for c in self.ontology.classes:
			for i in c.individuals:
				print(i)

	def test_subClass(self):
		for c in self.ontology.classes:
			for s in c.subClasses:
				print('%s is the sub class of %s' % (s, c))

	def test_superClass(self):
		for c in self.ontology.classes:
			for s in c.superClasses:
				print('%s is the super class of %s' % (s, c))


if __name__ == '__main__':
	main()