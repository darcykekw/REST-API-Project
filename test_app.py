import unittest
import json
from app import app
import base64

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.token = self.get_token()

    def get_token(self):
        # Login to get token
        # admin:password123
        creds = base64.b64encode(b'admin:password123').decode('utf-8')
        response = self.app.post('/login', headers={
            'Authorization': f'Basic {creds}'
        })
        if response.status_code != 200:
            raise Exception("Login failed: " + str(response.data))
        data = json.loads(response.data)
        return data['token']

    def test_get_books(self):
        response = self.app.get('/books?token=' + self.token)
        self.assertEqual(response.status_code, 200)

    def create_book_helper(self):
        book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'isbn': '1234567890'
        }
        response = self.app.post('/books?token=' + self.token, 
                                 data=json.dumps(book),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        return data['id']

    def test_create_book(self):
        self.create_book_helper()

    def test_update_book(self):
        # First create a book
        book_id = self.create_book_helper()
        
        update_data = {
            'title': 'Updated Title'
        }
        response = self.app.put(f'/books/{book_id}?token=' + self.token,
                                data=json.dumps(update_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        # First create a book
        book_id = self.create_book_helper()
        
        response = self.app.delete(f'/books/{book_id}?token=' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_xml_format(self):
        response = self.app.get('/books?token=' + self.token + '&format=xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<?xml', response.data)

    def test_search(self):
        response = self.app.get('/books?token=' + self.token + '&q=Gatsby')
        self.assertEqual(response.status_code, 200)
        # Assuming Gatsby is in the db from init_db
        self.assertIn(b'Gatsby', response.data)

if __name__ == '__main__':
    unittest.main()
