# coding=utf-8
from rdflib import Graph
from rdflib.term import BNode
from rdflib import RDF, OWL
from rdflib.util import guess_format


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
	def __init__(self, IRI=None, versionIRI=None):
		super(OWLOntology, self).__init__(IRI)
		self.graph = Graph()
		self.graph.add((self._IRI, RDF.type, OWL.Ontology))
		if versionIRI:
			self.graph.add((IRI, OWL.versionIRI, versionIRI))
		self._directImports = None

	def load(self, file=None, location=None, data=None, owlFormat=None):
		if location and not owlFormat:
			owlFormat = guess_format(location)
		self.graph.parse(format=owlFormat, file=file, location=location, data=data)
		maxNumOfTriples = 0
		for IRI in self.graph.subjects(RDF.type, OWL.Ontology):
			triples = [(p, o) for (p, o) in self.graph.predicate_objects(IRI)]
			if maxNumOfTriples < len(triples):
				maxNumOfTriples = len(triples)
				self._IRI = IRI

	def save(self):
		raise NotImplementedError

	@property
	def directImports(self):
		if not self._directImports:
			self._directImports = set()
			for IRI in self.graph.objects(self.IRI, OWL.imports):
				ont = OWLOntology()
				ont.load(location=IRI)
				self._directImports.add(ont)
		return self._directImports

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