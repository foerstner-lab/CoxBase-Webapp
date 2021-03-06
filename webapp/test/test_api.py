import os

import unittest

from pyramid import testing


class APIFunctionalTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app

        from webtest import TestApp
        app = get_app("{}/development.ini".format(os.environ["TRAVIS_BUILD_DIR"]))

        self.testapp = TestApp(app)

    def test_year_response(self):
        res = self.testapp.get("/api_country/DE", status=200)
        self.assertEqual(res.content_type, "application/json")
        self.assertIn("2005", res.json)

    def test_host_response(self):
        res = self.testapp.get("/api_host/DE", status=200)
        self.assertEqual(res.content_type, "application/json")
        self.assertIn("cattle", res.json)

    def test_province_response(self):
        res = self.testapp.get("/api_province/DE", status=200)
        self.assertEqual(res.content_type, "application/json")
        self.assertIn("NW", res.json)

    def test_genotype_response(self):
        res = self.testapp.get("/api_genotype/DE", status=200)
        self.assertEqual(res.content_type, "application/json")
        self.assertIn("A2", res.json)
    
    def test_mlva_coords_response(self):
        res = self.testapp.get("/api_mlva_map/D8", status=200)
        self.assertEqual(res.content_type, "application/json")
    
    def test_mst_coords_response(self):
        res = self.testapp.get("/api_mst_map/1", status=200)
        self.assertEqual(res.content_type, "application/json")
    
    def test_country_api_response(self):
        res = self.testapp.get("/coxviewer_api/DE", status=200)
        self.assertEqual(res.content_type, "application/json")
