import spacy
import warnings
from sys import platform
import pytest

from quickumls import spacy_component

class TestQuickUMLSComponent:
    @staticmethod
    def can_test_quickumls():
        if platform.startswith("win"):
            try:
                import quickumls_simstring
            except:
                # we're done here for now...
                return False

        return True

    def test_simple_pipeline(self):
        # let's make sure that this pipe has been initialized
        # At least for MacOS and Linux which are currently supported...

        if not TestQuickUMLSComponent.can_test_quickumls():
            return

        # allow default QuickUMLS (very small sample data) to be loaded
        nlp = spacy.blank("en")

        nlp.add_pipe("medspacy_quickumls")

        assert nlp

        quickumls = nlp.get_pipe("medspacy_quickumls")

        assert quickumls
        # this is a member of the QuickUMLS algorithm inside the component
        assert quickumls.quickumls
        # Check that the simstring database exists
        assert quickumls.quickumls.ss_db

    def test_quickumls_extractions(self):
        """
        Test that extractions can be performed using the very small (<100 concept) UMLS sample resources
        """

        # let's make sure that this pipe has been initialized
        # At least for MacOS and Linux which are currently supported...
        if not TestQuickUMLSComponent.can_test_quickumls():
            return

        # allow default QuickUMLS (very small sample data) to be loaded
        nlp = spacy.blank("en")

        nlp.add_pipe("medspacy_quickumls")

        # TODO -- Consider moving this and other extraction tests to separate tests from loading
        doc = nlp("Decreased dipalmitoyllecithin content found in lung specimens")

        assert len(doc.ents) == 1

        entity_spans = [ent.text for ent in doc.ents]

        assert "dipalmitoyllecithin" in entity_spans
