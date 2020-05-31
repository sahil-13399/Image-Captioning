import numpy as np
from pickle import load
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


wordtoix = load(open("./static/wordtoix.pkl", 'rb'))
ixtoword = load(open("./static/ixtoword.pkl", 'rb'))

max_length = 34


def preprocess(image_path):
    # Convert all the images to size 299x299 as expected by the inception v3 model
    img = image.load_img(image_path, target_size=(299, 299))
    # Convert PIL image to numpy array of 3-dimensions
    x = image.img_to_array(img)
    # Add one more dimension
    x = np.expand_dims(x, axis=0)
    # preprocess the images using preprocess_input() from inception module
    x = preprocess_input(x)
    return x


# Function to encode a given image into a vector of size (2048, )
def encode(image):
    image = preprocess(image) # preprocess the image
    inception = load_model('./static/c_inception.h5')
    inception._make_predict_function()
    fea_vec = inception.predict(image) # Get the encoding vector for the image
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1]) # reshape from (1, 2048) to (2048, )
    return fea_vec


def greedy(photo):
    model = load_model('./static/c_model.h5')

    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final


def ret_cap(img_path):
    feats = encode(img_path).reshape((1, 2048))
    return "Caption: " + greedy(feats)

