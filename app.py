from flask import Flask, jsonify, request, make_response, Response, render_template
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps
import dicttoxml

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '1a7d73a7910165856920d30aa36d5715'

mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') # Or header
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

def format_response(data, status_code=200):
    fmt = request.args.get('format')
    if fmt == 'xml':
        xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        return Response(xml, status=status_code, mimetype='application/xml')
    else:
        return make_response(jsonify(data), status_code)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (auth.username,))
    user = cur.fetchone()
    cur.close()

    if user and user['password'] == auth.password: # In real app, check hash
        token = jwt.encode({'user': user['username'], 'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# CRUD for Books

@app.route('/books', methods=['GET'])
@token_required
def get_books():
    cur = mysql.connection.cursor()
    search_query = request.args.get('q')
    if search_query:
        cur.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", ("%" + search_query + "%", "%" + search_query + "%"))
    else:
        cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return format_response(books)

@app.route('/books/<int:id>', methods=['GET'])
@token_required
def get_book(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    if not book:
        return format_response({'message': 'Book not found'}, 404)
    return format_response(book)

@app.route('/books', methods=['POST'])
@token_required
def add_book():
    data = request.get_json()
    if not data or not 'title' in data or not 'author' in data:
        return format_response({'message': 'Missing data'}, 400)
    
    title = data['title']
    author = data['author']
    published_year = data.get('published_year')
    isbn = data.get('isbn')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO books (title, author, published_year, isbn) VALUES (%s, %s, %s, %s)", (title, author, published_year, isbn))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    
    return format_response({'message': 'Book added', 'id': new_id}, 201)

@app.route('/books/<int:id>', methods=['PUT'])
@token_required
def update_book(id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cur.fetchone()
    
    if not book:
        cur.close()
        return format_response({'message': 'Book not found'}, 404)

    title = data.get('title', book['title'])
    author = data.get('author', book['author'])
    published_year = data.get('published_year', book['published_year'])
    isbn = data.get('isbn', book['isbn'])

    cur.execute("UPDATE books SET title=%s, author=%s, published_year=%s, isbn=%s WHERE id=%s", (title, author, published_year, isbn, id))
    mysql.connection.commit()
    cur.close()

    return format_response({'message': 'Book updated'})

@app.route('/books/<int:id>', methods=['DELETE'])
@token_required
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    
    if rows_affected == 0:
        return format_response({'message': 'Book not found'}, 404)
        
    return format_response({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
