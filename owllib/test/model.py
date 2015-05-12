# coding=utf-8
from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, OWL
from rdflib.util import guess_format
from rdflib.plugin import PluginException


class OWLEntity:
	def __init__(self, IRI=None):
		if IRI:
			self._IRI = IRI
		else:
			self._IRI = BNode()

	@property
	def IRI(self):
		return self._IRI

	def getAnnotationProperties(self, annotationProperty=None):
		raise NotImplementedError


class OWLAnnotationProperty:
	# isComment
	# isDeprecated
	# isLabel
	pass


class OWLClass(OWLEntity):
	# set ontologySet
	@property
	def individuals(self):
		raise NotImplementedError

	@property
	def subClasses(self):
		raise NotImplementedError

	@property
	def superClasses(self):
		raise NotImplementedError


class OWLIndividual(OWLEntity):
	# set ontology
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


class OWLOntology(OWLEntity):
	_guessFormats = set(['n3'])  # TODO
	_IRIDict = {}

	def __new__(cls, IRI=None, versionIRI=None):
		self = super(OWLOntology, cls).__new__(cls)
		if IRI:
			ontDict = OWLOntology._IRIDict.get(IRI, {})
			OWLOntology._IRIDict[IRI] = ontDict
			self = ontDict.get(versionIRI, self)
			ontDict[versionIRI] = self
		return self

	def __init__(self, IRI=None, versionIRI=None):
		super(OWLOntology, self).__init__(IRI)
		if not hasattr(self, 'graph'):
			self.graph = Graph()
			self.graph.add((self.IRI, RDF.type, OWL.Ontology))
			if versionIRI:
				self.graph.add((self.IRI, OWL.versionIRI, versionIRI))
			self._directImports = None

	@staticmethod
	def _load(file=None, location=None, data=None, owlFormat=None):
		if location and not owlFormat:
			owlFormat = guess_format(location)
		graph = Graph()
		try:
			return graph.parse(file=file, location=location, data=data, format=owlFormat)
		except PluginException as e:
			for f in OWLOntology._guessFormats:
				try:
					return graph.parse(file=file, location=location, data=data, format=f)
				except PluginException:
					pass
			raise e

	@staticmethod
	def load(file=None, location=None, data=None, owlFormat=None):
		graph = OWLOntology._load(file, location, data, owlFormat)
		maxNumOfTriples = 0
		maxIRI = None
		for IRI in graph.subjects(RDF.type, OWL.Ontology):
			triples = [(p, o) for (p, o) in graph.predicate_objects(IRI)]
			if maxNumOfTriples < len(triples):
				maxNumOfTriples = len(triples)
				maxIRI = IRI
		if maxIRI in OWLOntology._IRIDict:
			return OWLOntology(maxIRI)
		else:
			ont = OWLOntology(maxIRI)
			ont.graph += graph
			return ont

	def save(self):
		raise NotImplementedError

	@property
	def directImports(self):
		if not self._directImports:
			self._directImports = set()
			for IRI in self.graph.objects(self.IRI, OWL.imports):
				self._directImports.add(OWLOntology.load(location=IRI))
		return self._directImports

	@property
	def imports(self):
		imps = set()
		for imp in self.directImports:
			imps.add(imp)
			imps |= imp.directImports
		return imps

	@property
	def allEntities(self):
		raise NotImplementedError

	@property
	def allClasses(self):
		raise NotImplementedError

	@property
	def allIndividuals(self):
		raise NotImplementedError

	@property
	def allDataProperties(self):
		raise NotImplementedError

	@property
	def allObjectProperties(self):
		raise NotImplementedError

	@property
	def allAnnotationProperties(self):
		raise NotImplementedError