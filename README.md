# Text-Preprocessing-App

Text Preprocessing App is an app which transforms raw text data into a more structured format that is easier to analyze, model, and understand. Text data often contains noise, irrelevant information, or inconsistencies that can make it difficult to analyze using machine learning algorithms or other natural language processing (NLP) techniques.

Text preprocessing involves a variety of techniques, including:

    1. Removing unnecesary characters: cleaning up text data by removing unnecessary characters and patterns that might interfere with the analysis of the data

    2. Casefolding: returns a lowercase version of a string

    3. Tokenization: the process of splitting text data into smaller chunks, called tokens, such as words, phrases, or sentences

    4. Normalisation: normalize text by replacing slang words with their corresponding standard words and converting all words to lowercase

    5. Stemming: the process of reducing each word to its base or root form, which can help to simplify the text and make it easier to analyze

    6. Remove stopwords: removes stop words from a list of words representing the text of a tweet. Stop words are words that are commonly occurring and are typically not useful for text analysis, such as "the", "is", "are", "a", "an", etc.

    7. Detokenizing: reverse the tokenization process by joining a list of words back together into a single text string representing the text of a tweet
    


## Deployment

To deploy this project, 
1. Create virtual environment 

```bash
  python3 -m venv
```

2. Activate the virtual environment

```bash
  source venv/bin/activate
```

3. Install required libraries in requirements.txt

```bash
  pip install -r requirements.txt
```

4. Run Hello.py

```bash
  streamlit run Hello.py
```
## Authors

- [@yogishredder](https://github.com/yogishredder)
