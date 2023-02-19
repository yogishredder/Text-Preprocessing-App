import streamlit as st
import re
import pandas as pd
from io import StringIO
import chardet
import sqlite3
from sqlite3 import Connection
import src.function as fc
import src.util as utils

st.write("# Page 1: Text Preprocessing App from Text area📜")

st.markdown(
    """
    The app will take input text from the user, clean it by removing unwanted characters, punctuation, and stop words, and output the clean text.

    *Example:*   """)

st.code('USER USER AKU ITU AKU\n\nKU TAU MATAMU SIPIT TAPI DILIAT DARI MANA ITU AKU', language='python')


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

df_ori = st.text_area('*Input some text to analyze:*', '''    ''')
df = df_ori

uploaded_kamusalay = st.file_uploader("Upload slangword or *kamus_alay* CSV file", key = 'kamusalay')   #
if uploaded_kamusalay is not None:
    df_uploaded_kamusalay = pd.read_csv(uploaded_kamusalay, encoding = "ISO-8859-1", sep=',')

df = fc.remove_punct(df)   
df = fc.case_folding(df)
df = fc.tokenization(df)
try:
    df = fc.normalisasi(df)
except Exception:
    pass
df = fc.stemming(df)
df = fc.remove_stopwords(df)
df = fc.TreebankWordDetokenizer().detokenize(df)
df = df.replace(r'\b\w\b', '').replace(r'\s+', ' ').replace('xf','')
st.write('*Here the result:* **:red[', df,']**')

data = {'ori':  [df_ori], 'clean': [df] }
df_csv = pd.DataFrame(data)
df_sql = df

#EXPORT TO CSV FILE
@st.cache_resource
def convert_df(df_csv):
    return df_csv.to_csv().encode('utf-8')
csv = convert_df(df_csv)     
if df != '':
    st.download_button("Export result to CSV",csv,"cleaned_data.csv","text/csv",key='browser-data')

    #SAVE DATA TO SQLITE3
    if st.button("Save to database"):    
        conn = get_connection(DB_PATH)
        init_db(conn)
        conn.execute(f"INSERT INTO result VALUES (?, ?)", (df_ori, df_sql))
        conn.commit()
        display_data(conn)































