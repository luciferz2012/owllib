# coding=utf-8

from logging import debug

from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, RDFS, OWL
from rdflib.util import guess_format
from rdflib.plugin import PluginException


class OWLEntity:
	def __init__(self, ontology, IRI=None, new=True):
		self.__funcDict = {}
		self.__version = 0
		self.__ont = ontology
		self.__IRI = IRI
		if not IRI:
			self.__IRI = BNode()
		if new:
			self.ont.add(self.IRI, RDF.type, self.type)

	@staticmethod
	def check(func):
		def wrapper(self, *args):
			version = self.ont.getVersion(self.IRI)
			if self.__version < version:
				self.__funcDict = {}
				self.__version = version
			return func(self, *args)

		return wrapper

	@staticmethod
	def checkOntology(func):
		@OWLEntity.check
		def wrapper(self):
			if func in self.__funcDict:
				return self.__funcDict[func]
			debug('run: ' + str(func))
			result = func(self)
			self.__funcDict[func] = result
			return result

		return wrapper

	@staticmethod
	def checkIRI(func):
		@OWLEntity.check
		def wrapper(self, entity):
			IRIDict = self.__funcDict.get(func, {})
			if entity.IRI in IRIDict:
				return IRIDict[entity.IRI]
			debug('run: ' + str(func) + ', IRI: ' + str(entity.IRI))
			result = func(self, entity)
			IRIDict[entity.IRI] = result
			self.__funcDict[func] = IRIDict
			return result

		return wrapper

	@property
	def ont(self):
		return self.__ont

	@property
	def IRI(self):
		return self.__IRI

	@property
	def type(self):
		raise NotImplementedError

	def __str__(self):
		return self.IRI


class OWLClass(OWLEntity):
	def __init__(self, ontology, IRI=None, new=True):
		self.__type = OWL.Class
		if not IRI or isinstance(IRI, BNode):
			self.__type = OWL.Restriction
		super(OWLClass, self).__init__(ontology, IRI, new)

	@property
	def type(self):
		return self.__type

	@property
	@OWLEntity.checkOntology
	def individuals(self):
		return [OWLIndividual(self.ont, s, False) for s, p, o in self.ont.query(None, RDF.type, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def subClasses(self):
		return [OWLClass(self.ont, s, False) for s, p, o in self.ont.query(None, RDFS.subClassOf, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def superClasses(self):
		return [OWLClass(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, RDFS.subClassOf, None)]


class OWLIndividual(OWLEntity):
	@property
	def type(self):
		return OWL.NamedIndividual

	@OWLEntity.checkIRI
	def getDataPropertyValues(self, dataProperty):
		return [o for s, p, o in self.ont.query(self.IRI, dataProperty.IRI, None)]

	@OWLEntity.checkIRI
	def getObjectPropertyValues(self, objectProperty):
		return [OWLIndividual(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, objectProperty.IRI, None)]


class OWLProperty(OWLEntity):
	@property
	@OWLEntity.checkOntology
	def domains(self):
		return [OWLClass(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, RDFS.domain, None)]

	@property
	@OWLEntity.checkOntology
	def ranges(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def subProperties(self):
		raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def superProperties(self):
		raise NotImplementedError

	@property
	def functional(self):
		return OWL.FunctionalProperty in self.ont.getTypes(self)


class OWLDataProperty(OWLProperty):
	@property
	def type(self):
		return OWL.DatatypeProperty

	@property
	@OWLEntity.checkOntology
	def ranges(self):
		return [o for s, p, o in self.ont.query(self.IRI, RDFS.range, None)]

	@property
	@OWLEntity.checkOntology
	def subProperties(self):
		return [OWLDataProperty(self.ont, s, False) for s, p, o in self.ont.query(None, RDFS.subPropertyOf, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def superProperties(self):
		return [OWLDataProperty(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, RDFS.subPropertyOf, None)]


class OWLObjectProperty(OWLProperty):
	@property
	def type(self):
		return OWL.ObjectProperty

	@property
	@OWLEntity.checkOntology
	def ranges(self):
		return [OWLClass(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, RDFS.range, None)]

	@property
	@OWLEntity.checkOntology
	def subProperties(self):
		return [OWLObjectProperty(self.ont, s, False) for s, p, o in self.ont.query(None, RDFS.subPropertyOf, self.IRI)]

	@property
	@OWLEntity.checkOntology
	def superProperties(self):
		return [OWLObjectProperty(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, RDFS.subPropertyOf, None)]

	@property
	@OWLEntity.checkOntology
	def inverses(self):
		p1 = [OWLObjectProperty(self.ont, o, False) for s, p, o in self.ont.query(self.IRI, OWL.inverseOf, None)]
		p2 = [OWLObjectProperty(self.ont, s, False) for s, p, o in self.ont.query(None, OWL.inverseOf, self.IRI)]
		return p1 + p2

	@property
	def asymmetric(self):
		return OWL.AsymmetricProperty in self.ont.getTypes(self)

	@property
	def inverseFunctional(self):
		return OWL.InverseFunctionalProperty in self.ont.getTypes(self)

	@property
	def irreflexive(self):
		return OWL.IrreflexiveProperty in self.ont.getTypes(self)

	@property
	def reflexive(self):
		return OWL.ReflexiveProperty in self.ont.getTypes(self)

	@property
	def symmetric(self):
		return OWL.SymmetricProperty in self.ont.getTypes(self)

	@property
	def transitive(self):
		return OWL.TransitiveProperty in self.ont.getTypes(self)


class OWLOntology(OWLEntity):
	__guessFormats = {'n3'}  # TODO

	def __init__(self, IRI=None, graph=None):
		self.__graph = graph
		if not graph:
			self.__graph = Graph()
		self.__IRIDict = {}
		super(OWLOntology, self).__init__(self, IRI)

	def add(self, s, p, o):
		self.__graph.add((s, p, o))
		self.__update(s)
		self.__update(p)

	def query(self, s, p, o):
		return self.__graph.triples((s, p, o))

	def getVersion(self, IRI):
		return self.__IRIDict.get(IRI, 0)

	def __update(self, IRI):
		self.__IRIDict[IRI] = self.getVersion(IRI) + 1
		self.__IRIDict[self.IRI] = self.getVersion(self.IRI) + 1

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
			triples = [(p, o) for p, o in graph.predicate_objects(IRI)]
			if maxNumOfTriples < len(triples):
				maxNumOfTriples = len(triples)
				maxIRI = IRI
		ont = OWLOntology(maxIRI, graph)
		return ont

	def save(self):
		raise NotImplementedError

	@OWLEntity.checkIRI
	def getTypes(self, entity):
		return [o for s, p, o in self.query(entity.IRI, RDF.type, None)]

	# @property
	# @OWLEntity.checkOntology
	# def directImports(self):
	# raise NotImplementedError
	#
	# @property
	# @OWLEntity.checkOntology
	# def imports(self):
	# raise NotImplementedError
	#
	# @property
	# @OWLEntity.checkOntology
	# def entities(self):
	# raise NotImplementedError

	@property
	@OWLEntity.checkOntology
	def classes(self):
		owlClasses = [OWLClass(self, s, False) for s, p, o in self.query(None, RDF.type, OWL.Class)]
		owlRestrictions = [OWLClass(self, s, False) for s, p, o in self.query(None, RDF.type, OWL.Restriction)]
		return owlClasses + owlRestrictions

	@property
	@OWLEntity.checkOntology
	def individuals(self):
		return [OWLIndividual(self, s, False) for s, p, o in self.query(None, RDF.type, OWL.NamedIndividual)]

	@property
	@OWLEntity.checkOntology
	def dataProperties(self):
		return [OWLDataProperty(self, s, False) for s, p, o in self.query(None, RDF.type, OWL.DatatypeProperty)]

	@property
	@OWLEntity.checkOntology
	def objectProperties(self):
		return [OWLObjectProperty(self, s, False) for s, p, o in self.query(None, RDF.type, OWL.ObjectProperty)]