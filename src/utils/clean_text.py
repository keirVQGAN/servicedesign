import re
import string

import nltk

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def clean_text(input_file, output_file, student):
    with open(input_file, 'r') as file:
        content = file.readlines()

    # This regex pattern should match most timecode formats
    timecode_pattern = r"\d+:\d+:\d+.\d+ --> \d+:\d+:\d+.\d+"

    cleaned_lines = [line for line in content if not re.match(timecode_pattern, line.strip())]

    cleaned_content = ' '.join(cleaned_lines)

    # Replace names
    cleaned_content = cleaned_content.replace('Keir Williams', 'Keir')
    cleaned_content = cleaned_content.replace(student, 'Student')

    # tokenize the text
    tokens = word_tokenize(cleaned_content)

    # remove punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in stripped if not word in stop_words]

    cleaned_text = ' '.join(words)

    with open(output_file, 'w') as file:
        file.write(cleaned_text)

    return cleaned_text
