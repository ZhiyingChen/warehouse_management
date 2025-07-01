import pandas as pd
import os

def out_status(out_index: int, output_folder: str='./'):
    col = ['status']
    record_lt = [{'status': str(out_index)}]
    df = pd.DataFrame(record_lt, columns=col)
    df.to_csv(os.path.join(output_folder,'status.csv'))
