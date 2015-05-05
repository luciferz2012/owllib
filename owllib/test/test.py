from unittest import TestCase, main
from codecs import open

from owllib.test.model import OWLOntology


class TestOntology(TestCase):
	def test_init(self):
		OWLOntology()

	def test_load(self):
		ont = OWLOntology()
		f = open('../ont/test.n3', encoding='utf-8')
		ont.load(file=f, owlFormat='n3')
		f.close()
		return ont

	def test_directImports(self):
		ont = self.test_load()
		for imp in ont.directImports:
			print(imp)


if __name__ == '__main__':
	main()