from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
import cv2

app = Flask(__name__)

# Load the trained model
model = load_model('trained_demo_v4(best).h5')

# Define function to predict cyclone intensity label
def predict_label(img_path):
    # Load and preprocess the image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))
    img = img / 255.0
    # Expand dimensions to create a batch
    img = np.expand_dims(img, axis=0)
    # Make predictions
    prediction = model.predict(img)[0][0]  # Get the predicted wind speed value
    print(f"Prediction: {prediction}")  # Print the prediction value

    if prediction < 18:
        intensity_label = "Low or no cyclone (< 18KT)"
    elif prediction < 29:
        intensity_label = "Cyclone Depression (18-28KT)"
    elif prediction < 35:
        intensity_label = "Deep Cyclone Depression (29-34KT)"
    elif prediction < 49:
        intensity_label = "Cyclonic Storm (35-48KT)"
    elif prediction < 65:
        intensity_label = "Cyclonic Severe Storm (49-64KT)"
    elif prediction < 90:
        intensity_label = "Very Cyclonic Severe Storm (65-89KT)"
    elif prediction < 121:
        intensity_label = "Extremely Cyclonic Severe Storm (90-120KT)"
    else:
        intensity_label = "Cyclonic Super Storm (>121KT)"

    return intensity_label, prediction

# Define route for the home page
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def upload():
    return render_template("predict.html")

@app.route('/explore',methods=['GET','POST'])
def info():
    return render_template("explore.html")

@app.route('/readmore',methods=['GET','POST'])
def modelinfo():
    return render_template("readmore.html")

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")



# Define route for the form submission
@app.route("/submit", methods=['POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']  # Access the uploaded file
        img_path = "static/uploads/" + img.filename  # Construct the file path

        # Save the uploaded file
        img.save(img_path)

        # Call the predict_label function with the file path
        intensity_label,prediction = predict_label(img_path)

    return render_template("predict.html", intensity_label=intensity_label,prediction=prediction, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
