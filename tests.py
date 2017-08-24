from unittest import TestCase
from model import connect_to_db, db, example_data
from server import app
from flask import session
from seed import seed_example_data


class FlaskTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        seed_example_data()


    def tear_down():
        db.drop_all()


    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn("SF Civic Art", result.data)
        self.assertIn("Search by Artist Name:", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()