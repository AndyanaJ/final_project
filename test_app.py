import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from run import app, Todo  # Import the Flask app instance directly from run.py

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Create a test Flask app
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        self.client = self.app.test_client()
        self.db = SQLAlchemy(self.app)
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def add_task(self, title):
        task = Todo(title=title, complete=False)
        self.db.session.add(task)
        self.db.session.commit()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Todo List", response.data)

    def test_add_task(self):
        response = self.client.post('/add', data=dict(title="Test Task"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Task", response.data)

    def test_update_task(self):
        self.add_task("Update Test Task")
        response = self.client.get('/update/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Update Test Task", response.data)
        self.assertIn(b"completed", response.data)

    def test_delete_task(self):
        self.add_task("Delete Test Task")
        response = self.client.get('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Delete Test Task", response.data)

if __name__ == '__main__':
    unittest.main()
