import injector
from i_interactor import IWriteMixtureWithAmountInteractor, IRepository, IPresenter
from i_parameter import IParameterInteractor


class InputData:
    def __init__(self, soups) -> None:
        self.soups = soups

    def get_soups(self):
        return self.soups


class OutputData:
    def __init__(self, data) -> None:
        self.data = data


class SaveData:
    def __init__(self, data) -> None:
        self.data = data

    def get_row_properties(self, index):
        return self.data[index]


class WriteMixtureWithAmountInteractor(IWriteMixtureWithAmountInteractor[InputData]):
    @injector.inject
    def __init__(self, parameter: IParameterInteractor, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: InputData):
        soups = input_data.soups
        appended = []

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
                            appended.append([product_name] + mixture_values)

        product_names = [row[0] for row in appended]
        mixture_names = [row[1] for row in appended]
        amounts = [float(row[2].replace(',', '')) for row in appended]
        units = [row[3] for row in appended]

        result = list(zip(product_names, mixture_names, amounts, units))

        save_result = result

        save_data = SaveData(save_result)
        self.repository.save(save_data)

        output_result = result

        output_data = OutputData(output_result)
        self.presenter.output(output_data)
        # soups = get_soups_with_gmail_labels(labels)
        #
        # list_product_and_amount = []
        # for soup in soups:
        #     strong_tags = soup.find_all('strong')
        #     product_name = soup.find('h1').text if soup.find('h1') else "Unknown Product"
        #     # 条件に一致するテキストを抽出
        #     for tag in strong_tags:
        #         if tag.text == '収量':
        #             yield_text = tag.next_sibling
        #             amount_and_unit = yield_text.strip().split(' ')
        #             list_product_and_amount.append([product_name] + amount_and_unit)
        #
        # return list_product_and_amount
