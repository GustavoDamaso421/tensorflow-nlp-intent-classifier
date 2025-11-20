import pickle, sys, os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

base = r'c:\Users\expre\Desktop\estudos_tensorflow'
print('PWD exists?', os.path.exists(base))
files = ['cerebro_chatbot_v5.keras','tokenizer_v5.pickle','label_map_v5.pickle']
for f in files:
    p = os.path.join(base,f)
    print(f, '->', os.path.exists(p))

# Inspect pickles if present
try:
    with open(os.path.join(base,'label_map_v5.pickle'),'rb') as h:
        label_map = pickle.load(h)
    print('label_map type:', type(label_map))
    print('label_map sample items (first 10):')
    if isinstance(label_map, dict):
        for k,v in list(label_map.items())[:10]:
            print(' ',k, '->', v, type(v))
except Exception as e:
    print('Could not read label_map:', e)

try:
    with open(os.path.join(base,'tokenizer_v5.pickle'),'rb') as h:
        tokenizer = pickle.load(h)
    print('tokenizer type:', type(tokenizer))
    try:
        print('vocab size (len word_index):', len(tokenizer.word_index))
    except Exception as e:
        print('Could not inspect tokenizer.word_index:', e)
except Exception as e:
    print('Could not read tokenizer:', e)

# Try load model
try:
    model = tf.keras.models.load_model(os.path.join(base,'cerebro_chatbot_v5.keras'))
    print('Model loaded; summary (first lines):')
    try:
        model.summary()
    except Exception as e:
        print('Could not print model.summary():', e)
    # quick prediction if tokenizer exists
    try:
        frase = 'Olá, quero ver o cardápio'
        seq = tokenizer.texts_to_sequences([frase])
        padded = pad_sequences(seq, maxlen=11, padding='post')
        pred = model.predict(padded, verbose=0)
        print('prediction shape:', pred.shape)
        print('prediction vector (first row):', pred[0])
        print('argmax:', int(np.argmax(pred)))
    except Exception as e:
        print('Could not run prediction:', e)
except Exception as e:
    print('Could not load model:', e)

print('tensorflow version:', tf.__version__)
