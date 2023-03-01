import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle


nltk.download('punkt')
stemmer = LancasterStemmer()

with open("intents.json") as f:
    data = json.load(f)

try:
    with open("data.pickle",  "rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_y = []
    docs_x = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            word = nltk.word_tokenize(pattern)
            words.extend(word)
            docs_x.append(word)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle",  "wb") as f:
       pickle.dump((words, labels, training, output), f)

net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = "softmax")
net  = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch = 1000, batch_size = 8, show_metric = True)
    model.save("model.tflearn")

def bag_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for i in s_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1

    return np.array(bag)

def chat():
    print("Start talking with the bot!")
    print("Type quit to stop!")

    while True:
        inp = input("You: ")

        if inp.lower() == "quit":
            break
        
        results = model.predict([bag_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.8:

            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg['responses']

            print(random.choice(responses))
        
        else:
            print("I don't understand. Please try again.")

chat()




