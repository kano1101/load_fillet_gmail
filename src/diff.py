from difflib import SequenceMatcher


def assign_most_similarity_as_manual(gmail_worksheet):
    gmail_names = gmail_worksheet.col_values(3)[1:]
    manual_names = gmail_worksheet.col_values(13)[1:]

    values = []
    for i in range(0, len(gmail_names)):
        b_value = gmail_names[i]
        m_value = manual_names[i]
        similarity = SequenceMatcher(None, b_value, m_value).ratio()

        print(f"{gmail_names[i]}, {similarity}")
        values.append([similarity])

    gmail_worksheet.update('L2', values)


def assign_most_similar_mixture(gmail_worksheet, articles_worksheet, products_worksheet):
    """"""
    article_names = articles_worksheet.col_values(2)[1:]
    product_names = products_worksheet.col_values(2)[1:]

    mixture_names = article_names + product_names

    gmail_names = gmail_worksheet.col_values(3)[1:]

    values = []
    for gmail_name in gmail_names:
        b_value = gmail_name

        # 最も類似度の高い材料を選択
        highest_similarity = 0
        most_similar_mixture = ""
        for mixture in mixture_names:
            similarity = SequenceMatcher(None, b_value, mixture).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_mixture = mixture

        # 最も類似度の高い材料と類似度を計算して％表示で追加
        result = [most_similar_mixture, highest_similarity]
        print(f"{gmail_name}, {most_similar_mixture}")
        values.append(result)

    gmail_worksheet.update('K2', values)
