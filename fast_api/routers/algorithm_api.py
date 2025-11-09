from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
import pandas as pd
from fast_api.service.algorithm_runner import run_algorithm

router = APIRouter(prefix="/api", tags=["Algorithm"])


class RunRequest(BaseModel):
    files: Dict[str, list]  # 每个文件是一个 DataFrame 转成 list of dict


@router.post("/run")
def run_model(req: RunRequest):
    # 把前端传来的 json 转成 pandas DataFrame
    param_file_dict = {name: pd.DataFrame(rows) for name, rows in req.files.items()}
    result = run_algorithm(param_file_dict)
    return result
