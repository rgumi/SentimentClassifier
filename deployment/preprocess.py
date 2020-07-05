import re


def replace_multi_ex_marks(txt):
    return re.sub(pattern=r'!{2,}', repl=' multiExclamation', string=txt)


def replace_multi_q_marks(txt):
    return re.sub(pattern=r'\?{2,}', repl=' multiQuestion', string=txt)


def replace_multi_dots(txt):
    return re.sub(pattern=r'\.{2,}', repl='', string=txt)


def remove_multi_marks(txt):
    return re.sub(pattern=r'[\.!\?]{2,}', repl='', string=txt)


def remove_at_user(txt):
    return re.sub(pattern=r'@', repl='', string=txt)


def remove_hashtags(txt):
    return re.sub(pattern=r'#', repl='', string=txt)


def replace_pos_emojis(txt):
    return re.sub(pattern=r':\)|;\)|:-\)|;-\)', repl=' posEmoji ', string=txt)


def replace_neg_emojis(txt):
    return re.sub(pattern=r':\(|;\(|:-\(|;-\(|:-/|:/', repl=' negEmoji ', string=txt)


def remove_pos_emojis(txt):
    return re.sub(pattern=r':\)|;\)|:-\)|;-\)', repl='', string=txt)


def remove_neg_emojis(txt):
    return re.sub(pattern=r':\(|;\(|:-\(|;-\(|:-/|:/', repl='', string=txt)

# https://www.kaggle.com/sudalairajkumar/getting-started-with-text-preprocessing#Removal-of-Emojis


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def preprocess(txt):
    functions = [remove_multi_marks, remove_at_user, remove_hashtags]

    for func in functions:
        txt = func(txt)
    return txt
