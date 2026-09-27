
executionTarget = "EmsOos"

def aplicationProgram(mdf, Data, Report, Config):
  executionProgram = executionTarget + "(mdf, Data, Report, Config)"
  exec(executionProgram)

def EmsOos(mdf, Data, Report, Config):
  import emsOos.appendEmsOos as appendEmsOos
  import emsOos.emsOos_Report as EmsOos_Report

  Config.sourceData_Type  = "Original"        #[Simulation / Original]
  Config.mf4_file         = "/Users/u1_aida/Dev_Data/Tool_Dev/Oos_Test_RL"
  Config.Data_Dict        = "signalDataBase_EmsOos_s.csv"
  Config.Data_ListName    = "signalDataList_EmsOos_s.csv"
  Config.sourceList      = ["RadarRL"]

  appendEmsOos.generateDatData(mdf, Data.Data_m,Config)
  EmsOos_Report.EmsOosReport_main(Data, Config, Report)

def main(mdf, Data, Report, Config):
  import system5_Direct as system5_Direct
  system5_Direct.main(Data, Report, Config)
