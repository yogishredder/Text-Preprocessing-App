import streamlit as st
import re
import pandas as pd
from io import StringIO
import chardet
import sqlite3
from sqlite3 import Connection
import src.function as fc
import src.util as utils
import src.database as db

DB_PATH = "data/processed/data_cleansing.db"
def get_connection(path: str):
    return sqlite3.connect(path, check_same_thread=False)

def init_db(conn: Connection):
    conn.execute("""CREATE TABLE IF NOT EXISTS result (RAW_DATA, CLEANED_DATA);""")
    conn.commit()

def get_data(conn: Connection):
    dfr = pd.read_sql("SELECT CLEANED_DATA as CLEANED_SQLITE3_DATA FROM result", con=conn)
    return dfr

def display_data(conn: Connection):
    st.dataframe(get_data(conn))

############################################################TEXT PREPROCESSING

st.write("# Page 2 : Text Preprocessing App from CSV File📚")

st.markdown("""The app will read a CSV file containing text data, preprocess the text by removing unwanted characters, punctuation, and stop words, and output the cleaned text in a new CSV file""")

uploaded_file = st.file_uploader("Upload CSV file to process:")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding = "ISO-8859-1")
    max_data = st.slider("Max data count:", 0, 100)
    df = df.iloc[:max_data]
    df = df.drop(df.columns[1:13], axis=1)      #REMOVE NOT USED COLUMN

    uploaded_kamusalay = st.file_uploader("Upload slangword or *kamus_alay* CSV file", key = 'kamusalay')  
    if uploaded_kamusalay is not None:
        df_uploaded_kamusalay = pd.read_csv(uploaded_kamusalay, encoding = "ISO-8859-1", sep=',')

    df['text_only'] = df['Tweet'].apply(lambda x:fc.remove_punct(x))   #df['text_only'] = df['Tweet'].str.replace(r'[^\w\s]|_', '', regex=True) #WORK
    df.info()
    #df['lowercase'] = df['text_only'].str.lower()
    df['casefolding'] = df['text_only'].apply(lambda x: fc.case_folding(x))
    #df['tokenizing'] = df['lowercase'].apply(lambda x: fc.tokenization(x.lower()))
    df['tokenizing'] = df['casefolding'].apply(lambda x: fc.tokenization(x))
    try: 
        df['normalization'] = df['tokenizing'].apply(lambda x: fc.normalisasi(x))    
    except:
        df['normalization'] = df['tokenizing']
    df['stemming'] = df['normalization'].apply(lambda x: fc.stemming(x))
    df['after_stopword'] = df['stemming'].apply(lambda x: fc.remove_stopwords(x))
    df['detokenizing']=df['after_stopword'].apply(lambda x: fc.TreebankWordDetokenizer().detokenize(x))
    df['Cleaned_data'] = df['detokenizing'].str.replace(r'\b\w\b', '').str.replace(r'\s+', ' ').str.replace('xf','')
    df
    if max_data > 0:
        st.markdown("""Here the result:""")    
        df[['Tweet','Cleaned_data']]
        df = df[['Tweet','Cleaned_data']]

#EXPORT TO CSV FILE
try:
    @st.cache_resource
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(df)
    if not df.empty:
        st.download_button("Export result to CSV",csv,"cleaned_data.csv","text/csv",key='browser-data')

        #SAVE DATA TO SQLITE3
        if st.button("Save to database"):    
            conn = get_connection(DB_PATH)
            init_db(conn)
            conn.execute('DELETE from result')
            for index,row in df.iterrows():
                conn.execute('INSERT INTO result values (?,?)', (row['Tweet'], row['Cleaned_data']))
                conn.commit()            
            display_data(conn)

            try:
                conn.close()
            except Exception:
                pass

except Exception:
    pass
