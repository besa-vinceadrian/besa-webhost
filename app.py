# Library Management System uisng Flask

from flask import Flask, request, jsonify

app = Flask(__name__)

books = [
    {"id": 1, 
     "title": "1984", 
     "author": "George Orwell", 
     "year_published": 1949},
    {"id": 2, 
     "title": "To Kill a Mockingbird", 
     "author": "Harper Lee", 
     "year_published": 1960},
    {"id": 3, 
    "title": "The Great Gatsby", 
    "author": "F. Scott Fitzgerald", 
    "year_published": 1925}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/', methods=['POST'])
def add_book():
    new_book = request.get_json()

    if not new_book or not all(key in 
            new_book for key in ("title", "author", "year_published")):
        return jsonify({"Error: Invalid book data"}), 400
    
    new_book["id"] = len(books) + 1
    books.append(new_book)
    
    return jsonify({
        "message": "Book added successfully",
        "book": new_book
        }), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = next((b for b in books if b["id"] == id), None)
    if not book:
        return jsonify({"Error": "Book not found"}), 404

    updated_data = request.get_json()
    if not updated_data or not all(key in updated_data 
            for key in ("title", "author", "year_published")):
        return jsonify({"Error": "Invalid book data"}), 400

    book.update(updated_data)
    return jsonify({
        "message": "Book updated successfully",
        "book": book
        }), 200

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books

    book = next((b for b in books if b["id"] == id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted successfully", 
                        "book": book}), 200
    else:
        return jsonify({"error": "Book not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)