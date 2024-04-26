from presenter import IViewer
from presenter import ViewModel


class ConsoleViewer(IViewer):
    def view(self, view_model: ViewModel):
        print(f'実行OK 製品名: {view_model.data}')
        for data in view_model.data:
            print(f'記録済: {data}')
        return []
