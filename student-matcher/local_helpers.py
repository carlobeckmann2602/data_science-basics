import re
import pandas as pd


def add_column_to_data_and_short_labels(df, all_columns, new_short_label, column_df, full_question):
    short_labels = all_columns.index.tolist()

    # add the new column to the dataframe
    df[full_question] = column_df

    # add the new column to the short labels
    short_labels.append(new_short_label)
    short_labels_and_full_questions = dict(zip(short_labels, df.columns))
    all_columns = pd.Series(short_labels_and_full_questions)

    # update the value of the new column to be the full question
    all_columns[new_short_label] = full_question

    return df, all_columns


def remove_column_from_data_and_short_labels(df, all_columns, column_to_drop_short_label):
    # remove the column from the dataframe
    df = df.drop([all_columns[column_to_drop_short_label]], axis=1)

    # remove the column from the short labels
    short_labels = all_columns.index.tolist()
    short_labels.remove(column_to_drop_short_label)
    short_labels_and_full_questions = dict(zip(short_labels, df.columns))
    all_columns = pd.Series(short_labels_and_full_questions)

    return df, all_columns


def generate_full_question_from_short_label(short_label):
    # replace the letters in front of the first _ with the same string but capitalized and with space instead of _ and add (encoded)
    full_question = re.sub(r"^[a-zA-Z]+_", lambda match: match.group(0), short_label)
    full_question = full_question.replace("_", " ").title() + "? (encoded)"

    return full_question


def one_hot_encode_columns_and_update_short_labels(df, columns, columns_to_encode_short_labels: list):
    # get the full column labels (full questions) of the columns to encode
    columns_to_encode = [columns[column_label] for column_label in columns_to_encode_short_labels]

    # strip, lowercase, replace / with _, replace whitespace with _
    for column in columns_to_encode:
        df[column] = df[column].str.strip().str.lower().replace("/", "_", regex=True).replace("\s", "_", regex=True)

    # one-hot encode the columns
    df_encoded = pd.get_dummies(df, columns=columns_to_encode, prefix=columns_to_encode_short_labels)
    
    # find the newly added column labels
    short_labels = columns.index.tolist()
    new_column_labels = [item for item in list(df_encoded.columns.values) if item.startswith(tuple(column for column in columns_to_encode_short_labels))]

    # add the new column labels to the short labels
    short_labels_encoded = short_labels + list(new_column_labels)

    # remove the columns that were encoded from the short labels
    for column in columns_to_encode_short_labels:
        short_labels_encoded.remove(column)

    # update column labels and generate full questions for the new columns
    short_labels_and_full_questions_encoded = dict(zip(short_labels_encoded, df_encoded.columns))
    short_labels_and_full_questions_encoded = {key: generate_full_question_from_short_label(value) if key in new_column_labels else value for key, value in short_labels_and_full_questions_encoded.items()}
    columns_encoded = pd.Series(short_labels_and_full_questions_encoded)

    # rename columns in dataframe to full questions
    df_encoded.rename(short_labels_and_full_questions_encoded, inplace=True, axis=1)

    return df_encoded, columns_encoded


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