"""
Automatic tests of the DOI checker.

They do not connect to the internet: instead of asking Crossref, they use prepared answers
that imitate Crossref's. So the tests work on any computer and always the same way.
To try it against the real Crossref, see ejemplos/comprobar-doi/LEEME.md.
"""

import unittest

from tools.sources.crossref import (
    CONFIRMED, MISMATCHED, NOT_FOUND, check_work, compare_with_crossref,
)

WORK = {
    "id": "searle1980",
    "title": "Minds, brains, and programs",
    "author": [{"family": "Searle", "given": "John R."}],
    "issued": {"date-parts": [[1980]]},
    "DOI": "10.1017/S0140525X00005756",
}

CROSSREF_ANSWER = {
    "title": ["Minds, brains, and programs"],
    "author": [{"family": "Searle", "given": "John R."}],
    "issued": {"date-parts": [[1980, 9]]},
}


def crossref_answering(answer):
    """Imitate Crossref by always returning the same answer."""
    return lambda doi, email: answer


class DoiCheckerTests(unittest.TestCase):

    def test_confirms_a_work_whose_data_match(self):
        result = check_work(WORK, "prueba@ejemplo.org", crossref_answering(CROSSREF_ANSWER))
        self.assertEqual(result.outcome, CONFIRMED)

    def test_detects_a_doi_that_does_not_exist(self):
        result = check_work(WORK, "prueba@ejemplo.org", crossref_answering(None))
        self.assertEqual(result.outcome, NOT_FOUND)

    def test_detects_a_wrong_year(self):
        work = dict(WORK, issued={"date-parts": [[1981]]})
        result = check_work(work, "prueba@ejemplo.org", crossref_answering(CROSSREF_ANSWER))
        self.assertEqual(result.outcome, MISMATCHED)
        self.assertIn("Año distinto", result.mismatches[0])

    def test_detects_a_real_doi_of_another_work(self):
        other = {"title": ["Deep learning"], "author": [{"family": "LeCun"}], "issued": {"date-parts": [[2015]]}}
        differences = compare_with_crossref(WORK, other)
        self.assertEqual(len(differences), 3)  # title, year and author

    def test_is_not_fooled_by_accents_or_capitals(self):
        work = dict(WORK, title="MINDS, BRAINS AND PROGRAMS", author=[{"family": "Séarle"}])
        self.assertEqual(compare_with_crossref(work, CROSSREF_ANSWER), [])


if __name__ == "__main__":
    unittest.main()
