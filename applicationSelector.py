
executionTarget = "EmsOos"
import textwrap

def setAplicationProgram(Data, Report, Config):
  executionProgram = executionTarget + "(Data, Report, Config)"
  exec(executionProgram)

def execAplicationProgram(mdf, Data, Report, Config):

  exec(Config.codeString)
 
def EmsOos(Data, Report, Config):

  Config.sourceData_Type  = "Original"        #[Simulation / Original]
  Config.mf4_file         = "/Users/u1_aida/Dev_Data/Tool_Dev/Oos_Test_RL"
  Config.Data_Dict        = "signalDataBase_EmsOos_s.csv"
  Config.Data_ListName    = "signalDataList_EmsOos_s.csv"
  Config.sourceList      = ["RadarRL"]

  codeString = """
  import emsOos.appendEmsOos as appendEmsOos
  import emsOos.emsOos_Report as EmsOos_Report
  appendEmsOos.generateDatData(mdf, Data.Data_m,Config)
  EmsOos_Report.EmsOosReport_main(Data, Config, Report)
  """
  Config.codeString = textwrap.dedent(codeString)
 
def main(mdf, Data, Report, Config):
  import system5_Direct as system5_Direct
  system5_Direct.main(Data, Report, Config)
