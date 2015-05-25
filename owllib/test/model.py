# coding=utf-8

from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, RDFS, OWL
from rdflib.util import guess_format
from rdflib.plugin import PluginException


class OWLObject:
	def __init__(self, IRI=None):
		if IRI:
			self.__IRI = IRI
		else:
			self.__IRI = BNode()

	@property
	def IRI(self):
		return self.__IRI

	def __str__(self):
		return self.IRI

	def getAnnotationProperties(self, annotationProperty=None):
		raise NotImplementedError


class OWLAnnotationProperty:
	# isComment
	# isDeprecated
	# isLabel
	pass


class OWLEntity(OWLObject):
	def __init__(self, ontology, IRI=None):
		super(OWLEntity, self).__init__(IRI)
		self.__ont = ontology
		self.__funcDict = {}
		self.ontology.add(self.IRI, RDF.type, self.type)

	@property
	def ontology(self):
		return self.__ont

	@property
	def type(self):
		raise NotImplementedError

	@staticmethod
	def checkOntology(func):
		def wrapper(self, *args):
			version, result = self.__funcDict.get(func, (-1, None))
			if version < self.ontology.version:
				result = func(self, *args)
				self.__funcDict[func] = (self.ontology.version, result)
			return result

		return wrapper


class OWLClass(OWLEntity):
	@property
	def type(self):
		return OWL.Class

	@property
	@OWLEntity.checkOntology
	def individuals(self):
		return [OWLIndividual(self.ontology, s) for s, p, o in self.ontology.query(None, RDF.type, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def subClasses(self):
		return [OWLClass(self.ontology, s) for s, p, o in self.ontology.query(None, RDFS.subClassOf, self.IRI)]

	@property
	def superClasses(self):
		return [OWLClass(self.ontology, o) for s, p, o in self.ontology.query(self.IRI, RDFS.subClassOf, None)]


class OWLIndividual(OWLEntity):
	@property
	def type(self):
		return OWL.NamedIndividual

	def getDataProperties(self, dataProperty=None):
		raise NotImplementedError

	def getObjectProperties(self, objectProperty=None):
		raise NotImplementedError


class OWLProperty(OWLEntity):
	# set ontologySet
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


class OWLOntology(OWLObject):
	__guessFormats = {'n3'}  # TODO

	def __init__(self, IRI=None):
		super(OWLOntology, self).__init__(IRI)
		self.__graph = Graph()
		self.__version = 0
		self.add(self.IRI, RDF.type, OWL.Ontology)

	def __update(self):
		self.__version += 1

	@property
	def version(self):
		return self.__version

	def add(self, s, p, o):
		self.__graph.add((s, p, o))
		self.__update()

	def query(self, s, p, o):
		return self.__graph.triples((s, p, o))

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

	@property
	def directImports(self):
		raise NotImplementedError

	@property
	def imports(self):
		raise NotImplementedError

	@property
	def allEntities(self):
		raise NotImplementedError

	@property
	def classes(self):
		return [OWLClass(self, s) for s, p, o in self.query(None, RDF.type, OWL.Class)]

	@property
	def individuals(self):
		return [OWLIndividual(self, s) for s, p, o in self.query(None, RDF.type, OWL.NamedIndividual)]

	@property
	def dataProperties(self):
		raise NotImplementedError

	@property
	def objectProperties(self):
		raise NotImplementedError

	@property
	def annotationProperties(self):
		raise NotImplementedError