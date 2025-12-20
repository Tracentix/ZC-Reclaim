import unittest
from src.app import create_app
from src.core import db

class ZCReclaimTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_auth_partitions(self):
        """Partition Testing: Valid vs Invalid inputs"""
        response = self.client.post('/auth/register', data=dict(
            username='testuser', email='test@zewailcity.edu.eg', password='123'
        ), follow_redirects=True)
        self.assertIn(b'Account created!', response.data)

        response = self.client.post('/auth/login', data=dict(
            email='', password=''
        ), follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    def test_admin_authorization(self):
        """Verification: Ensuring role-based access control works"""
        self.client.post('/auth/register', data=dict(
            username='student', email='s@zc.edu.eg', password='123'), follow_redirects=True)
        self.client.post('/auth/login', data=dict(
            email='s@zc.edu.eg', password='123'), follow_redirects=True)
        
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Access denied', response.data)