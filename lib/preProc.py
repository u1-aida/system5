import numpy as np
import csv
import os
import glob

def preProc_Common(Data, Config, report, idx1, idx2):
  # 構造体の構成 [Plot位置][プロットデータ番号][ソース番号] -> 各要素は時系列 t の配列
  lenPlotList = len(report.plotList)
  report.dataValue = np.empty(lenPlotList, dtype=object)
  report.dataTime = np.empty(lenPlotList, dtype=object)
  for idxPlot in range(lenPlotList):
    # Subplotに対応した分の配列を確保
    report.dataValue[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    report.dataTime[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    for idxData in range(len(report.plotList[idxPlot])):
      report.dataValue[idxPlot][idxData] = np.empty(len(Config.sourceList), dtype=object)
      report.dataTime[idxPlot][idxData] = np.empty(len(Config.sourceList), dtype=object)
      # 各プロットデータに対応した分の配列を確保
      tarItem = report.plotList[idxPlot][idxData]
      for idxSource in range(Config.lenSourceList):
        # tarItem が DataList のどちらのリストに含まれるか判定
        try:
          if hasattr(Config, 'DataList'):
            if hasattr(Config.DataList, 'list_M') and tarItem in Config.DataList.list_M:
              #debug = len(report.plotList[idxPlot])
              #for idxData in range(len(report.plotList[idxPlot])):
                #print(idxData)
                report.dataValue[idxPlot][idxData][idxSource] = np.empty(idx2, dtype=object)
                report.dataTime[idxPlot][idxData][idxSource] = np.empty(idx2, dtype=object)
                #for idxSource in range(Config.lenSourceList):
                for idxNum in range (idx1,idx2):
                  report.dataValue[idxPlot][idxData][idxSource][idxNum] = np.empty(len(Config.sourceList), dtype=object)
                  report.dataTime[idxPlot][idxData][idxSource][idxNum] = np.empty(len(Config.sourceList), dtype=object)
            else:
              print("Single data")
        except Exception:
          # 判定に失敗した場合は既定の False を維持
          pass

  for idxPlot in range(lenPlotList):
    for idxData in range(len(report.plotList[idxPlot])):
      tarItem = report.plotList[idxPlot][idxData]
      for idxSource in range(Config.lenSourceList):
        # tarItem が DataList のどちらのリストに含まれるか判定
        try:
          if hasattr(Config, 'DataList'):
            if hasattr(Config.DataList, 'list_M') and tarItem in Config.DataList.list_M:
              report.sourceChannel = Config.sourceList[idxSource]
              for idxNum in range (idx1,idx2):
                debug0 = report.sourceChannel
                debug1 = idxData
                debug2 = (f"Data_m.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
                try:
                  val  = eval(f"Data.Data_m.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
                  time = eval(f"Data.Data_m.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.time")
                except:
                  try:
                    report.sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
                    val  = eval(f"Data.Data_m.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
                    time = eval(f"Data.Data_m.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.time")
                  except:
                    pass
                try:
                  val = np.array(val)
                  report.dataValue[idxPlot][idxData][idxSource][idxNum] = val
                  report.dataTime [idxPlot][idxData][idxSource][idxNum] = time
                except:
                  pass
            else:
              report.sourceChannel = Config.sourceList[idxSource]
              debug0 = report.sourceChannel
              debug1 = idxData
              debug2 = (f"Data_s.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.value")
              try:
                val  = eval(f"Data.Data_s.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.value")
                time = eval(f"Data.Data_s.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.time")
              except:
                try:
                  report.sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
                  val  = eval(f"Data.Data_s.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.value")
                  time = eval(f"Data.Data_s.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.time")
                except:
                  pass
              try:
                val = np.array(val)
                report.dataValue[idxPlot][idxData][idxSource] = val
                report.dataTime [idxPlot][idxData][idxSource] = time
              except:
                pass

        except Exception:
          # 判定に失敗した場合は既定の False を維持
          pass


def preProc_Single(Data, Config, report):
  # 構造体の構成 [Plot位置][プロットデータ番号][ソース番号] -> 各要素は時系列 t の配列
  report.report_s.dataValue = np.empty(report.lenPlotList, dtype=object)
  report.report_s.dataTime = np.empty(report.lenPlotList, dtype=object)
  for idxPlot in range(report.lenPlotList):
    report.report_s.dataValue[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    report.report_s.dataTime[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    for idxData in range(len(report.plotList[idxPlot])):
      report.report_s.dataValue[idxPlot][idxData] = np.empty(len(Config.sourceList), dtype=object)
      report.report_s.dataTime[idxPlot][idxData] = np.empty(len(Config.sourceList), dtype=object)

  for idxPlot in range(report.lenPlotList):
    for idxData in range(len(report.plotList[idxPlot])):
      for idxSource in range(Config.lenSourceList):
        report.sourceChannel = Config.sourceList[idxSource]
        debug = report.sourceChannel
        try:
          val  = eval(f"Data.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.value")
          time = eval(f"Data.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.time")
        except:
          try:
            report.sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
            val  = eval(f"Data.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.value")
            time = eval(f"Data.{report.plotList[idxPlot][idxData]}_{report.sourceChannel}.time")
          except:
            pass
        try:
          val = np.array(val)
          report.report_s.dataValue[idxPlot][idxData][idxSource] = val
          report.report_s.dataTime [idxPlot][idxData][idxSource] = time
        except:
          pass

def preProc_Append(Data, Config, report):
  if(len(Data.dataValue) == 0):
    Data.dataValue = report.dataValue
    Data.dataTime = report.dataTime
    debug1 = len(Data.dataTime[0][0][0])
  else:
    debug2 = len(Data.dataTime[0][0][0])
    for idxPlot in range(report.lenPlotList):
      for idxData in range(len(report.plotList[idxPlot])):
        for idxSource in range(Config.lenSourceList):
          Data.dataValue[idxPlot][idxData][idxSource] = np.concatenate([Data.dataValue[idxPlot][idxData][idxSource], report.dataValue[idxPlot][idxData][idxSource]])
          currentLength = len(Data.dataTime[idxPlot][idxData][idxSource]) - 1
          currentDataTime = Data.dataTime[idxPlot][idxData][idxSource][currentLength]
          currentTime = report.dataTime[idxPlot][idxData][idxSource][0]
          if(currentTime < (currentDataTime + 1.0)):
            timeOffset = currentDataTime - currentTime + 0.001
            report.dataTime[idxPlot][idxData][idxSource] = report.dataTime[idxPlot][idxData][idxSource] + timeOffset
          Data.dataTime[idxPlot][idxData][idxSource] = np.concatenate([Data.dataTime[idxPlot][idxData][idxSource], report.dataTime[idxPlot][idxData][idxSource]])
    #print("debug2 = ", debug2)

def preProc_Multi(Data, Config, report, idx1, idx2):
  # 構造体の構成 [Plot位置][プロットデータ番号][ソース番号] -> 各要素は時系列 t の配列
  # Plot Windowの数だけ、プロットデータ番号を持つ
  report.report_m.dataValue = np.empty(report.lenPlotList, dtype=object)
  report.report_m.dataTime = np.empty(report.lenPlotList, dtype=object)
  for idxPlot in range(report.lenPlotList):
    # 各Plot Windowひ表樹するデータ分の配列を確保
    report.report_m.dataValue[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    report.report_m.dataTime[idxPlot] = np.empty(len(report.plotList[idxPlot]), dtype=object)
    for idxData in range(len(report.plotList[idxPlot])):
      report.report_m.dataValue[idxPlot][idxData] = np.empty(idx2, dtype=object)
      report.report_m.dataTime[idxPlot][idxData] = np.empty(idx2, dtype=object)
      #for idxSource in range(Config.lenSourceList):
      for idxNum in range (idx1,idx2):
        report.report_m.dataValue[idxPlot][idxData][idxNum] = np.empty(len(Config.sourceList), dtype=object)
        report.report_m.dataTime[idxPlot][idxData][idxNum] = np.empty(len(Config.sourceList), dtype=object)

  for idxPlot in range(report.lenPlotList):
    for idxData in range(len(report.plotList[idxPlot])):
      for idxNum in range (idx1, idx2):
        for idxSource in range(Config.lenSourceList):
          report.sourceChannel = Config.sourceList[idxSource]
          debug = report.sourceChannel
          try:
            val  = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
            time = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.time")
          except:
            try:
              report.sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
              val  = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
              time = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.time")
            except:
              pass
          try:
            report.sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
            val  = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.value")
            time = eval(f"Data.{report.plotList[idxPlot][idxData]}_i{idxNum}_{report.sourceChannel}.time")
          except:
            pass
          try:
            val = np.array(val)
            report.report_m.dataValue[idxPlot][idxData][idxNum][idxSource] = val
            report.report_m.dataTime [idxPlot][idxData][idxNum][idxSource] = time
          except:
            pass

