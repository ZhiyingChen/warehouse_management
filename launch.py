from source.context import Context
from source.info.data_loader import DataLoader
from source.info.config import Config
from source.utils import log, status
from source.model import ModelManager
from source.result.processor import ResultProcessor
from source.result.dumper import ResultDumper
import time
import logging

if __name__ == "__main__":
    config = Config()
    context = Context()
    context.config = config
    logger = log.setup_log(config.output_folder)
    status.out_status(0)
    st = time.time()
    try:

        data_loader = DataLoader()
        data_loader.generate_data(context=context)

        model_manager = ModelManager()
        model_manager.create_constraints(context=context)
        model_manager.solve_all_objectives(context=context)
        sol_dict = model_manager.get_solution()

        result_processor = ResultProcessor(sol_dict=sol_dict)
        result_processor.generate_results(context=context)

        result_dumper = ResultDumper()
        result_file_dict = result_dumper.generate_all_files(context=context)

        logging.info("success")
        logging.info("Total running time: {}".format(time.time() - st))

        status.out_status(1)

    except Exception as e:
        logging.exception(e)
        logging.error("fail")
        logging.info("Total running time: {}".format(time.time() - st))
        status.out_status(-1)
