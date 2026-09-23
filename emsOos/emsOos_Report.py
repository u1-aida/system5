import numpy as np
import csv
import os
import glob

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use('ggplot')
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

import lib.localSetup as localSetup
import lib.preProc as preProc
import lib.findProgram as findProgram

#   クラスの定義
class Dat():
  pass

class DataClass():
  def __init__(self):
    self.value = ""
    self.time = ""

def emsOosPlot_PreProc(Report, targetList, targetData, idxNum, idxSource):
  Report.plotNum = 1
  lenData = len(targetList)
  for idx in range(lenData):
    pos = targetList[idx]
    posBegin = max(0, pos - 10)
    posEnd = min(len(Report.dataValue[1][0][idxSource][idxNum]) - 1, pos + 10)
    emsOosPlot(Report, idxNum, idxSource, posBegin, posEnd)

def emsOosPlot (Report, idxNum, idxSource, posBegin, posEnd):
  figure = plt.figure(figsize=(16, 9))
  numPlotCol = 1
  numPlotRow = 3
  lenData = numPlotRow * numPlotCol
  gs_master = GridSpec(nrows=numPlotRow, ncols=numPlotCol, hspace=0.4, wspace=0.15, left=0.08, right=0.95, top=0.93, bottom=0.05,height_ratios = [0.3, 0.7, 1])
  axes = []
  for Col in range(numPlotCol):
    for Row in range(numPlotRow):
      if len(axes) >= lenData:
        break
      axes.append(figure.add_subplot(gs_master[Row, Col]))
    if len(axes) >= lenData:
      break

  fig_0, fig_1, fig_2 = axes
  fig_0.plot(Report.dataTime[0][0][idxSource][posBegin:posEnd], Report.dataValue[0][0][idxSource][posBegin:posEnd])
  fig_0.legend(Report.plotList[0])
  fig_0.set_title(f"{Report.evaluationItem[0]}, ID = {idxNum}", fontsize=12)

  fig_1.plot(Report.dataTime[1][0][idxSource][idxNum][posBegin:posEnd], Report.dataValue[1][0][idxSource][idxNum][posBegin:posEnd])
  fig_1.legend(Report.plotList[1])
  fig_1.set_title(f"{Report.evaluationItem[1]}, ID = {idxNum}", fontsize=12)

  fig_2.plot(Report.dataTime[2][0][idxSource][idxNum][posBegin:posEnd], Report.dataValue[2][0][idxSource][idxNum][posBegin:posEnd])
  #fig_0.set_yticks([0, 0.5, 1], ["valid", "debouncing", "invalid"])
  fig_2.legend(Report.plotList[2])
  fig_2.set_title(Report.evaluationItem[2], fontsize=12)
  plt.tight_layout()
  png_filename = (f"{Report.evaluationItem[0]}_ID={idxNum}_{Report.plotNum}.png")
  plt.savefig(os.path.join(Report.png_path, png_filename))
  Report.png_paths.append(os.path.join(Report.png_path, png_filename))
  Report.plotNum += 1
  return figure

def EmsOosReport_main(Data, Config, Report):

  Report.reportName = "EMS_OOS_Report"

  # 各グラフに表示するタイトルの設定（この設定が配列の次元数１を決定する）
  Report.evaluationItem = ["EmsOos_State", "Ems_ssmPhase", "Ems_DebouncingTimer"]

  # 各グラフに表示する信号のリストを設定（この設定が配列の次元数２を決定する） 
  Report.plotList = np.empty((len(Report.evaluationItem)), dtype=object)

  # 各グラフに表示する信号のリストを設定（この設定が配列の次元数２を決定する）
  Report.plotList[0]=(["emsIsOos"])
  Report.plotList[1]=(["EmsStateMachines_ssmPhase"])
  Report.plotList[2]=(["EmsStateMachines_debouncingTimer"])
  # 各グラフに表示する信号の単位を設定（この設定が配列の次元数２を決定する）
  Report.plotUnit = (["-", "-", "s"])

  #  Reportを出力するフォルダーを設定(PNG)
  Report.reportPath = os.path.join(Config.execute_path, "report")
  Report.png_path = os.path.join(Report.reportPath, "png")
  os.makedirs(Report.reportPath, exist_ok=True)
  os.makedirs(Report.png_path, exist_ok=True)

  idx1 = 0
  idx2 = 32
  Report.stateChangeInvalid = np.empty(idx2, dtype=object)
  Report.stateChangeHealed = np.empty(idx2, dtype=object)
  Report.stateChangeList = np.empty(idx2, dtype=object)
  preProc.preProc_Common(Data, Config, Report, idx1, idx2)

  #  配列[0][0][0]が1へ変化した時のインデックスを取得
  Report.emsOosInvalid = findProgram.findChangePoint(Report.dataValue[0][0][0], 1)

  #  配列[0][0][0]が0へ変化した時のインデックスを取得
  Report.emsOosHealed  = findProgram.findChangePoint(Report.dataValue[0][0][0], 0)

  debug5 = Report.emsOosInvalid
  debug6 = Report.emsOosHealed

  #  構造体データの各IDに対して、配列[1][0][idxSource][idxNum]が変化した詩のインデックスを取得するため配列を確保
  for idxNum in range (idx1,idx2):
    Report.stateChangeInvalid[idxNum] = np.empty(len(Config.sourceList), dtype=object)
    Report.stateChangeHealed[idxNum] = np.empty(len(Config.sourceList), dtype=object)
    Report.stateChangeList[idxNum] = np.empty(len(Config.sourceList), dtype=object)


  # 構造体データの各IDに対して、配列[1][0][idxSource][idxNum]が変化した詩のインデックスを取得する 
  for idxNum in range(idx1, idx2):
    for idxSource in range(len(Config.sourceList)):
      Report.stateChangeInvalid[idxNum][idxSource] = findProgram.findChangePoint(Report.dataValue[1][0][idxSource][idxNum], "invalid")
      Report.stateChangeHealed[idxNum][idxSource] = findProgram.findChangePoint(Report.dataValue[1][0][idxSource][idxNum], "valid")
      Report.stateChangeList[idxNum][idxSource] = Report.stateChangeInvalid[idxNum][idxSource] + Report.stateChangeHealed[idxNum][idxSource]

      #  stateChangeInvalidとemsOosInvalidの両方に含まれるインデックスを取得し、共通するインデックスが存在する場合emsOosPlot_PreProc関数を呼び出す
      matchIdList_1 = [
          idx for idx in Report.stateChangeInvalid[idxNum][idxSource]
          if idx in Report.emsOosInvalid
      ]
      matchIdList_2 = [
          idx for idx in Report.stateChangeHealed[idxNum][idxSource]
          if idx in Report.emsOosHealed

      ]
      matchIdList = matchIdList_1 + matchIdList_2

      lenList = len(matchIdList)
      for idx in range(lenList):
        emsOosPlot_PreProc(Report, matchIdList, Report.stateChangeList[idxNum][idxSource], idxNum, idxSource)

