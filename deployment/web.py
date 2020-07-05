import torch
import flask
import time
from flask import Flask
from flask import request
import torch.nn as nn
from preprocess import preprocess
from model import SentimentClassifier
from transformers import BertModel, BertTokenizer

app = Flask(__name__, static_folder='./public',
            static_url_path='/')


PRE_TRAINED_MODEL_NAME = 'bert-base-german-cased'
MODEL_PATH = "./model.bin"
DEVICE = "cpu"
MAX_LEN = 120
CLASS_NAMES = ['negative', 'neutral', 'positive']
# Set in main
TOKENIZER = None
MODEL = None


def encode(raw_tweet):
    inputs = TOKENIZER.encode_plus(
        raw_tweet,
        None,
        add_special_tokens=True,
        truncation=True,
        max_length=MAX_LEN,
        pad_to_max_length=True,
    )
    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]

    return {
        "tweet_text": raw_tweet,
        "ids": torch.tensor(ids, dtype=torch.long).unsqueeze(0),
        "mask": torch.tensor(mask, dtype=torch.long).unsqueeze(0),
        "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)
    }


def predict(tweet):
    tokenizer = TOKENIZER
    tweet = str(tweet)
    tweet = " ".join(tweet.split())
    tweet = preprocess(tweet)

    inputs = encode(tweet)

    ids = inputs["ids"]
    mask = inputs["mask"]
    token_type_ids = inputs["token_type_ids"]

    ids = ids.to(DEVICE, dtype=torch.long)
    token_type_ids = token_type_ids.to(DEVICE, dtype=torch.long)
    mask = mask.to(DEVICE, dtype=torch.long)

    outputs = MODEL(
        ids=ids, mask=mask, token_type_ids=token_type_ids)

    outputs = torch.sigmoid(outputs).cpu().detach().numpy()
    print(outputs)
    return outputs[0]


@app.route("/predict", methods=['POST'])
def web_predict():
    json = request.json
    raw_tweet = json.get('tweet')
    print(f'Predicting sentiment of "{raw_tweet}""')
    start_time = time.time()
    neg_pred, neut_pred, pos_pred = predict(raw_tweet)
    response = {}

    response["response"] = {
        'sentiment': {
            "positive": str(pos_pred),
            "neutral": str(neut_pred),
            "negative": str(neg_pred),
        },
        "tweet": str(raw_tweet),
        "time_taken": str(time.time() - start_time),
    }

    return flask.jsonify(response)


@ app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == "__main__":
    MODEL = SentimentClassifier(len(CLASS_NAMES))
    TOKENIZER = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    MODEL = nn.DataParallel(MODEL)
    MODEL.load_state_dict(torch.load(
        MODEL_PATH, map_location=torch.device(DEVICE)))
    MODEL.to(DEVICE)
    MODEL.eval()
    app.run(host='0.0.0.0')
