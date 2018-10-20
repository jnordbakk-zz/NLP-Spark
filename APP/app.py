import os
import io
import numpy as np

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from flask import Flask, request, redirect, url_for, jsonify, render_template
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

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('twitter').getOrCreate()

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'Uploads'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# model = None
# graph = None


#######################
## Notes: need to import new model that was only run on "cleaned frame" that has relavant fileds

# In app
# Pull tweets, format, get coordinates
# turn into spark dataframe
# apply data_prep_pipeline  and then model ## QUESTION can we have columns that are not part of model? Lat/Lomg?
# return Lat, log and prediction
######################



# Load the model
new_predictor = NaiveBayesModel.load("../sentiment_model.h5")


testdata= spark.createDataFrame([    
    ("Happy Monday twitter", 0.778,0.564,0.09,0.346)
], ["tweet", "Compound","Negative","Neutral","Positive"])

data = testdata.withColumn('length', length(testdata['tweet']))

# Create all the features to the data set
pos_neg_to_num2 = StringIndexer(inputCol='Compound',outputCol='compound2')
pos_neg_to_num3 = StringIndexer(inputCol='Positive',outputCol='positive2')
pos_neg_to_num4 = StringIndexer(inputCol='Negative',outputCol='negative2')
pos_neg_to_num5 = StringIndexer(inputCol='Neutral',outputCol='neutral2')

tokenizer = Tokenizer(inputCol="tweet", outputCol="token_text")
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
test_results.select(["prediction"]).show(5)


# def gettweets():
#     # do stuff
    
#     return tweets



# @app.route("/send", methods=['GET', 'POST'])
# def send():
#     if request.method == "POST":
#         searchterm = request.form["searchterm"]
       
#         gettweets(searchterm)

    

#         return render_template('results.html',data=data)

#     return render_template('index.html')


# if __name__ == "__main__":
#     app.run(debug=True)
