from i_parameter import IParameter, IParameterController
import injector


class ParameterController(IParameterController):
    @injector.inject
    def __init__(self, parameter: IParameter):
        self.parameter = parameter
