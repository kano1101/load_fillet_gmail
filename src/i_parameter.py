from abc import abstractmethod, ABC


class IParameter(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()


class IParameterController(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    def get_label(self):
        pass


class IParameterInteractor(ABC):
    def __init__(self, parameter: IParameter):
        self.parameter = parameter


class IParameterRepository(ABC):
    def __init__(self, parameter: IParameter):
        self.parameter = parameter

    def get_output_product_worksheet(self):
        pass

    def get_output_expand_worksheet(self):
        pass
