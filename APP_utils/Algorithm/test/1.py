from GPR import GPR
import numpy as np
import pandas as pd

xls_file = pd.read_excel(
    'D:\Alai\paper_Alai\Journal of Mechanical Design\起重机论文\提交过程\【2】第一次审回\计算1.xlsx',
    sheet_name=0,
)

data = np.asarray(xls_file.values.tolist())
# print(xls_file.head())
print(data[:, 0])
