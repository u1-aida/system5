import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

from asammdf import MDF
class Dat():
  pass

class DataClass():
  def __init__(self):
    self.value = ""
    self.time = ""

def get_sensor_data(mdf, sourceChannel, signal_name):
  try:
    for entry in mdf.channels_db[signal_name]:
      (group_index, channel_index) = entry
      ch = mdf.groups[group_index].channels[channel_index]
      cg = mdf.groups[group_index].channel_group
          
      source = ch.source or getattr(cg, "acq_source", None)
      try:
        sourceName = ch.source.name
      except:
        sourceName = None
      if ((source.path == sourceChannel) or (sourceName == sourceChannel)):
        return mdf.get(group=group_index, index=channel_index).samples
  except:
    print("No data found [", signal_name, " ]")
    return [0]
          
def get_sensor_time(mdf, sourceChannel, signal_name):
  try:
    for entry in mdf.channels_db[signal_name]:
      (group_index, channel_index) = entry
      ch = mdf.groups[group_index].channels[channel_index]
      cg = mdf.groups[group_index].channel_group
              
      source = ch.source or getattr(cg, "acq_source", None)
      try:
        sourceName = ch.source.name
      except:
        sourceName = None
      if ((source.path == sourceChannel) or (sourceName == sourceChannel)):
        return mdf.get(group=group_index, index=channel_index).timestamps
  except:
    print("No data found [", signal_name, " ]")
    return [0]
          
def get_Data_old(mdf, Data, Config_Cmn, Config_loc, signal_name):
  # source => Config.sourceChannelに最適化
  try:
    signal_name = signal_name.strip()  # 余分な空白を削除

    debug_2 = signal_name
    debug_3 = Config_Cmn.signalDataBaseList.index[Config_Cmn.signalDataBaseList['ShortName'] == signal_name]
    debug_4 = [signal_name].tolist()

    idx = Config_loc.signalDataBaseList.index[Config_loc.signalDataBaseList['ShortName'] == signal_name].tolist()[0]
    signal_original = Config_loc.signalDataBaseList['OriginalName'][idx].lstrip()
    #if(Config.sourceData_Type == "Selena"):
    #signal_original = "_" + signal_original
    try:
      signal_calc = Config_loc.signalDataBaseList['Normalization'][idx].lstrip()
    except:
      pass
    exec(f"Data.{signal_name}_{Config_Cmn.sourceChannel} = DataClass()")
    # 修正: exec内でsignal_originalが文字列として扱われてしまうため、f-stringで展開
    exec(f"Data.{signal_name}_{Config_Cmn.sourceChannel}.time = get_sensor_time(mdf, Config_Cmn.sourceChannel ,signal_original)")
    exec(f"Data.{signal_name}_{Config_Cmn.sourceChannel}.value = get_sensor_data(mdf, Config_Cmn.sourceChannel ,signal_original)")
    try:
      Process = f'Data.{signal_name}_{Config_Cmn.sourceChannel}.value = np.array(Data.{signal_name}_{Config_Cmn.sourceChannel}.value){signal_calc}'
    except:
      Process = f'Data.{signal_name}_{Config_Cmn.sourceChannel}.value = np.array(Data.{signal_name}_{Config_Cmn.sourceChannel}.value)'
    try:
      exec(Process)
    except:
      pass
  except:
    print("No data found [", signal_name, " ]")

  return Data  # 見つからなかった場合

def get_Data(mdf, Data, Config, signal_name):
  # source => Config.sourceChannelに最適化
  try:
    signal_name = signal_name.strip()  # 余分な空白を削除


    idx = Config.signalDataBaseList.index[Config.signalDataBaseList['ShortName'] == signal_name].tolist()[0]
    signal_original = Config.signalDataBaseList['OriginalName'][idx].lstrip()
    signal_original = signal_original.strip()  # 余分な空白を削除

    try:
      signal_calc = Config.signalDataBaseList['Normalization'][idx].lstrip()
    except:
      pass
    sourceChannel = Config.sourceChannel
    try:
      exec(f"Data.{signal_name}_{sourceChannel} = DataClass()")
    except:
      sourceChannel = Config.sourceChannel.split("::", 1)[1] if "::" in Config.sourceChannel else Config.sourceChannel
      exec(f"Data.{signal_name}_{sourceChannel} = DataClass()")

    # 修正: exec内でsignal_originalが文字列として扱われてしまうため、f-stringで展開
    exec(f"Data.{signal_name}_{sourceChannel}.time = get_sensor_time(mdf, Config.sourceChannel ,signal_original)")
    exec(f"Data.{signal_name}_{sourceChannel}.value = get_sensor_data(mdf, Config.sourceChannel ,signal_original)")

    try:
      Process = f'Data.{signal_name}_{Config.sourceChannel}.value = np.array(Data.{signal_name}_{Config.sourceChannel}.value){signal_calc}'
    except:
      Process = f'Data.{signal_name}_{Config.sourceChannel}.value = np.array(Data.{signal_name}_{Config.sourceChannel}.value)'
    try:
      exec(Process)
    except:
      pass
  except:
    print("No data found [", signal_name, " ]")

  return Data  # 見つからなかった場合

def get_SingleData(mdf, Data, Config, signalDataBaseList, signal_name_org):
  for row in signalDataBaseList:
    if row[0] == signal_name_org:
      signal_original_1 = row[1].lstrip()  # 2列目（時間信号名）を返す
      signal_original_2 = row[2].lstrip()  # 2列目（時間信号名）を返す
      signal_original_1 = signalDataBaseList['OriginalName_1'][idx].lstrip()
      signal_original_2 = signalDataBaseList['OriginalName_2'][idx].lstrip()

      signal_original = signal_original_1 + ".i" +str(Config.targetIdx) + "." + signal_original_2
      #signal_name = signal_name_org + "_i" + str(Config.targetIdx)
      signal_name = signal_name_org
      try:
        signal_calc = row[2]
      except:
        pass
      exec(f"Data.{signal_name} = DataClass()")
      # 修正: exec内でsignal_originalが文字列として扱われてしまうため、f-stringで展開
      exec(f"Data.{signal_name}.time = get_sensor_time(mdf, Config.sourceChannel,signal_original)")
      exec(f"Data.{signal_name}.value = get_sensor_data(mdf, Config.sourceChannel,signal_original)")
      try:
        Process = f'Data.{signal_name}.value = np.array(Data.{signal_name}.value){signal_calc}'
      except:
        Process = f'Data.{signal_name}.value = np.array(Data.{signal_name}.value)'
      try:
        exec(Process)
      except:
        pass

  return Data  # 見つからなかった場合

def get_MultiData(mdf, Data, sourceChannel, signalDataBaseList, signal_name_org, idx1, idx2):
  for row in signalDataBaseList:
    debug_1 = row
    debug_2 = signal_name_org
    #debug_3 = signalDataBaseList.index[signalDataBaseList['ShortName']]
    #debug_4 = [signal_name_org].tolist()
    #idx = signalDataBaseList.index[signalDataBaseList['ShortName'] == signal_name_org].tolist()[0]
    if row[0] == signal_name_org:
      for i in range(idx1,idx2):
        signal_original_1 = row[1].lstrip()  # 2列目（時間信号名）を返す
        signal_original_2 = row[2].lstrip()  # 2列目（時間信号名）を返す
        signal_original = signal_original_1 + "[" +str(i) + "]." + signal_original_2
        #(signal_original)
        signal_name = signal_name_org + "_i" + str(i)
        try:
          signal_calc = row[2]
        except:
          pass
        exec(f"Data.{signal_name}_{sourceChannel} = DataClass()")
        # 修正: exec内でsignal_originalが文字列として扱われてしまうため、f-stringで展開
        exec(f"Data.{signal_name}_{sourceChannel}.time = get_sensor_time(mdf, sourceChannel,signal_original)")
        exec(f"Data.{signal_name}_{sourceChannel}.value = get_sensor_data(mdf, sourceChannel,signal_original)")
        try:
          Process = f'Data.{signal_name}_{sourceChannel}.value = np.array(Data.{signal_name}_{sourceChannel}.value){signal_calc}'
        except:
          Process = f'Data.{signal_name}_{sourceChannel}.value = np.array(Data.{signal_name}_{sourceChannel}.value)'
        try:
          exec(Process)
        except:
          pass

  return Data  # 見つからなかった場合

