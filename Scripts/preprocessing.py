import nltk
import os
import re
import time
import string
import constants as const
import pandas as pd
import multiprocessing
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import es_core_news_md
from nltk.tokenize import word_tokenize
from multiprocessing import freeze_support

roots = SnowballStemmer('spanish')
spanish_stopwords = stopwords.words('spanish')
nlp = es_core_news_md.load()

def cleanup(column):
        column_cleaned = column.lower().strip()
        column_cleaned = re.sub('\\s+', ' ', column_cleaned)
        column_cleaned = ' '.join(set(column_cleaned.split(' ')))
        column_cleaned = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', column_cleaned)
        column_cleaned = re.sub(r'\d',' ', column_cleaned)
        return column_cleaned

def remove_stopwords(column):
    nostop_column = [i for i in column.split() if i not in spanish_stopwords]
    return ' '.join(nostop_column)

def stemming(column):
    words = [roots.stem(w) for w in word_tokenize(column)]
    stemmed_text = ' '.join(words)
    return stemmed_text

def lemmatize(column):
    column_tokens = nlp(column)
    lemmatized_tokens = [token.lemma_ for token in column_tokens]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

def preprocessingDataFrameColumn(df, column_name):
    new_column_name = f"{column_name}_processed"
    print(f"Eliminando duplicados, espacios, signos y numeros de la columna {column_name}...")
    df[new_column_name] = df[column_name].apply(lambda c: cleanup(c))
    print(f"Eliminando stopwors de la columna {column_name}...")
    df[new_column_name] = df[new_column_name].apply(lambda c: remove_stopwords(c))
    print(f"Realizando Stemming de la columna {column_name}...")
    df[new_column_name] = df[new_column_name].apply(lambda c: stemming(c))
    print(f"Realizando Lematizacion de la columna {column_name}...")
    df[new_column_name] = df[new_column_name].apply(lambda c: lemmatize(c))
    return df

if __name__ == '__main__':
     # Protege el código para evitar que se ejecute en los procesos secundarios
    freeze_support()
    nltk.download('stopwords')
    list_of_csv = os.listdir(const.PROCESSED_PATH)
    n_cores = multiprocessing.cpu_count()
    visions_column = "visions"
    proposals_column = "proposals"

    start_time = time.time()
    for csv in list_of_csv:
        data_frame = pd.read_csv(f"{const.PROCESSED_PATH}\\{csv}")
        print(f"Preprocesando archivo {csv} ...")
     
        if n_cores >= 2:
            with Pool(2) as pool:
                results = []
                results.append(pool.apply_async(preprocessingDataFrameColumn,args=(data_frame,visions_column)))
                results.append(pool.apply_async(preprocessingDataFrameColumn, args=(data_frame,proposals_column)))
            
                data_frame[f"{visions_column}_processed"] = results[0].get()[f"{visions_column}_processed"]
                data_frame[f"{proposals_column}_processed"] = results[1].get()[f"{proposals_column}_processed"]
            
            data_frame.to_csv(f"{const.PROCESSED_PATH}\\pln_{csv}", index = False)
        else:
            print("Se recomienda usar un dispositivo con mas de un nucleo de procesamiento")
            break
    end_time = time.time()
    print("Tiempo de proceso en visiones y propuestas de todos los archivos: ", end_time - start_time)
