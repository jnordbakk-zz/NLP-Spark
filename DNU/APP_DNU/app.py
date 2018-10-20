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
from pyspark.ml.classification import NaiveBayes

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'Uploads'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

model = None
graph = None


# Load the model

model = NaiveBayes.load("sentiment_model.h5")
# graph = K.get_session().graph


load_model()

def gettweets():




@app.route('/', methods=['GET', 'POST'])
def get tweet():
    data = {"success": False}
    if request.method == 'POST':

       searchterm = request.form["searchterm"]
       
       gettweets(searchterm)

    
        # global graph
        #  with graph.as_default():
        #     preds = model.predict(file)
        #     results = decode_predictions(preds)
        #         # print the results
        #     print(results)

        #     data["predictions"] = []

        #         # # loop over the results and add them to the list of
        #         # # returned predictions
        #         # for (imagenetID, label, prob) in results[0]:
        #         #     r = {"label": label, "probability": float(prob)}
        #         #     data["predictions"].append(r)

        #         # indicate that the request was a success
        #     data["success"] = True

        # return jsonify(data)
        return render_template('results.html',data=data)
        
        # return render_template('results.html',data= jsonify(data))

    return render_template('index.html')
 


if __name__ == "__main__":
    app.run(debug=True)
