from dotenv import load_dotenv
from builder import DependencyBuilder

def run_calc_and_write_mixture_similarity():
    load_dotenv()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.calc_and_write_mixture_similarity()

if __name__ == '__main__':
    run_calc_and_write_mixture_similarity()