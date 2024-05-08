from dotenv import load_dotenv
from builder import DependencyBuilder

def run_write_mixture_with_amount():
    load_dotenv()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.write_mixture_with_amount()

if __name__ == '__main__':
    run_write_mixture_with_amount()