from corpus_loader import load_all_languages
from paradox.evaluation.training_test_split import split_training_data
from paradox.utils.vocabulary_extractor import get_vocabulary
from paradox.utils.one_hot_encoder import get_one_hot_encoding
from keras.utils.np_utils import to_categorical
from enum import Enum
import numpy as np


def load_keras_data_set(language, number_of_classes, data_set_type, concat_vectors, ngram_range=(1, 1)):
    task = 'Task1'
    if number_of_classes == 3:
        task = 'Task2'
    data_sets = load_all_languages()
    test_train_split = split_training_data(data_sets[language][task][0], data_sets[language][task][1])
    analyzer = ''
    if data_set_type == DataSetType.one_hot_encoding_character or data_set_type == DataSetType.one_hot_encoding_word:
        analyzer = 'char_wb'
        if data_set_type == DataSetType.one_hot_encoding_word:
            analyzer = 'word'
        vocabulary = get_vocabulary(test_train_split['X_train'], analyzer=analyzer, ngram_range=ngram_range)
        X_train = get_one_hot_encoding(test_train_split['X_train'], vocabulary=vocabulary, analyzer=analyzer,
                                       concat_vectors=concat_vectors)
        X_test = get_one_hot_encoding(test_train_split['X_test'], vocabulary=vocabulary, analyzer=analyzer,
                                      concat_vectors=concat_vectors)
    elif data_set_type == DataSetType.sequence_character:
        raise NotImplementedError
    elif data_set_type == DataSetType.sequence_word:
        raise NotImplementedError
    return {'X_train': X_train,
            'X_test': X_test,
            'y_train': to_categorical(np.array(test_train_split['y_train']), number_of_classes),
            'y_test_categorical': to_categorical(np.array(test_train_split['y_test']), number_of_classes),
            'y_test': test_train_split['y_test'],
            'vocabulary': vocabulary}


class DataSetType(Enum):
    one_hot_encoding_word = 1
    one_hot_encoding_character = 2
    sequence_character = 3
    sequence_word = 4
