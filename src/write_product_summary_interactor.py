import injector
from i_interactor import IWriteProductSummaryInteractor, IRepository, IPresenter
from i_parameter import IInteractorParameter


class ProductSummaryInputData:
    def __init__(self, soups, label) -> None:
        self.soups = soups
        self.label = label

    def get_soups(self):
        return self.soups

    def get_label(self):
        return self.label


class ProductSummaryOutputData:
    def __init__(self, data) -> None:
        self.data = data


class SaveProductSummaryData:
    def __init__(self, rows) -> None:
        self.rows: list[[str, str, str]] = rows

    def get_rows(self):
        return self.rows


class WriteProductSummaryInteractor(IWriteProductSummaryInteractor[ProductSummaryInputData]):
    @injector.inject
    def __init__(self, parameter: IInteractorParameter, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: ProductSummaryInputData):
        print("WriteProductSummaryInteractor.handle start")
        soups = input_data.get_soups()
        label = input_data.get_label()

        list_product_and_amount: list[[str, str, str, str]] = []

        for soup in soups:
            strong_tags = soup.find_all('strong')
            product_name = soup.find('h1').text if soup.find('h1') else "Unknown Product"
            # 条件に一致するテキストを抽出
            for tag in strong_tags:
                if tag.text == '収量':
                    yield_text = tag.next_sibling
                    amount_and_unit = yield_text.strip().split(' ')
                    list_product_and_amount.append([product_name] + [label] + amount_and_unit)

        save_result = list_product_and_amount
        print(f"{len(list_product_and_amount)} products found")

        save_data = SaveProductSummaryData(save_result)
        self.repository.save_product_summary_direct_if_necessary(save_data)

        # output_result = result
        #
        # output_data = ProductSummaryOutputData(output_result)
        # self.presenter.output(output_data)
