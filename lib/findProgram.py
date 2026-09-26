import numpy as np
import os
import glob

def findStandstill(Data, Config, report, targetSignal):

  lenSource = len(Config.sourceList)
  report.standstill_List = np.empty((lenSource), dtype=object)
  for idxSource in range (Config.lenSourceList):
    tarValue = getattr(Data, f'{targetSignal}_{Config.sourceList[idxSource]}').value

    # tarValueが0以外へ変化したインデックスを取得
    changeIndices = np.where((tarValue[:-1] == 0) & (tarValue[1:] != 0))[0] + 1
    report.standstill_List[idxSource] = changeIndices

def findDriveOff(Data, Config, report, targetSignal):
  for idxSource in range(Config.lenSourceList):
    idxList = []
    tarValue = getattr(Data, f'{targetSignal}_{Config.sourceList[idxSource]}').value
    tarTime = getattr(Data, f'{targetSignal}_{Config.sourceList[idxSource]}').time

    # tarValueが0へ変化したインデックスを取得
    changeIndices = np.where((tarValue[:-1] != 0) & (tarValue[1:] == 0))[0] + 1  # 変化点の次のインデックスを取得
    exec(f"report.driveOff_List_{Config.sourceList[idxSource]} = changeIndices")
    #report.driveOff_List[idxSource] = changeIndices

def findTargetSlot(Data, Config, report, targetSignal, targetSlot):
  report.slotBegin = np.empty((Config.lenSourceList), dtype=object)
  report.slotEnd = np.empty((Config.lenSourceList), dtype=object)
  tmpBegin = []
  tmpEnd = []
  for idxSource in range(Config.lenSourceList):
    slotBegin = []
    slotEnd = []
    for idx in range(len(report.evaluationItem) - 1):
      idxPlot = 0
      tarTime = report.dataTime[idx][0][idxSource]
      lenTime = len(tarTime)
      timeResolution = (tarTime[lenTime-1] - tarTime[0]) / (lenTime)
      harfSlot = int(targetSlot / timeResolution)
    for targetPoint in report.standstill_List[idxSource]:
      slotBegin.append(np.max([0, targetPoint - harfSlot]))
      slotEnd.append(np.min([lenTime - 1, targetPoint + harfSlot]))
    report.slotBegin[idxSource] = slotBegin
    report.slotEnd[idxSource] = slotEnd

def findChangePoint(currentState, targetState):
  lenData = len(currentState)
  changePoint_List = []
  for idx in range (1, lenData):
    try:
      if(targetState == currentState[idx].decode('utf-8') and targetState != currentState[idx-1].decode('utf-8')):
        changePoint_List.append(idx)
    except:
      if(targetState == currentState[idx] and targetState != currentState[idx-1]):
        changePoint_List.append(idx)
  return changePoint_List
