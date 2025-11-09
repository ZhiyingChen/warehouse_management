import time
from source.context import Context
from source.info import Config
from source.info.data_loader import DataLoader
from source.model import ModelManager
from source.result.processor import ResultProcessor
from source.result.dumper import ResultDumper


def run_algorithm(input_files: dict):
    """封装算法主逻辑，返回结果字典"""
    config = Config(load_from_file=False)
    context = Context()
    context.config = config

    st_time = time.time()
    try:
        data_loader = DataLoader(param_file_dict=input_files)
        data_loader.generate_data(context=context)

        model_manager = ModelManager()
        model_manager.create_constraints(context=context)
        model_manager.solve_all_objectives(context=context)
        sol_dict = model_manager.get_solution()

        result_processor = ResultProcessor(sol_dict=sol_dict)
        result_processor.generate_results(context=context)

        result_dumper = ResultDumper()
        result_file_dict = result_dumper.generate_all_files(context=context)

        runtime = round(time.time() - st_time, 2)

        return {"success": True, "runtime": runtime, "results": result_file_dict}
    except Exception as e:
        return {"success": False, "error": str(e)}
