import re
import pandas as pd

# Read the text from file
with open('hw01_tinytr.txt', 'r', encoding='utf8') as f:
    text = f.read()

# Preprocess the text
text = text.lower()
token_list = re.findall(r"\w+(?:'\w+)?|[^\w\s]", text)
token_list = ["</s>" if token in [".", "?", "!"] else token for token in token_list]

# Add sentence boundaries <s> and </s>
token_list = ["<s>"] + token_list + ["</s>"]

# Unigram
words = " ".join(token_list).split()
unigram_count = pd.Series(words).value_counts().to_dict()

# Save unigram information
df_uni = pd.DataFrame({"unigrams": list(unigram_count.keys()), "frequency": list(unigram_count.values())})
df_uni["probability"] = df_uni["frequency"] / len(words)
df_uni = df_uni.sort_values("frequency", ascending=False)

with open('hw01_tinytr_Sonuc.txt', 'w', encoding='utf-8') as f:
    f.write(f"\n\n\nMetindeki Cümle Sayısı : {text.count('.') + text.count('!') + text.count('?')}\n")
    f.write(f"Metindeki Toplam Kelime Sayısı (Corpus Size) : {len(words)}\n")
    f.write(f"Metindeki Unique Kelime Sayısı (Vocabulary Size) : {len(unigram_count)} (<s> ve </s> dahil edildi)\n")
    f.write(df_uni.to_string(header=True, index=False))

# Bigram
bigrams = list(zip(words, words[1:]))
bigram_count = pd.Series(bigrams).value_counts().to_dict()
bigram_prob = {key: count / unigram_count[key[0]] for key, count in bigram_count.items()}

# Save bigram information
df_bi = pd.DataFrame({"bigram": list(bigram_count.keys()), "frequency": list(bigram_count.values()), "probability": list(bigram_prob.values())})
df_bi = df_bi.sort_values("frequency", ascending=False)[:100]

with open('hw01_tinytr_Sonuc.txt', 'w', encoding='utf-8') as f:
    f.write(f"\n\n\nBigram Bilgileri :\n")
    f.write(df_bi.to_string(header=True, index=False))

# UNK and Smoothing
new_text_UNK = text.replace("dün", "UNK")
words_UNK = new_text_UNK.split()
unigram_count_UNK = pd.Series(words_UNK).value_counts().to_dict()

# Create bigrams for UNK
bigrams_UNK = list(zip(words_UNK, words_UNK[1:]))
bigram_count_UNK = pd.Series(bigrams_UNK).value_counts().to_dict()
bigram_prob_UNK = {(word1, word2): (count + 0.5) / (unigram_count_UNK[word1] + len(unigram_count_UNK) * 0.5) for (word1, word2), count in bigram_count_UNK.items()}

# Save UNK and smoothed bigram information
df_UNK = pd.DataFrame({"bigram": list(bigram_count_UNK.keys()), "probability": list(bigram_prob.values()), "smoothed_probability": list(bigram_prob_UNK.values())})
df_UNK = df_UNK.sort_values("smoothed_probability", ascending=False)[:100]

with open('hw01_tinytr_Sonuc.txt', 'w', encoding='utf-8') as f:
    f.write(f"\n\n\nUNK değiştirme ve Smoothing sonrası :\n")
    f.write(df_UNK.to_string(header=True, index=False))

# Calculating Sentence Probability
def sentence_prob(sentence):
    sentence = sentence.lower().split()
    sentence = ["UNK" if word not in words_UNK else word for word in sentence]
    prob = 1
    for j in range(len(sentence) - 1):
        prob *= bigram_prob_UNK.get((sentence[j], sentence[j+1]), 0)
    return prob

with open('hw01_tinytr_Sonuc.txt', 'w', encoding='utf-8') as f:
    f.write(f"\n\n\n<s> Ali eve geldi </s>: {sentence_prob('<s> ali eve geldi </s>')}\n")
    f.write(f"\n<s> Mehmet eve ve okula Pazartesi gitti </s>: {sentence_prob('<s> Mehmet eve ve okula Pazartesi gitti </s>')}\n")
