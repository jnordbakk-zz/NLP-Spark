
#######################
## Notes: need to import new model that was only run on "cleaned frame" that has relavant fileds

# In app
# Pull tweets, format, get coordinates
# turn into spark dataframe
# apply data_prep_pipeline  and then model ## QUESTION can we have columns that are not part of model? Lat/Lomg?
# return Lat, log and prediction
######################



#################################################
# # import necessary libraries
#################################################

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    url_for)
    
import os
import io
import numpy as np

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from flask import Flask, request, redirect, url_for, jsonify, render_template,make_response
from pyspark import SparkContext
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel



from pyspark.sql import SparkSession
from pyspark.sql.functions import length
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vector
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark import SparkContext
from pyspark import SparkFiles
from pyspark.sql.functions import length
from flask_cors import CORS
from json import dumps, loads

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('twitter').getOrCreate()



#################################################
# Flask Setup
#################################################
# app = Flask(__name__)

app = Flask(__name__, static_url_path='/static')
CORS(app)


###########################################################
# Load the model and create function to add features
###########################################################

new_predictor = NaiveBayesModel.load("../sentiment_model.h5")

def sparktransform(pandasdf):

    ## convert pandas to spark dataframe
    sparkdf = spark.createDataFrame(pandasdf)

    ## Add length column
    data = sparkdf.withColumn('length', length(sparkdf['Tweet']))

    # Create all the features to the data set
    pos_neg_to_num2 = StringIndexer(inputCol='Compound',outputCol='compound2')
    pos_neg_to_num3 = StringIndexer(inputCol='Positive',outputCol='positive2')
    pos_neg_to_num4 = StringIndexer(inputCol='Negative',outputCol='negative2')
    pos_neg_to_num5 = StringIndexer(inputCol='Neutral',outputCol='neutral2')

    tokenizer = Tokenizer(inputCol="Tweet", outputCol="token_text")
    stopremove = StopWordsRemover(inputCol='token_text',outputCol='stop_tokens')
    hashingTF = HashingTF(inputCol="stop_tokens", outputCol='hash_token')
    idf = IDF(inputCol='hash_token', outputCol='idf_token')


    # Create feature vectors
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml.linalg import Vector

    clean_up = VectorAssembler(inputCols=['idf_token', 'length','compound2','negative2','positive2','neutral2'], outputCol='features')

    # Create a and run a data processing Pipeline
    from pyspark.ml import Pipeline
    data_prep_pipeline = Pipeline(stages=[pos_neg_to_num2,pos_neg_to_num3,pos_neg_to_num4,pos_neg_to_num5,tokenizer, stopremove, hashingTF, idf, clean_up])

    # Fit and transform the pipeline
    cleaner = data_prep_pipeline.fit(data)
    cleaned = cleaner.transform(data)

    #apply model

    test_results = new_predictor.transform(cleaned)
#     test_results.select(["prediction"]).show(5)
    
    # convert to pandas DF
    pandasdf = test_results.toPandas()
#     pandasdf = pandasdf[["Tweet","coordinates","prediction"]]

    return pandasdf



@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == "POST":
        ## get html element and asign to variable
        searchterm = request.form["searchterm"]
    else:
        searchterm = request.args.get("searchterm", "apple")

    from get_tweets_func_script import get_tweet_frame
    pandasDF = get_tweet_frame(searchterm)
    pandasdf=sparktransform(pandasDF)
    jsondata =[]
    jsondata=loads(pandasdf.to_json(orient='records') )
    print(type(jsondata))
    
    return jsonify(jsondata)

@app.route("/submit", methods=["POST"])
def submit():
    searchterm = request.form["searchterm"]
    return redirect(url_for('viz', searchterm=searchterm))


@app.route("/viz", methods=["GET"])
def viz():
    searchterm = request.args.get("searchterm", "apple")
    return render_template('viz.html', search_term=searchterm)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)