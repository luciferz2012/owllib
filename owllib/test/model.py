# coding=utf-8
from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, OWL


class OWLEntity:
	# get IRI
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


class OWLOntology:
	# get IRI
	def __init__(self, IRI=None, versionIRI=None):
		self.graph = Graph()
		if IRI:
			self._IRI = IRI
		else:
			self._IRI = BNode()
		self.graph.add((self._IRI, RDF.type, OWL.Ontology))
		if versionIRI:
			self.graph.add((IRI, OWL.versionIRI, versionIRI))

	def load(self, owlFormat, file=None, location=None, data=None):
		self.graph.parse(format=owlFormat, file=file, location=location, data=data)

	def save(self):
		raise NotImplementedError

	@property
	def annotationProperties(self):
		raise NotImplementedError

	@property
	def directImports(self):
		raise NotImplementedError

	@property
	def imports(self):
		raise NotImplementedError

	@property
	def ontologyManager(self):
		raise NotImplementedError

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