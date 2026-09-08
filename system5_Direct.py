import os
import glob
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from asammdf import MDF

import lib.mdfExtractor as MdfExtractor
import lib.findProgram as findProgram

import emsOos.appendEmsOos as appendEmsOos
import emsOos.emsOos_Report as EmsOos_Report

#   クラスの定義
class Dat():
  pass

class DataClass():
  def __init__(self):
    self.value = ""
    self.time = ""

Data = Dat()
Data.Data_s = Dat()
Data.Data_m = Dat()

Config = Dat()
# mf4_file_list: MF4ファイルのリスト
# lenSourceList: sourceListの長さ
# execute_path: スクリプトの実行パス
# parent_path: 親ディレクトリのパス
# pathName: カレントディレクトリのパス
# template_path: テンプレートのパス
# dataBase_full_path: データベースのフルパス
# dataList_full_path: データリストのフルパス
# sourceData_Type: データの種類（Simulation / Original）
# Data_Dict: データ辞書のパス
# Data_ListName: データリストのパス
# sourceList: ソースチャンネルのリスト
# mf4_file: MF4ファイルのパス

Report = Dat()

def configSetup(Config):
  Config.sourceData_Type  = "Original"        #[Simulation / Original]
  Config.mf4_file         = "/Users/u1_aida/Dev_Data/Tool_Dev/Oos_Test_RL"
  Config.Data_Dict        = "signalDataBase_EmsOos_s.csv"
  Config.Data_ListName    = "signalDataList_EmsOos_s.csv"
  Config.sourceList      = ["RadarRL"]
  Config.template_path = os.path.join(Config.execute_path, "template")                            # 親ディレクトリのWorkフォルダを指定
  Config.lenSourceList = len(Config.sourceList)

  Config.dataBase_full_path = os.path.join(Config.execute_path, 'dataBase', Config.Data_Dict)
  Config.dataList_full_path = os.path.join(Config.execute_path, 'dataList', Config.Data_ListName)

  Config.signalDataBaseList = pd.read_csv(Config.dataBase_full_path)

  with open(Config.dataList_full_path, "r", encoding="utf-8") as f:
    Config.DataList.list_S = [line.strip() for line in f if line.strip()]

def preProc(Data, Config):
  Config.mf4_file_list = []
  Config.execute_path = os.path.dirname(os.path.abspath(__file__))                            # スクリプトの実行パスを取得
  Config.parent_path = os.path.dirname(Config.execute_path)                                   # 親ディレクトリのパスを取得
  Config.pathName = os.getcwd()                                                               # カレントディレクトリのパスを取得

def getMdfData(mdf, Data, Config):
  # Single（構造体データでない）データの読み込み
  for tarData in Config.DataList.list_S:
    for Config.sourceChannel in Config.sourceList:
      Data = MdfExtractor.get_Data(mdf, Data, Config, tarData)  # Radarのデータを取得

def aplicationProgram(mdf, Data, Report, Config):
  appendEmsOos.generateDatData(mdf, Data.Data_m,Config)
  EmsOos_Report.EmsOosReport_main(Data, Config, Report)

def main(Data, Report, Config):

  Config.sourceData_Type = "Original"        #[Simulation / Original]
  Config.DataList = Dat()
  Config.DataList.list_S = []
  Config.DataList.list_M = []
  Data.dataValue = []
  Data.dataTime = []

  preProc(Data, Config)
  configSetup(Config)

  if Config.mf4_file and os.path.isdir(Config.mf4_file):
    Config.singleMode = False  # フォルダー指定なら複数ファイルモード
  else:
    Config.singleMode = True   # ファイル直接指定または存在確認できない場合は単一モード


  if(Config.singleMode == False):
    # 複数ファイル（指定フォルダ内の一処理）モード
    mf4_folder = os.path.normpath(Config.mf4_file)  # パスの正規化
    mf4_file_list = list(set(glob.glob(os.path.join(mf4_folder, "*.mf4")) + glob.glob(os.path.join(mf4_folder, "*.MF4"))))
    mf4_file_list.sort()  # ファイル名でソート
    for mf4_File in mf4_file_list:
      mdf = MDF(mf4_File)
      Config.mf4_file_name = os.path.splitext(os.path.basename(mf4_File))[0]

      local = Dat()

      # Single（構造体データでない）データをData.Data_sに格納
      # Multi（構造体データ）データの場合は、各実行ファンクションで適宜Data.Data_mに格納すること
      getMdfData(mdf, Data.Data_s, Config)
      aplicationProgram(mdf, Data, Report, Config)
      print(f"Processed file: {mf4_File}")
     
  else:
    mf4_File = os.path.normpath(Config.mf4_file)  # パスの正規化
    mdf = MDF(mf4_File)
    Config.mf4_file_name = os.path.splitext(os.path.basename(mf4_File))[0]

    local = Dat()
    getMdfData(mdf, Data, Config)
    aplicationProgram(args, mdf, Data, Report, Config)

if __name__ == '__main__':
  main(Data, Report, Config)
