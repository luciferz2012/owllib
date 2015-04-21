class OWLEntity:
    # getIRI
    def getAnnotationProperties(self, annotationProperty=None):
        raise NotImplementedError


class OWLClass(OWLEntity):
    def getIndividuals(self, ontologySet):
        raise NotImplementedError

    def getSubClasses(self, ontologySet):
        raise NotImplementedError

    def getSuperClasses(self, ontologySet):
        raise NotImplementedError


class OWLIndividual(OWLEntity):
    def getDataProperties(self, ontology, dataProperty=None):
        raise NotImplementedError

    def getObjectProperties(self, ontology, objectProperty=None):
        raise NotImplementedError


class OWLProperty(OWLEntity):
    def getDomains(self, ontologySet):
        raise NotImplementedError

    def getRanges(self, ontologySet):
        raise NotImplementedError

    def getSubProperties(self, ontologySet):
        raise NotImplementedError

    def getSuperProperties(self, ontologySet):
        raise NotImplementedError


class OWLDataProperty(OWLProperty):
    pass


class OWLObjectProperty(OWLProperty):
    def getInverses(self, ontologySet):
        raise NotImplementedError

    def isAsymmetric(self, ontolgySet):
        raise NotImplementedError

    def isInverseFunctional(self, ontologySet):
        raise NotImplementedError

    def isIrreflexive(self, ontologySet):
        raise NotImplementedError

    def isReflexive(self, ontologySet):
        raise NotImplementedError

    def isSymmetric(self, ontologySet):
        raise NotImplementedError

    def isTransitive(self, ontologySet):
        raise NotImplementedError


class OWLAnnotationProperty(OWLEntity):
    # isComment
    # isDeprecated
    # isLabel
    pass


class OWLOntology:
    # getIRI
    def getAnnotationProperties(self):
        raise NotImplementedError

    def getDirectImports(self):
        raise NotImplementedError

    def getImports(self):
        raise NotImplementedError

    def getOntologyManager(self):
        raise NotImplementedError

    def getAllEntities(self):
        raise NotImplementedError

    def getAllClasses(self):
        raise NotImplementedError

    def getAllIndividuals(self):
        raise NotImplementedError

    def getAllDataProperties(self):
        raise NotImplementedError

    def getAllObjectProperties(self):
        raise NotImplementedError

    def getAllAnnotationProperties(self):
        raise NotImplementedError


class OWLOntologyManager:
    def createOntology(self, IRI):
        raise NotImplementedError

    def getDirectImports(self, ontology):
        raise NotImplementedError

    def getImports(self, ontology):
        raise NotImplementedError

    def getOntology(self, IRI):
        raise NotImplementedError

    def loadOntology(self, IRI):
        raise NotImplementedError

    def removeOntology(self, ontology):
        raise NotImplementedError

    def saveOntology(self, ontology, IRI, ontologyFormat):
        raise NotImplementedError