import os
import glob
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from asammdf import MDF

import lib.mdfExtractor as mdfExtractor

def generateDatData(mdf, Data, Config):
  # Multi（構造体データ）データの読み込み
  dataBase_full_path = os.path.join(Config.execute_path, 'dataBase', 'signalDataBase_EmsOos.csv')
  dataList_full_path = os.path.join(Config.execute_path, 'dataList', 'signalDataList_EmsOos.csv')

  with open(dataBase_full_path, "r", encoding="utf-8") as f:
    Config.signalDataBaseList = [line.strip().split(",") for line in f if line.strip()]

  with open(dataList_full_path, "r", encoding="utf-8") as f:
    Config.DataList.list_M = [line.strip() for line in f if line.strip()]
  
  for tarData in Config.DataList.list_M:
    for Config.sourceChannel in Config.sourceList:
      Data = mdfExtractor.get_MultiData(mdf, Data, Config.sourceChannel, Config.signalDataBaseList, tarData, 0, 32)
  
  print("Debug: generateDatData - Data generation completed for all signals in the list.")
  return Data
  


