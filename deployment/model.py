from transformers import BertModel
from torch import nn

PRE_TRAINED_MODEL_NAME = 'bert-base-german-cased'
# is ignored anyways for predictions
DROPOUT = 0.3


class SentimentClassifier(nn.Module):

    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=DROPOUT)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, ids, mask, token_type_ids):
        _, pooled_output = self.bert(
            input_ids=ids,
            attention_mask=mask,
            token_type_ids=token_type_ids
        )
        output = self.drop(pooled_output)
        return self.out(output)
