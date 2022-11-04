import numpy as np
import pickle
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# load data and extract all the vectors
with open('clean_full_cosine.pkl', 'rb') as f:
    data = pickle.load(f)
list_books = sorted([book['title'] for book in data])
title_list = [item['title'] for item in data]


@app.route("/", methods=['GET', 'POST'])
def template_test():
    if request.method == 'POST':
        selected_title = request.form.get('selected_title')
        selected_book = next(item for item in data if item['title'] == selected_title)
        similar_books = [data[i] for i in selected_book['cosine']]
        return render_template('index.html',
                               list_books=list_books,
                               book_selected=selected_book,
                               similar_books=similar_books[:6])
    else:
        return render_template('index.html', list_books=list_books)


@app.route("/recommendations", methods=['GET'])
def get_recommendations():
    title = request.args.get('title', default=None, type=str)
    num_reco = request.args.get("number", default=5, type=int)
    distance = request.args.get("distance", default="cosine", type=str)
    field = request.args.get("field", default="Title", type=str)
    if not title:
        return jsonify("Missing Title for the book"), 400
    elif distance not in ["cosine", "euclidean"]:
        return jsonify("Distance can only be cosine or euclidean"), 400
    elif num_reco not in range(1, 21):
        return jsonify("Can only request between 1 and 20 books"), 400
    elif title not in title_list:
        return jsonify("Title not in supported books"), 400
    elif field not in data[0].keys():
        return jsonify("Field not available in the data"), 400
    else:
        try:
            selected_book = next(item for item in data if item['Title'] == title)
            similar_books = [data[i][field] for i in selected_book[distance]]
            return jsonify(similar_books[:num_reco]), 200
        except Exception as e:
            return jsonify(str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)