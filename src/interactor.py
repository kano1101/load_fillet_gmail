import injector
from i_interactor import IInteractor, IRepository, IPresenter
from i_parameter import IParameterInteractor


class InputData:
    def __init__(self) -> None:
        pass


class OutputData:
    def __init__(self) -> None:
        pass


class Interactor(IInteractor[InputData]):
    @injector.inject
    def __init__(self, parameter: IParameterInteractor, repository: IRepository, presenter: IPresenter) -> None:
        self.parameter = parameter
        self.repository = repository
        self.presenter = presenter

    def handle(self, input_data: InputData):
        save_data = input_data
        self.repository.save(save_data)
        output_data = OutputData()
        self.presenter.output(output_data)
