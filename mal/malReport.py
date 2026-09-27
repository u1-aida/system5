import numpy as np
import csv
import os
import glob

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use('ggplot')
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

import Lib.localSetup as localSetup
import Lib.docProgram as docProgram
import Lib.preProc as preProc

#   クラスの定義
class Dat():
  pass

class DataClass():
  def __init__(self):
    self.value = ""
    self.time = ""


def dataPlot_Elevation(Data, Config, local, report):
  for idxSource in range(Config.lenSourceList):
    #figure = plt.figure(figsize=(16, 12))
    figure = plt.figure(figsize=(20, 12))
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
    # Overall figure title (use mf4 file name from Config)
    if (len(Config.sourceList) > 1):
      plotTitle = f'{Config.mf4_file_name}_{Config.sourceList[idxSource]}'
    else:
      plotTitle = f'{Config.mf4_file_name}'
    try:
      figure.suptitle(plotTitle, fontsize=14)
    except Exception:
      pass
    plotNum = 0
    for idxPlot in range(report.lenPlotList):
      tarFig = eval(f'fig_{plotNum}')
      max_Y = -999
      min_Y = 999
      for idxData in range(len(report.plotList[idxPlot])):
        tarPlotValue = report.dataValue[idxPlot][idxData][idxSource]
        tarPlotTime = report.dataTime[idxPlot][idxData][idxSource]

        min_X = tarPlotTime[0]
        max_X = tarPlotTime[len(tarPlotTime)-1 ]
        max_Y = max(np.nanmax(tarPlotValue), max_Y)      
        min_Y = min(np.nanmin(tarPlotValue), min_Y)
        maxData = max(tarPlotValue)
        minData = min(tarPlotValue)
        mean_Y = np.mean(tarPlotValue)
        print("MinSingle = ", minData, " MaxSingle = ", maxData, " MeanSingle = ", mean_Y)
        plotStep = 0.1
        while np.nanmax(tarPlotValue) >= max_Y:
          max_Y += plotStep
        while np.nanmin(tarPlotValue) <= min_Y:
          min_Y -= plotStep
        tarFig.plot(tarPlotTime, tarPlotValue, label=report.plotList[idxPlot][idxData])
        
      dataName = f'{report.titleList[plotNum]}'
      tarFig.set_title( f"{dataName}", fontsize=12, fontweight='regular')
      tarFig.set_xlim(min_X, max_X)
      tarFig.set_ylim(min_Y, max_Y)
      if(plotNum == (numPlotRow-1)):
        tarFig.set_xlabel('Time')
      tarFig.set_ylabel(report.plotUnit[idxPlot])

      tarFig.legend()
      tarFig.grid(color = 'black', linestyle = '--', linewidth = 0.5, axis='both')
      plotNum += 1

    if (len(Config.sourceList) > 1):
      png_filename = f'{Config.mf4_file_name}_{Config.sourceList[idxSource]}.png'
    else:
      png_filename = f'{Config.mf4_file_name}.png'

    plt.savefig(os.path.join(local.png_path, png_filename))
    report.png_paths.append(os.path.join(local.png_path, png_filename))
    report.plotNum += 1
    plt.close()

def plot_All(Data, Config, local,report):
  for idxSource in range(Config.lenSourceList):
    #figure = plt.figure(figsize=(16, 12))
    figure = plt.figure(figsize=(22, 5))
    numPlotCol = 1
    numPlotRow = 2
    lenData = numPlotRow * numPlotCol
    gs_master = GridSpec(nrows=numPlotRow, ncols=numPlotCol, hspace=0.4, wspace=0.15, left=0.08, right=0.95, top=0.925, bottom=0.05,height_ratios = [1, 1])
    axes = []
    for Col in range(numPlotCol):
      for Row in range(numPlotRow):
        if len(axes) >= lenData:
          break
        axes.append(figure.add_subplot(gs_master[Row, Col]))
      if len(axes) >= lenData:
        break

    fig_0, fig_1 = axes
    #try:
    #  figure.suptitle(f"{report.reportName}_{Config.sourceList[idxSource]}", fontsize=14)
    #except Exception:
    #  pass
    plotNum = 0
    for idxPlot in range(report.lenPlotList):
      tarFig = eval(f'fig_{plotNum}')
      max_Y = -999
      min_Y = 999
      for idxData in range(len(report.plotList[idxPlot])):
        tarPlotValue = Data.dataValue[idxPlot][idxData][idxSource]
        tarPlotTime = Data.dataTime[idxPlot][idxData][idxSource]

        min_X = tarPlotTime[0]
        max_X = tarPlotTime[len(tarPlotTime)-1 ]
        max_Y = max(np.nanmax(tarPlotValue), max_Y)      
        min_Y = min(np.nanmin(tarPlotValue), min_Y)
        maxData = max(tarPlotValue)
        minData = min(tarPlotValue)
        mean_Y = np.mean(tarPlotValue)
        print("Min = ", minData, " Max = ", maxData, " Mean = ", mean_Y)
        plotStep = 0.1
        if idxPlot in [0]:
          min_Y = -12.0
          max_Y = 12.0

        while np.nanmax(tarPlotValue) >= max_Y:
          max_Y += plotStep
        while np.nanmin(tarPlotValue) <= min_Y:
          min_Y -= plotStep
        tarFig.plot(tarPlotTime, tarPlotValue, label=report.plotList[idxPlot][idxData])
        
      dataName = f'{report.titleList[plotNum]}'
      tarFig.set_title( f"{dataName}", fontsize=12, fontweight='regular')
      tarFig.set_xlim(min_X, max_X)
      tarFig.set_ylim(min_Y, max_Y)
      if(plotNum == (numPlotRow-1)):
        tarFig.set_xlabel('Time')
      tarFig.set_ylabel(report.plotUnit[idxPlot])

      tarFig.legend()
      tarFig.grid(color = 'black', linestyle = '--', linewidth = 0.5, axis='both')
      plotNum += 1

    png_filename = f'{report.reportName}_{Config.sourceList[idxSource]}.png'
    plt.savefig(os.path.join(local.multiPlot_png_path, png_filename))
    report.png_paths.append(os.path.join(local.multiPlot_png_path, png_filename))
    report.plotNum += 1
    plt.close()

def postProc(Data, Config, report):
  for idxPlot in range(report.lenPlotList):
    for idxData in range(len(report.plotList[idxPlot])):
      for idxSource in range(Config.lenSourceList):
        if idxPlot in [0]:
          val = report.dataValue[idxPlot][idxData][idxSource]
          report.dataValue[idxPlot][idxData][idxSource] = np.array(val) * 180.0 / np.pi  # ラジアンを度に変換

def malReport_main(Data, Config, Report):
  local = Dat()
  Report.plotNum = 1
  Report.csv_paths = []
  Report.png_paths = []

  Report.reportName = "MAL_el_Report"

  Report.Evaluation_List = ["MAL_el_Indicator", "Vehicle Speed"]
  Report.titleList = ["Indicator", "Vehicle Speed"]

  Report.plotList = np.empty((len(Report.Evaluation_List)), dtype=object)

  #Report.plotList[0]=(["MAL_elOOS_outOfSpecCause"])
  #Report.plotList[1]=(["MAL_elOOS_stablePosition", "MAL_elComp_estimation", "MAL_elComp_meanVal"])
  Report.plotList[0]=(["MAL_elOOS_stablePosition", "MAL_AngleIndicator_el", "MAL_AngleIndicator_elMean"])
  Report.plotList[1] =(["EgoStateOut_vxVehRef"])
  #Report.plotList[4] =(["EgoStateOut_yawRate"])
  Report.plotUnit = (["deg","m/s"])

  Report.lenPlotList = len(Report.plotList)


  Report.lenEvaluationList = len(Report.Evaluation_List)
  Report.evalResult = np.empty((Report.lenEvaluationList), dtype=object)
  localSetup.LocalSetup(Config, local, Report)
  preProc.preProc_Single(Data, Config, Report)
  postProc(Data, Config, Report)
  preProc.preProc_Append(Data, Config, Report)
  dataPlot_Elevation(Data, Config, local, Report)
  if (Config.multiPlot == True):
    plot_All(Data, Config, local, Report)
  print("malReport_main finished")