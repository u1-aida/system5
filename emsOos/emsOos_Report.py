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

def emsOosPlot_PreProc(Report, idxNum, idxSource):
  lenData = len(Report.stateChangeInvalid[idxNum][idxSource])
  for idx in range(lenData):
    pos = Report.stateChangeInvalid[idxNum][idxSource][idx]
    posBegin = max(0, pos - 10)
    posEnd = min(len(Report.dataValue[0][0][idxSource][idxNum]) - 1, pos + 10)
    emsOosPlot_1(Report, idxNum, idxSource, posBegin, posEnd)

def emsOosPlot_1 (Report, idxNum, idxSource, posBegin, posEnd):
  figure = plt.figure(figsize=(16, 9))
  numPlotCol = 1
  numPlotRow = 2
  lenData = numPlotRow * numPlotCol
  gs_master = GridSpec(nrows=numPlotRow, ncols=numPlotCol, hspace=0.4, wspace=0.15, left=0.08, right=0.95, top=0.93, bottom=0.05,height_ratios = [1, 1])
  axes = []
  for Col in range(numPlotCol):
    for Row in range(numPlotRow):
      if len(axes) >= lenData:
        break
      axes.append(figure.add_subplot(gs_master[Row, Col]))
    if len(axes) >= lenData:
      break

  fig_0, fig_1 = axes
  fig_0.plot(Report.dataTime[0][0][idxSource][idxNum][posBegin:posEnd], Report.dataValue[0][0][idxSource][idxNum][posBegin:posEnd])
  fig_0.plot(Report.dataTime[0][1][idxSource][posBegin:posEnd], Report.dataValue[0][1][idxSource][posBegin:posEnd])
  #fig_0.set_title(f"Phase: {Report.dataValue[0][0][idxSource][idxNum][posBegin:posEnd]}")
  fig_0.set_title(Report.evaluationItem[0])
  fig_1.plot(Report.dataTime[1][0][idxSource][idxNum][posBegin:posEnd], Report.dataValue[1][0][idxSource][idxNum][posBegin:posEnd])
  #fig_1.set_title(f"Debouncing Timer: {Report.dataValue[1][0][idxSource][idxNum][posBegin:posEnd]}")
  fig_1.set_title(Report.evaluationItem[1])
  plt.tight_layout()
  plt.show()
  return figure

def EmsOosReport_main(Data, Config, Report):
  local = Dat()
  Report.plotNum = 1
  Report.csv_paths = []
  Report.png_paths = []

  Report.reportName = "EMS_OOS_Report"

  Report.evaluationItem = ["EmsOos_State", "Ems_DebounceTimer"]

  Report.plotList = np.empty((len(Report.evaluationItem)), dtype=object)

  Report.plotList[0]=(["EmsStateMachines_ssmPhase", "emsIsOos"])
  Report.plotList[1]=(["EmsStateMachines_debouncingTimer"])
  Report.plotUnit = (["-", "-"])

  Report.lenPlotList = len(Report.plotList)
  Report.lenEvaluationList = len(Report.evaluationItem)
  Report.evalResult = np.empty((Report.lenEvaluationList), dtype=object)
  Report.lenTotalData = np.empty(Report.lenPlotList)
  #ocalSetup.LocalSetup(Config, local, Report)
  idx1 = 0
  idx2 = 32
  Report.stateChangeInvalid = np.empty(idx2, dtype=object)
  Report.stateChangeHealed = np.empty(idx2, dtype=object)
  preProc.preProc_Common(Data, Config, Report, idx1, idx2)
  Report.emsOosInvalid = findProgram.findChangePoint(Report.dataValue[0][1][0], 1)
  Report.emsOosHealed  = findProgram.findChangePoint(Report.dataValue[0][1][0], 0)

  print(Report.emsOosInvalid)
  for idxNum in range (idx1,idx2):
    Report.stateChangeInvalid[idxNum] = np.empty(len(Config.sourceList), dtype=object)
    Report.stateChangeHealed[idxNum] = np.empty(len(Config.sourceList), dtype=object)

  for idxNum in range(idx1, idx2):
    for idxSource in range(len(Config.sourceList)):
      Report.stateChangeInvalid[idxNum][idxSource] = findProgram.findChangePoint(Report.dataValue[0][0][idxSource][idxNum], "invalid")
      Report.stateChangeHealed[idxNum][idxSource] = findProgram.findChangePoint(Report.dataValue[0][0][idxSource][idxNum], "valid")
      if(len(Report.stateChangeInvalid[idxNum][idxSource]) > 0):
        emsOosPlot_PreProc(Report, idxNum, idxSource)
