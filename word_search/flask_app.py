from flask import Flask, render_template, request, redirect
from trand_search import parsing, predict_yhat
from googlesearch import google_parsing



# js reference : https://apt-info.github.io/it%EC%9D%BC%EB%B0%98/line-chart/

app = Flask("searchWord")


@app.route("/")
def home():
    return render_template("searchView.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word
    else:
        return redirect('/')

    keyword = parsing(word)

    date, count = [], []

    for ymw in keyword['Date']:
        date.append(ymw)

    for search_count in keyword['search_count']:
        count.append(search_count)

    google_keyword = google_parsing(word)
    google_date, google_count = [], []

    for google_ymw in google_keyword['date']:
        google_date.append(google_ymw)

    for gsearch_count in google_keyword[word]:
        google_count.append(gsearch_count)
        
    naver_yhat = predict_yhat()
    
    y_date, y_count = [], []
    for yhat_date in naver_yhat['ds']:
        y_date.append(yhat_date)    
        
    for yhat_count in naver_yhat['yhat']:
        y_count.append(yhat_count)
        
    return render_template('graph.html', word=word, date=date, count=count, google_date=google_date, google_count=google_count, yhat_date=y_date, yhat_count=y_count)


if __name__ == '__main__':
   app.run()

#app.run(host="127.0.0.1")