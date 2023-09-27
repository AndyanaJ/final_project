import unittest
from run import app, db, Todo

class FlaskAppTestCase(unittest.TestCase):
    
    # Set up the test environment
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        self.app = app.test_client()
        db.create_all()

    # Tear down the test environment
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper function to add a test task
    def add_task(self, title):
        task = Todo(title=title, complete=False)
        db.session.add(task)
        db.session.commit()

    # Test the home page
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Todo List", response.data)

    # Test adding a task
    def test_add_task(self):
        response = self.app.post('/add', data=dict(title="Test Task"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Task", response.data)

    # Test updating a task
    def test_update_task(self):
        self.add_task("Update Test Task")
        response = self.app.get('/update/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Update Test Task", response.data)
        self.assertIn(b"completed", response.data)

    # Test deleting a task
    def test_delete_task(self):
        self.add_task("Delete Test Task")
        response = self.app.get('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Delete Test Task", response.data)

if __name__ == '__main__':
    unittest.main()
