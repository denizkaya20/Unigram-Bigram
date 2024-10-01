This program performs language processing and probability calculations on a given Turkish text file. It determines the number of sentences and words in the text, calculates unigram and bigram frequencies and their probabilities. Additionally, it replaces words that appear only once with "UNK" and computes smoothed bigram probabilities using the Add-k (k=0.5) smoothing method. Finally, it calculates the probability values of sentences entered by the user using these smoothed bigram probabilities.

Contents
Requirements
Installation
Usage
Program Features
Example Run
Results
Notes
Contact
Requirements
Python 3.x
Required libraries:
re (Regular Expressions)
collections.Counter
pandas (optional, for displaying data in table format)
Installation
Install Python

Download and install Python 3.x from the official website.

Install Required Libraries

Install the necessary libraries by running the following command in the terminal or command prompt:

bash
Kodu kopyala
pip install pandas
Usage
Prepare the Program File

Save the program code in a file (e.g., main.py).
Prepare the Text File

Place the text file to be processed (in .txt format and UTF-8 encoding) in the same directory as the program.
Run the Program

Execute the program using the following command in the terminal or command prompt:

bash
Kodu kopyala
python main.py
Provide Necessary Inputs

The program will prompt you to enter the name of the text file.
You will then be asked to enter two sentences whose probabilities will be calculated.
Program Features
Determining the Number of Sentences

Counts the number of sentences in the text using period (.), question mark (?), and exclamation mark (!) as indicators.

Creating a Token List

Differentiates between words and sentence-ending punctuation marks.
Converts all words to lowercase.
Inserts <s> at the beginning and </s> at the end of each sentence.
Calculating Unigram and Bigram Frequencies and Probabilities

Calculates the frequencies of unigrams and bigrams.
Determines probability values based on these frequencies.
UNK Replacement and Smoothing Process

Replaces words that appear only once in the text with UNK.
Calculates smoothed bigram probabilities using the Add-k (k=0.5) smoothing method.
Calculating Sentence Probabilities

Computes the probability values of user-entered sentences using the smoothed bigram probabilities.
Treats words not found in the text as UNK.

The sonuc.txt file will contain the following information:

Number of Sentences in the Text

Total Number of Words in the Text (Corpus Size)

Number of Unique Words in the Text (Vocabulary Size)

Unigram Information

Unigram    Frequency    Probability
--------   ---------    -----------
ali        3            0.05
went       2            0.033
...
Bigram Information

Bigram               Frequency    Probability
------------------   ---------    -----------
('<s>', 'ali')       3            0.6
('ali', 'went')      2            0.66
...
Smoothed Bigram Information (Top 100 Bigrams)

Bigram               Original Probability    Smoothed Probability
------------------   -------------------     ---------------------
('<s>', 'ali')       0.6                     0.58
('ali', 'UNK')       0                       0.02
...
Probabilities of the Sentences You Entered


Sentence: Ali went to school
Probability: 0.000345

Sentence: Today the weather is very nice
Probability: 0.000123

The text files must be in UTF-8 format.
Definition of a Word

Words consist only of letters (Turkish and English letters).
Numbers, punctuation marks, etc., are not included in the token list.
Sentence Boundaries

Sentence endings are determined by period (.), question mark (?), and exclamation mark (!).
UNK Word

Words that appear only once in the text are replaced with UNK.
Add-k Smoothing A value of k=0.5 is used for the smoothing process.

If you encounter errors, ensure that the text file is correctly formatted and that the required libraries are installed.

Contact
For any issues or questions, please contact:

Email: denizkaya83@yahoo.com
