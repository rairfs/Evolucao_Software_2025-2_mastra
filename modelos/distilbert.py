from transformers import pipeline
import pandas

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    top_k=None
)


csv = pandas.read_csv("../output/pr_comments.csv", sep=";")
csvResultToConcat = []

for index, row in csv.iloc[::1].iterrows():
    pr_number = str(row.get("pr_number"))
    user = str(row.get("user"))
    comment = str(row.get("comment"))

    if "[bot]" not in user:
        sentimentClassification = distilled_student_sentiment_classifier(comment)
        jsonSentimentClassification = sentimentClassification[0]

        df_scores = pandas.json_normalize(jsonSentimentClassification)
        df_pivot = df_scores.set_index('label').T
        df_pivot['pr_number'] = pr_number
        df_pivot['user'] = user
        df_pivot['comment'] = comment

        cols = ['pr_number', 'user', 'comment', 'positive', 'neutral', 'negative']
        df_final_row = df_pivot[cols]

        #df_final.to_csv("distilbert_result.csv", index=False)
        csvResultToConcat.append(df_final_row)

df_csv_final = pandas.concat(csvResultToConcat, ignore_index=True)
df_csv_final.to_csv("results/distilbert.csv", index=False)