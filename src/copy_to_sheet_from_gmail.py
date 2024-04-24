from access import get_soups_with_gmail_labels


def get_product_amount_to_sheet_from_gmail(labels):
    soups = get_soups_with_gmail_labels(labels)

    list_product_and_amount = []
    for soup in soups:
        strong_tags = soup.find_all('strong')
        product_name = soup.find('h1').text if soup.find('h1') else "Unknown Product"
        # 条件に一致するテキストを抽出
        for tag in strong_tags:
            if tag.text == '収量':
                yield_text = tag.next_sibling
                amount_and_unit = yield_text.strip().split(' ')
                list_product_and_amount.append([product_name] + amount_and_unit)

    return list_product_and_amount


def copy_to_sheet_from_gmail(labels):
    soups = get_soups_with_gmail_labels(labels)
    print(f"メッセージの件数: {len(soups)}")

    results = []
    for soup in soups:
        product_name = soup.find('h1').text if soup.find('h1') else "Unknown Product"
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                mixture_values = [cell.get_text() for cell in cells]
                if mixture_values:
                    if mixture_values[0] != "水" and "グラタン" not in mixture_values[0]:
                        results.append([product_name] + mixture_values)

    product_names = [[row[0]] for row in results]
    mixture_names = [[row[1]] for row in results]
    amounts = [[row[2]] for row in results]
    units = [[row[3]] for row in results]

    return product_names, mixture_names, amounts, units
