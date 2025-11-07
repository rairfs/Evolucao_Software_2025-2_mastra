from transformers import pipeline
import pandas

pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

csv = pandas.read_csv("../output/pr_comments.csv", sep=";")
csvResultToConcat = []

for index, row in csv.iloc[::1].iterrows():
    pr_number = str(row.get("pr_number"))
    user = str(row.get("user"))
    comment = str(row.get("comment"))

    if "[bot]" not in user:
        sentimentClassification = pipe(comment)

        result_dict = {
            'pr_number': pr_number,
            'user': user,
            'comment': comment,
            'Positive': 0.0,
            'Negative': 0.0,
            'Neutral': 0.0
        }

        if sentimentClassification and len(sentimentClassification) > 0:
            score_data = sentimentClassification[0]
            label = score_data.get("label")
            score = score_data.get("score")

            if label and score is not None:
                result_dict[label.capitalize()] = score

        csvResultToConcat.append(result_dict)

df_csv_final = pandas.DataFrame(csvResultToConcat)
df_csv_final.to_csv("results/multilingual-sentiment.csv", index=False)