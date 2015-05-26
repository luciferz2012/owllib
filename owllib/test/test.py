from unittest import TestCase, main
from codecs import open
from logging import basicConfig, INFO, info

from rdflib import RDF, OWL
from rdflib.term import URIRef

from owllib.test.model import OWLOntology, OWLClass, OWLIndividual, OWLDataProperty, OWLObjectProperty


def Ont(location='../ont/test.n3'):
	return TestOntology().test_load(location)


basicConfig(filename='test.log', filemode='w', level=INFO)


class TestEntity(TestCase):
	def test_check(self):
		ont = Ont()
		c1 = ont.classes
		c2 = ont.classes
		for p in ont.dataProperties:
			for i in ont.individuals:
				i.getDataPropertyValues(p)
		self.assertEqual(c1, c2)


class TestClass(TestCase):
	def test_init(self):
		ont = OWLOntology()
		IRI = URIRef('123')
		OWLClass(ont, IRI)
		OWLClass(ont, IRI)
		OWLClass(ont, IRI)
		for c in Ont().classes:
			info(c)

	def test_type(self):
		IRI = URIRef('123')
		cls = OWLClass(Ont(), IRI)
		self.assertEqual(cls.type, OWL.Class)
		cls = OWLClass(Ont())
		self.assertEqual(cls.type, OWL.Restriction)

	def test_individuals(self):
		for c in Ont().classes:
			for i in c.individuals:
				info(i)

	def test_subClasses(self):
		for c in Ont().classes:
			for s in c.subClasses:
				info('%s is the sub class of %s' % (s, c))

	def test_superClasses(self):
		for c in Ont().classes:
			for s in c.superClasses:
				info('%s is the super class of %s' % (s, c))


class TestIndividual(TestCase):
	def test_init(self):
		OWLIndividual(Ont())

	def test_dataPropertyValues(self):
		for i in Ont().individuals:
			for p in Ont().dataProperties:
				info(i.getDataPropertyValues(p))

	def test_objectPropertyValues(self):
		for i in Ont().individuals:
			for p in Ont().objectProperties:
				info(i.getObjectPropertyValues(p))


class TestProperty(TestCase):
	def test_domains(self):
		for p in Ont().dataProperties:
			for d in p.domains:
				info(d)


class TestDataProperty(TestCase):
	def test_init(self):
		OWLDataProperty(Ont())

	def test_range(self):
		for p in Ont().dataProperties:
			for r in p.ranges:
				info(r)

	def test_subProperties(self):
		for p in Ont().dataProperties:
			for s in p.subProperties:
				info('%s is the sub property of %s' % (s, p))

	def test_superProperties(self):
		for p in Ont().dataProperties:
			for s in p.superProperties:
				info('%s is the super property of %s' % (s, p))


class TestObjectProperty(TestCase):
	def test_init(self):
		OWLObjectProperty(Ont())

	def test_range(self):
		for p in Ont().objectProperties:
			for r in p.ranges:
				info(r)

	def test_subProperties(self):
		for p in Ont().objectProperties:
			for s in p.subProperties:
				info('%s is the sub property of %s' % (s, p))

	def test_superProperties(self):
		for p in Ont().objectProperties:
			for s in p.superProperties:
				info('%s is the super property of %s' % (s, p))

	def test_inverse(self):
		for p in Ont().objectProperties:
			for q in p.inverses:
				info('%s is the inverse of %s' % (p, q))

	def test_types(self):
		for p in Ont().objectProperties:
			info(p.functional)
			info(p.asymmetric)
			info(p.inverseFunctional)
			info(p.irreflexive)
			info(p.reflexive)
			info(p.symmetric)
			info(p.transitive)


class TestOntology(TestCase):
	def test_init(self):
		OWLOntology()

	def test_version(self):
		ont = self.test_load()
		cls = OWLClass(ont)
		o1 = ont.getVersion(ont.IRI)
		v1 = ont.getVersion(cls.IRI)
		ont.add(cls.IRI, RDF.type, OWL.Class)
		o2 = ont.getVersion(ont.IRI)
		v2 = ont.getVersion(cls.IRI)
		info((o1, o2, v1, v2))
		self.assertNotEqual(o1, o2)
		self.assertNotEqual(v1, v2)

	def test_load(self, location='../ont/test.n3'):
		f = open(location, encoding='utf-8')
		ont = OWLOntology.load(file=f, owlFormat='n3')
		f.close()
		return ont

	def test_save(self):
		ont = Ont()
		OWLClass(ont, URIRef('AddedClass'))
		ont.save('../ont/save.n3', 'n3')

	def test_classes(self):
		for c in Ont().classes:
			info(c)

	def test_individuals(self):
		for i in Ont().individuals:
			info(i)

	def test_dataProperties(self):
		for p in Ont().dataProperties:
			info(p)

	def test_objectProperties(self):
		for p in Ont().objectProperties:
			info(p)


if __name__ == '__main__':
	main()