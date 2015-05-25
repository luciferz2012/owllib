# coding=utf-8

from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, RDFS, OWL
from rdflib.util import guess_format
from rdflib.plugin import PluginException


class OWLEntity():
	def __init__(self, ontology, IRI=None):
		self.__funcDict = {}
		self.__ont = ontology
		if IRI:
			self.__IRI = IRI
		else:
			self.__IRI = BNode()
		self.ontology.add(self.IRI, RDF.type, self.type)

	@staticmethod
	def checkOntology(func):
		def wrapper(self, *args):
			version, result = self.__funcDict.get(func, (-1, None))
			if version < self.ontology.version:
				result = func(self, *args)
				self.__funcDict[func] = (self.ontology.version, result)
			return result

		return wrapper

	@property
	def ontology(self):
		return self.__ont

	@property
	def IRI(self):
		return self.__IRI

	@property
	def type(self):
		raise NotImplementedError

	def __str__(self):
		return self.IRI

	def getValues(self, key):
		return [self.ontology.getValue(o) for s, p, o in self.ontology.query(self.IRI, key.IRI, None)]


class OWLClass(OWLEntity):
	@property
	def type(self):
		return OWL.Class  # TODO OWL.Restriction

	@property
	@OWLEntity.checkOntology
	def individuals(self):
		return [OWLIndividual(self.ontology, s) for s, p, o in self.ontology.query(None, RDF.type, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def subClasses(self):
		return [OWLClass(self.ontology, s) for s, p, o in self.ontology.query(None, RDFS.subClassOf, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def superClasses(self):
		return [OWLClass(self.ontology, o) for s, p, o in self.ontology.query(self.IRI, RDFS.subClassOf, None)]


class OWLIndividual(OWLEntity):
	@property
	def type(self):
		return OWL.NamedIndividual


class OWLProperty(OWLEntity):
	@property
	def domains(self):
		raise NotImplementedError

	@property
	def ranges(self):
		raise NotImplementedError

	@property
	def subProperties(self):
		raise NotImplementedError

	@property
	def superProperties(self):
		raise NotImplementedError


class OWLDataProperty(OWLProperty):
	pass


class OWLObjectProperty(OWLProperty):
	@property
	def inverses(self):
		raise NotImplementedError

	def isAsymmetric(self):
		raise NotImplementedError

	def isInverseFunctional(self):
		raise NotImplementedError

	def isIrreflexive(self):
		raise NotImplementedError

	def isReflexive(self):
		raise NotImplementedError

	def isSymmetric(self):
		raise NotImplementedError

	def isTransitive(self):
		raise NotImplementedError


class OWLOntology(OWLEntity):
	__guessFormats = {'n3'}  # TODO

	def __init__(self, IRI=None):
		self.__graph = Graph()
		self.__version = 0
		super(OWLOntology, self).__init__(self, IRI)

	def add(self, s, p, o):
		self.__graph.add((s, p, o))
		self.__update()

	def query(self, s, p, o):
		return self.__graph.triples((s, p, o))

	@property
	def version(self):
		return self.__version

	def __update(self):
		self.__version += 1

	@property
	def type(self):
		return OWL.Ontology

	@staticmethod
	def __load(file=None, location=None, data=None, owlFormat=None):
		if location and not owlFormat:
			owlFormat = guess_format(location)
		graph = Graph()
		try:
			return graph.parse(file=file, location=location, data=data, format=owlFormat)
		except PluginException as e:
			for f in OWLOntology.__guessFormats:
				try:
					return graph.parse(file=file, location=location, data=data, format=f)
				except PluginException:
					pass
			raise e

	@staticmethod
	def load(file=None, location=None, data=None, owlFormat=None):
		graph = OWLOntology.__load(file, location, data, owlFormat)
		maxNumOfTriples = 0
		maxIRI = None
		for IRI in graph.subjects(RDF.type, OWL.Ontology):
			triples = [(p, o) for (p, o) in graph.predicate_objects(IRI)]
			if maxNumOfTriples < len(triples):
				maxNumOfTriples = len(triples)
				maxIRI = IRI
		ont = OWLOntology(maxIRI)
		ont.__graph = graph
		ont.__update()
		return ont

	def save(self):
		raise NotImplementedError

	def getTypes(self, IRI):
		return [o for s, p, o in self.query(IRI, RDF.type, None)]

	def getValue(self, IRI):
		types = self.getTypes(IRI)
		if OWL.Ontology in types:
			return OWLOntology(self, IRI)
		if OWL.Class in types:
			return OWLClass(self, IRI)
		if OWL.NamedIndividual in types:
			return OWLIndividual(self, IRI)
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def directImports(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def imports(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def entities(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def classes(self):
		return [OWLClass(self, s) for s, p, o in self.query(None, RDF.type, OWL.Class)]

	@property
	@OWLEntity.checkOntology
	def individuals(self):
		return [OWLIndividual(self, s) for s, p, o in self.query(None, RDF.type, OWL.NamedIndividual)]

	@property
	@OWLEntity.checkOntology
	def dataProperties(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def objectProperties(self):
		raise NotImplementedError
