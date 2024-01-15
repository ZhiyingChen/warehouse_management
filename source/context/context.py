from ..info import InputData
from ..info import Config
from ..result import ResultStorage


class Context:

    def __init__(self):
        self.input_data: InputData
        self.config: Config
        self.result_storage: ResultStorage
