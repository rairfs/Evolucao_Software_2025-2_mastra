import pandas as pd
import matplotlib.pyplot as plt

nlp_bert = pd.read_csv("./modelos/results/nlptown_bert.csv")
multi_sent = pd.read_csv("./modelos/results/multilingual-sentiment.csv")
distil_bert = pd.read_csv("./modelos/results/distilbert.csv")

for col in ['1 star', '2 stars', '3 stars', '4 stars', '5 stars']:
    nlp_bert[col] = pd.to_numeric(nlp_bert[col], errors='coerce').fillna(0)
for col in ['Positive', 'Neutral', 'Negative']:
    multi_sent[col] = pd.to_numeric(multi_sent[col], errors='coerce').fillna(0)
for col in ['positive', 'neutral', 'negative']:
    distil_bert[col] = pd.to_numeric(distil_bert[col], errors='coerce').fillna(0)

def stars_to_sentiment(row):
    scores = row[['1 star', '2 stars', '3 stars', '4 stars', '5 stars']]
    max_star = scores.idxmax()
    if max_star in ['4 stars', '5 stars']:
        return "positive"
    elif max_star == '3 stars':
        return "neutral"
    else:
        return "negative"

nlp_bert['sentiment'] = nlp_bert.apply(stars_to_sentiment, axis=1)

multi_sent['sentiment'] = multi_sent[['Positive', 'Neutral', 'Negative']].idxmax(axis=1).str.lower()

def classify_distil(row, diff_threshold=0.15, neutral_min=0.25):
    pos, neu, neg = row['positive'], row['neutral'], row['negative']
    if abs(pos - neg) < diff_threshold and neu > neutral_min:
        return "neutral"
    elif pos > neg:
        return "positive"
    else:
        return "negative"

distil_bert['sentiment'] = distil_bert.apply(classify_distil, axis=1)

categories = ['positive', 'neutral', 'negative']

def count_with_missing(df):
    counts = df['sentiment'].value_counts()
    for c in categories:
        if c not in counts:
            counts[c] = 0
    return counts[categories]

nlp_counts = count_with_missing(nlp_bert)
multi_counts = count_with_missing(multi_sent)
distil_counts = count_with_missing(distil_bert)

colors = {
    'positive': '#4CAF50',
    'neutral': '#2196F3',
    'negative': '#FF9800'
}

def autopct_format(values):
    def inner_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}% ({val})'
    return inner_autopct

plt.figure(figsize=(15,5))

plt.subplot(1, 3, 1)
plt.pie(
    distil_counts,
    labels=distil_counts.index,
    autopct=autopct_format(distil_counts),
    startangle=140,
    colors=[colors[label] for label in distil_counts.index]
)
plt.title("DistilBERT - Pontuação com Range de Neutralidade")
plt.legend(
    [f"Regra: |positive - negative| < 0.15 e neutral > 0.25 → Neutral"],
    loc="lower center", bbox_to_anchor=(0.5, -0.2), fontsize=9
)

plt.subplot(1, 3, 2)
plt.pie(
    multi_counts,
    labels=multi_counts.index,
    autopct=autopct_format(multi_counts),
    startangle=140,
    colors=[colors[label] for label in multi_counts.index]
)
plt.title("Multilingual Sentiment - Classificação Direta")

plt.subplot(1, 3, 3)
plt.pie(
    nlp_counts,
    labels=nlp_counts.index,
    autopct=autopct_format(nlp_counts),
    startangle=140,
    colors=[colors[label] for label in nlp_counts.index]
)
plt.title("NLPTown BERT - Avaliação em Estrelas")
plt.legend(
    ["Regra: 1–2★ → Negativo | 3★ → Neutro | 4–5★ → Positivo"],
    loc="lower center", bbox_to_anchor=(0.5, -0.2), fontsize=9
)

plt.tight_layout()

plt.savefig("./comparacao_modelos_sentimento.png", dpi=300, bbox_inches="tight")

plt.show()
