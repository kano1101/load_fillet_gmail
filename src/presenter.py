import injector
from calc_and_write_mixture_similarity_interactor import SimilarityOutputData
from i_interactor import IPresenter
from i_presenter import IViewer


class ViewModel:
    def __init__(self, output_data: SimilarityOutputData):
        self.data = output_data.data


class Presenter(IPresenter[SimilarityOutputData]):
    @injector.inject
    def __init__(self, viewer: IViewer):
        self.viewer = viewer

    def output(self, output_data: SimilarityOutputData):
        view_model = ViewModel(output_data)
        self.viewer.view(view_model)
