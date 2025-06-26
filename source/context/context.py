from ..info import InputData
from ..info import Config
from ..result import ResultStorage


class Context:

    def __init__(self):
        self.input_data: InputData = InputData()
        self.config: Config = Config()
        self.result_storage: ResultStorage = ResultStorage()
