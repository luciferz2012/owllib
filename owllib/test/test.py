from unittest import TestCase, main
from codecs import open

from rdflib.term import URIRef

from owllib.test.model import OWLOntology


class TestOntology(TestCase):
	def test_new(self):
		IRI = URIRef('a')
		versionIRI = URIRef('b')
		ont1 = OWLOntology(IRI)
		ont2 = OWLOntology(IRI)
		ont3 = OWLOntology(IRI, versionIRI)
		self.assertEqual(ont1, ont2)
		self.assertNotEqual(ont1, ont3)

	def test_init(self):
		OWLOntology()

	def test_load(self, location='../ont/test.n3'):
		f = open(location, encoding='utf-8')
		ont = OWLOntology.load(file=f, owlFormat='n3')
		f.close()
		return ont

	def test_load_same_IRI(self):
		ont1 = OWLOntology.load(location='http://eulersharp.sourceforge.net/2003/03swap/workflow')
		ont2 = OWLOntology.load(location='http://eulersharp.sourceforge.net/2003/03swap/workflow')
		self.assertEqual(ont1, ont2)

	def test_directImports(self):
		ont = self.test_load('../ont/import.n3')
		self.assertEqual(len(ont.directImports), 2)

	def test_imports(self):
		ont = self.test_load('../ont/import.n3')
		self.assertEqual(len(ont.imports), 2)


if __name__ == '__main__':
	main()