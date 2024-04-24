import json

def replace_article_names(sh):
    assign_worksheet = sh.worksheet("作業用")

    articles_worksheet = sh.worksheet("材料")
    article_names = articles_worksheet.col_values(2)[1:]

    gmail_worksheet = sh.worksheet("Gmail")
    mixture_names_replace = gmail_worksheet.col_values(2)[1:]
    mixture_names_for_compare_to_article = gmail_worksheet.col_values(7)[1:]

    for i, searching_mixture_name in enumerate(mixture_names_for_compare_to_article):
        if searching_mixture_name in article_names:
            index = article_names.index(searching_mixture_name)
            article_names[index] = mixture_names_replace[i]

    result = []
    for article_name in article_names:
        result.append([article_name])

    assign_worksheet.update('B2', result)


def replace_product_names(sh):
    assign_worksheet = sh.worksheet("作業用")

    articles_worksheet = sh.worksheet("材料")
    article_names = articles_worksheet.col_values(2)[1:]

    gmail_worksheet = sh.worksheet("Gmail")
    mixture_names_replace = gmail_worksheet.col_values(2)[1:]
    mixture_names_for_compare_to_article = gmail_worksheet.col_values(7)[1:]

    for i, searching_mixture_name in enumerate(mixture_names_for_compare_to_article):
        if searching_mixture_name in article_names:
            index = article_names.index(searching_mixture_name)
            article_names[index] = mixture_names_replace[i]

    result = []
    for article_name in article_names:
        result.append([article_name])

    assign_worksheet.update('B2', result)
