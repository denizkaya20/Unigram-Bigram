import re
import pandas as pd

# Dosya ismini klavyeden okuma
filename = input("Lütfen metin dosyasının ismini girin: ")
with open(filename, 'r', encoding='utf8') as f:
    text = f.read()

# Metni küçük harflere çevirme
text = text.lower()

# Cümleleri cümle sonu noktalama işaretlerine göre bölme
sentences = re.split(r'[.!?]', text)
sentences = [s.strip() for s in sentences if s.strip()]  # Boş cümleleri çıkar

# Cümle sayısını hesaplama
sentence_count = len(sentences)

# Simge listesini oluşturma ve cümle başı ve sonu simgelerini ekleme
token_list = []
for sentence in sentences:
    # Kelimeleri bulma (sadece harflerden oluşan kelimeler)
    words_in_sentence = re.findall(r'[a-zA-ZığüşöçİĞÜŞÖÇ]+', sentence)
    if words_in_sentence:
        token_list.extend(['<s>'] + words_in_sentence + ['</s>'])

# Unigram frekanslarını hesaplama
unigram_count = pd.Series(token_list).value_counts().to_dict()

# Toplam kelime sayısı (corpus size)
total_unigrams = len(token_list)

# Unigram olasılıklarını hesaplama
df_uni = pd.DataFrame({
    "unigrams": list(unigram_count.keys()),
    "frequency": list(unigram_count.values())
})
df_uni["probability"] = df_uni["frequency"] / total_unigrams
df_uni = df_uni.sort_values("frequency", ascending=False)

# Bigram frekanslarını hesaplama
bigrams = list(zip(token_list, token_list[1:]))
bigram_count = pd.Series(bigrams).value_counts().to_dict()

# Bigram olasılıklarını hesaplama
bigram_prob = {key: count / unigram_count[key[0]] for key, count in bigram_count.items()}

# Sonuçları 'hw01_tinytr_Sonuc.txt' dosyasına yazma
with open('hw01_tinytr_Sonuc.txt', 'w', encoding='utf-8') as f:
    f.write(f"Metindeki Cümle Sayısı : {sentence_count}\n")
    f.write(f"Metindeki Toplam Kelime Sayısı (Corpus Size) : {total_unigrams}\n")
    f.write(f"Metindeki Unique Kelime Sayısı (Vocabulary Size) : {len(unigram_count)} (<s> ve </s> dahil edildi)\n\n")
    f.write("Unigram Bilgileri (Frekansa Göre Büyükten Küçüğe Sıralı):\n")
    f.write(df_uni.to_string(header=True, index=False))
    f.write("\n\n")

    # Bigram bilgilerini yazma
    df_bi = pd.DataFrame({
        "bigram": [str(bigram) for bigram in bigram_count.keys()],
        "frequency": list(bigram_count.values()),
        "probability": list(bigram_prob.values())
    })
    df_bi = df_bi.sort_values("frequency", ascending=False)
    f.write("Bigram Bilgileri (Frekansa Göre Büyükten Küçüğe Sıralı):\n")
    f.write(df_bi.to_string(header=True, index=False))
    f.write("\n\n")

# En az geçen 1 kelimeyi 'UNK' ile değiştirme
single_occurrence_words = [word for word, count in unigram_count.items() if count == 1]
token_list_UNK = ['UNK' if word in single_occurrence_words else word for word in token_list]

# UNK ile değiştirilmiş unigram frekanslarını hesaplama
unigram_count_UNK = pd.Series(token_list_UNK).value_counts().to_dict()

# Bigram frekanslarını yeniden hesaplama
bigrams_UNK = list(zip(token_list_UNK, token_list_UNK[1:]))
bigram_count_UNK = pd.Series(bigrams_UNK).value_counts().to_dict()

# Düzeltilmiş bigram olasılıklarını hesaplama (Add-k smoothing, k=0.5)
k = 0.5
vocab_size = len(unigram_count_UNK)
smoothed_bigram_prob = {}
for bigram in bigram_count_UNK:
    count = bigram_count_UNK[bigram]
    smoothed_prob = (count + k) / (unigram_count_UNK[bigram[0]] + k * vocab_size)
    smoothed_bigram_prob[bigram] = smoothed_prob

# En yüksek 100 düzeltilmiş bigramı bulma
sorted_smoothed_bigrams = sorted(smoothed_bigram_prob.items(), key=lambda x: x[1], reverse=True)[:100]

# Orijinal bigram olasılıklarını da hesaplama
original_bigram_prob_UNK = {}
for bigram in bigram_count_UNK:
    original_prob = bigram_count_UNK[bigram] / unigram_count_UNK[bigram[0]]
    original_bigram_prob_UNK[bigram] = original_prob

df_smoothed = pd.DataFrame({
    "bigram": [str(bigram) for bigram, _ in sorted_smoothed_bigrams],
    "original_probability": [original_bigram_prob_UNK[bigram] for bigram, _ in sorted_smoothed_bigrams],
    "smoothed_probability": [prob for _, prob in sorted_smoothed_bigrams]
})

# Sonuç dosyasına ekleme yapma
with open('hw01_tinytr_Sonuc.txt', 'a', encoding='utf-8') as f:
    f.write("UNK değiştirme ve Smooting İşleminden Sonra En Yüksek 100 Bigram Değeri:\n")
    f.write(df_smoothed.to_string(header=True, index=False))
    f.write("\n\n")

# Cümle olasılığını hesaplayan fonksiyon
def sentence_prob(sentence_tokens):
    prob = 1.0
    for i in range(len(sentence_tokens) - 1):
        bigram = (sentence_tokens[i], sentence_tokens[i+1])
        numerator = bigram_count_UNK.get(bigram, 0) + k
        denominator = unigram_count_UNK.get(sentence_tokens[i], 0) + k * vocab_size
        prob *= numerator / denominator
    return prob

# Kullanıcıdan en az iki cümle okuma ve olasılıklarını hesaplama
for i in range(2):
    user_sentence = input(f"Lütfen {i+1}. cümleyi girin: ")
    user_sentence_tokens = re.findall(r'[a-zA-ZığüşöçİĞÜŞÖÇ]+', user_sentence.lower())
    user_sentence_tokens = ['<s>'] + user_sentence_tokens + ['</s>']
    user_sentence_tokens = ['UNK' if word in single_occurrence_words else word for word in user_sentence_tokens]
    sentence_probability = sentence_prob(user_sentence_tokens)
    with open('hw01_tinytr_Sonuc.txt', 'a', encoding='utf-8') as f:
        f.write(f"Cümle {i+1}: {' '.join(user_sentence_tokens)}\n")
        f.write(f"Olasılığı: {sentence_probability}\n\n")

print("İşlem tamamlandı. Sonuçlar 'hw01_tinytr_Sonuc.txt' dosyasına kaydedildi.")
