from flask  import Flask,render_template,url_for,request
import json
import Data_pre_processing as process #Data_pre_processing script
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import PassiveAggressiveClassifier
import pickle 



app = Flask(__name__)
model = pickle.load(open("PAC.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
tfidf_transformer = pickle.load(open("tfidf_transformer.pkl", "rb"))

@app.route('/')
#def home():
	#return render_template('test.html')

@app.route('/predict',methods=['POST'])
def predict():
  text = request.args.get(' رن بقي و حيات امك ')
  text = process.clean([text])
  text_counts = vectorizer.fit_transform(text)
  text_transfrom = tfidf_transformer.fit_transform(text_counts)
  pred = model.predict(text_transfrom)
  return ( pred)

if __name__ == '__main__':
    app.run(debug=True)

