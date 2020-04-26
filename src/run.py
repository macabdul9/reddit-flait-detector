from rfd.TextPreprocessor import TextPreprocessor
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

if __name__ == "__main__":
    ## read csv (if session has expired)
    df = pd.read_csv("df.csv")
    # count the unigrams after processing the text
    text_preprocessor = TextPreprocessor(text_attribute='text')
    df_preprocessed = text_preprocessor.transform(df)
    df_preprocessed['unigram_count'] = df_preprocessed.text.progress_apply(lambda x: len(x.split()))
    print(f'shape before cleaning {df_preprocessed.shape}')
    # Dropping the rows based on NA text 
    df_preprocessed = df_preprocessed.dropna(subset=['text'], axis=0)
    print(f'shape after removing na {df_preprocessed.shape}')

    # # Filter out those rows which have more than 10 words
    ## df_preprocessed = df_preprocessed[df_preprocessed.unigram_count > 5]
    ## print(f'shape after removing unigram thresh {df_preprocessed.shape}')

    # Remove rows which have duplicate text data (there might be some fields which will have same text after preprocessing)
    df_preprocessed = df_preprocessed.drop_duplicates(subset='text', keep='first')
    print(f'shape after removing duplicate {df_preprocessed.shape}')
    df_preprocessed.to_csv("df_processed.csv", index=False)