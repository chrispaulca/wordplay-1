import sys

import nltk
import unidecode
from nltk.stem.porter import *
from sklearn.feature_extraction import stop_words
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import zipfile
import os
PARTIALS = False


def gettext_plain(text):
    """
    Assumes the input <text> is plain text and return it as string.
    """
    ret_str = text
    return ret_str


def gettext_xml(xmltext):
    """
    Parse xmltext and return the text from <title> and <text> tags
    """
    xmltext = xmltext.encode('ascii', 'ignore')  # ensure no weird char
    tree = ET.fromstring(xmltext)
    ret_str = ''
    for elem in tree.iterfind('title'):
        ret_str += elem.text
    ret_str += ' '  # insert a space in the middle for seperation.
    for text_node in tree.iterfind('.//text/*'):
        ret_str += text_node.text
        ret_str += ' '
    return ret_str


def words(text):
    """
    Given a string, return a list of words normalized as follows.
    Split the string to make words first by using regex compile() function
    and string.punctuation + '0-9\\r\\t\\n]' to replace all those
    char with a space character.
    Split on space to get word list.
    Ignore words < 3 char long.
    Lowercase all words
    """
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    # delete stuff but leave at least a space to avoid clumping together
    nopunct = regex.sub(" ", text)
    words = nopunct.split(" ")
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    # print words
    return words


def tokenize(text):
    """
    Tokenize text and return a non-unique list of tokenized words
    found in the text. Normalize to lowercase, strip punctuation,
    remove stop words, drop words of length < 3.
    """
    processed_text = words(text)
    goodwords = ''
    for w in processed_text:
        if w not in stop_words.ENGLISH_STOP_WORDS:
            goodwords += w
            goodwords += ' '
    tokenized_text = nltk.word_tokenize(goodwords)
    return tokenized_text


def stemwords(words):
    """
    Given a list of tokens/words, return a new list with each word
    stemmed using a PorterStemmer.
    """
    stem_list = []
    ps = PorterStemmer()
    for word in words:
        stem_list.append(ps.stem(word))
    return stem_list


def tokenizer(text):
    """
    The tokenizer.
    """
    return stemwords(tokenize(text))


def compute_tfidf(corpus):
    """
    Create and return a TfidfVectorizer object after training it on
    the list of articles pulled from the corpus dictionary. The
    corpus argument is a dictionary mapping file name to xml text.
    """
    tfidf = TfidfVectorizer(input='content',
                            analyzer='word',
                            preprocessor=gettext_plain,
                            tokenizer=tokenizer,
                            stop_words='english',
                            decode_error='ignore')
    # the key is: id
    # the value of corpus is: (name, artist, album, lyric)
    # corpus[key][3] is the lyric
    text_list = [corpus[key][3] for key in corpus]
    tfidf.fit(text_list)
    return tfidf


def summarize(tfidf, text, n=0):
    """
    Given a trained TfidfVectorizer object and some XML text, return
    up to n (word,score) pairs in a list.
    """
    text = unidecode.unidecode(text)
    sparse_matrix = tfidf.transform([text])
    word_index_array = sparse_matrix.nonzero()[1]
    aaa = sparse_matrix.nonzero()[0]
    word_array = tfidf.get_feature_names()
    tuple_list = []
    for i in range(len(word_index_array)):
        the_tuple = (word_array[word_index_array[i]],
                     sparse_matrix[aaa[i],
                     word_index_array[i]])
        if the_tuple[1] >= 0.09:
            tuple_list.append(the_tuple)

    tuple_list.sort(key=lambda tup: tup[1], reverse=True)

    # n == 0 means output everything, otherwise only output n tuples
    if n == 0:
        max_output_len = len(tuple_list)
    else:
        max_output_len = n if len(tuple_list) > n else len(tuple_list)
    return tuple_list[:max_output_len]


def load_corpus(zipfilename):
    """
    Given a zip file containing root directory reuters-vol1-disk1-subset
    and a bunch of *.xml files, read them from the zip file into
    a dictionary of (word,xmltext) associations. Use namelist() from
    ZipFile object to get list of xml files in that zip file.
    Convert filename reuters-vol1-disk1-subset/foo.xml to foo.xml
    as the keys in the dictionary. The values in the dictionary are the
    raw XML text from the various files.
    """
    ret_dict = {}
    full_path = os.path.expanduser(zipfilename)
    path_to_extract = full_path.split(os.path.basename(full_path))[0]
    zipref = zipfile.ZipFile(full_path, 'r')
    zipref.extractall(path_to_extract)
    files_in_package = zipref.namelist()
    for file in files_in_package:
        file_basename = os.path.basename(file)
        if file_basename == '':
            continue
        with open(path_to_extract + file, 'r') as xml_file:
            content = xml_file.read()
            ret_dict[file_basename] = content
    zipref.close()
    return ret_dict
