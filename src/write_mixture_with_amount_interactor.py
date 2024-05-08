import injector
from i_interactor import IWriteMixtureWithAmountInteractor, IRepository, IPresenter
from i_parameter import IInteractorParameter
from utils import to_num


class MixtureWithAmountInputData:
    def __init__(self, soups) -> None:
        self.soups = soups

    def get_soups(self):
        return self.soups


class MixtureWithAmountOutputData:
    def __init__(self, data) -> None:
        self.data = data


class SaveMixtureWithAmountData:
    def __init__(self, rows) -> None:
        self.rows = rows

    def get_rows(self):
        return self.rows


class WriteMixtureWithAmountInteractor(IWriteMixtureWithAmountInteractor[MixtureWithAmountInputData]):
    @injector.inject
    def __init__(self, parameter: IInteractorParameter, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: MixtureWithAmountInputData):
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
        amounts = [to_num(row[2]) for row in appended]
        units = [row[3] for row in appended]

        result = list(zip(product_names, mixture_names, amounts, units))

        save_result = result

        save_data = SaveMixtureWithAmountData(save_result)
        self.repository.save_mixture_and_amount_columns(save_data)

        output_result = result

        output_data = MixtureWithAmountOutputData(output_result)
        self.presenter.output(output_data)
