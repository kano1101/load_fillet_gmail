import injector
from calc_and_write_mixture_similarity_interactor import OutputData
from i_interactor import IPresenter
from i_presenter import IViewer


class ViewModel:
    def __init__(self, output_data: OutputData):
        self.data = output_data.data


class Presenter(IPresenter[OutputData]):
    @injector.inject
    def __init__(self, viewer: IViewer):
        self.viewer = viewer

    def output(self, output_data: OutputData):
        view_model = ViewModel(output_data)
        self.viewer.view(view_model)
