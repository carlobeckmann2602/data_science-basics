import re
import pandas as pd


def add_column_to_data_and_short_labels(data, columns, new_short_label, column_data, full_question):
    short_labels = columns.index.tolist()
    data[full_question] = column_data
    short_labels.append(new_short_label)
    short_labels_and_full_questions = dict(zip(short_labels, data.columns))
    columns = pd.Series(short_labels_and_full_questions)
    columns[new_short_label] = full_question

    return data, columns

def remove_column_from_data_and_short_labels(data, columns, column_to_drop_short_label):
    # columns_to_drop = [columns.lieblingsmusiker]
    # data = data.drop(columns_to_drop, axis=1)
    
    data = data.drop([columns[column_to_drop_short_label]], axis=1)

    short_labels = columns.index.tolist()
    short_labels.remove(column_to_drop_short_label)

    short_labels_and_full_questions = dict(zip(short_labels, data.columns))
    columns = pd.Series(short_labels_and_full_questions)

    return data, columns


def generate_full_question_from_short_label(short_label):
    # replace the letters in front of the first _ with the same string but capitalized and with space instead of _
    full_question = re.sub(r"^[a-zA-Z]+_", lambda match: match.group(0), short_label)

    full_question = full_question.replace("_", " ").title() + "? (encoded)"

    return full_question


def one_hot_encode_columns_and_update_short_labels(data, columns, columns_to_encode_short_labels: list):
    columns_to_encode = [columns[column_label] for column_label in columns_to_encode_short_labels]

    for column in columns_to_encode:
        data[column] = data[column].str.replace("/", "_").replace("_", "_").str.lower()

    data_encoded = pd.get_dummies(data, columns=columns_to_encode, prefix=columns_to_encode_short_labels)
    
    short_labels = columns.index.tolist()
    new_column_labels = [item for item in list(data_encoded.columns.values) if item.startswith(tuple(column for column in columns_to_encode_short_labels))]

    short_labels_encoded = short_labels + list(new_column_labels)

    for column in columns_to_encode_short_labels:
        short_labels_encoded.remove(column)

    print(short_labels_encoded)

    short_labels_and_full_questions_encoded = dict(zip(short_labels_encoded, data_encoded.columns))
    short_labels_and_full_questions_encoded = {key: generate_full_question_from_short_label(value) if key in new_column_labels else value for key, value in short_labels_and_full_questions_encoded.items()}
    columns_encoded = pd.Series(short_labels_and_full_questions_encoded)

    return data_encoded, columns_encoded


def insert_linebreaks(title):
    linebreak_limit = 50

    if len(title) < linebreak_limit:
        return title
    else:
        part_after_limit = title[linebreak_limit:]
        # replace first whitespace after limit with linebreak
        part_after_limit = re.sub(r"\s+", "\n", part_after_limit, 1)
        return title[:linebreak_limit] + part_after_limit


# remove_emojis from https://stackoverflow.com/a/58356570
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def remove_emojis_and_whitespace(data):
    return remove_emojis(data).strip()