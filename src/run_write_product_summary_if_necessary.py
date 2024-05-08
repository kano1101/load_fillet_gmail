from dotenv import load_dotenv
from builder import DependencyBuilder

def run_write_product_summary_if_necessary():
    load_dotenv()
    dependency = DependencyBuilder()
    controller = dependency.build()

    controller.write_product_summary_if_necessary()

if __name__ == '__main__':
    run_write_product_summary_if_necessary()