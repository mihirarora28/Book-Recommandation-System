from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd

populartop50 = pickle.load(open('popular.pkl','rb'))
similarity_scores  = pickle.load(open('similarity.pkl','rb'))
finalTable = pickle.load(open('finaltable.pkl', 'rb'))
books = pickle.load(open('books.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def index():
    print(populartop50.shape)
    return render_template('index.html',
                           bookName = list(populartop50['Book-Title'].values),
                           peopleRated =list (populartop50['Number of People Rated'].values),
                           year = list(populartop50['Year-Of-Publication'].values),
                           imageUrl =list(populartop50['Image-URL-S'].values),
                           Author =list(populartop50['Book-Author'].values),
                           rating = list(populartop50['Book-Rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods = ['POST'])
def recommend():
    user_input = request.form.get('user_input');
    data = []
    index = np.where(finalTable.index == user_input)[0][0]
    distances = similarity_scores[index]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    for i in similar_items:
        items = []
        temp_df = (books[books['Book-Title'] == finalTable.index[i[0]]])
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        data.append(items)
    print(data);
    return render_template('recommend.html',data = data)


if __name__ == '__main__':
    app.run(debug = True)
