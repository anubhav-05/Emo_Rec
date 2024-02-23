from flask import Flask, render_template, request, jsonify
import pickle
from keras.preprocessing import image
from PIL import Image
import numpy as np
from PIL import ImageOps

app = Flask(__name__, template_folder='templates')

with open('emotion_predictor.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def index():
    return render_template('index.html', emotion='')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Resize the image to the target size (56, 56)
    img = Image.open(file)
    img = img.resize((56, 56))
    img = ImageOps.grayscale(img)

    # Convert the image to a numpy array
    test_image = image.img_to_array(img)

    # Expand the dimensions to create a batch of size 1
    test_image = np.expand_dims(test_image, axis=0)

    # Normalize the pixel values to be in the range [0, 1]
    test_image /= 255.0

    # Make predictions
    result = model.predict(test_image)
    index = np.argmax(result)
    output = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprised']
    emotion = output[index]
    print(emotion)
    
    # Pass the result to the template for rendering
    if(emotion=='Angry'):
        return jsonify({'emotion1': emotion})
    elif(emotion=='Disgust'):
        return jsonify({'emotion2': emotion})
    elif(emotion=='Fear'):
        return jsonify({'emotion3': emotion})
    elif(emotion=='Happy'):
        return jsonify({'emotion4': emotion})
    elif(emotion=='Neutral'):
        return jsonify({'emotion5': emotion})
    elif(emotion=='Sad'):
        return jsonify({'emotion6': emotion})
    return jsonify({'emotion7': emotion})
if __name__ == '__main__':
    app.run(debug=True)
