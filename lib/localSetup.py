import os
import glob
import csv
import numpy as np
import pandas as pd

def LocalSetup(Config, local, report):
  # 各レポートの出力先を設定
  report.report_path = os.path.join(Config.execute_path, 'Report', Config.mf4_file_name)
  local.csv_path = os.path.join(report.report_path, 'csv')
  local.html_path = os.path.join(report.report_path, 'html')
  local.png_path = os.path.join(local.html_path, 'png')
  
  os.makedirs(local.csv_path, exist_ok=True)
  os.makedirs(local.html_path, exist_ok=True)
  os.makedirs(local.png_path, exist_ok=True)

  if (Config.multiPlot == True):
    report.multiPlot_report_path = os.path.join(Config.execute_path, 'Report', report.reportName)
    local.multiPlot_csv_path = os.path.join(report.multiPlot_report_path, 'csv')
    local.multiPlot_html_path = os.path.join(report.multiPlot_report_path, 'html')
    local.multiPlot_png_path = os.path.join(local.multiPlot_html_path, 'png')
    
    os.makedirs(local.multiPlot_csv_path, exist_ok=True)
    os.makedirs(local.multiPlot_html_path, exist_ok=True)
    os.makedirs(local.multiPlot_png_path, exist_ok=True)

def ConfigSetup(Config, local, report):
  # 各レポートの出力先を設定
  report.report_path = os.path.join(Config.execute_path, 'Report', report.reportName)
  Config.csv_path = os.path.join(report.report_path, 'csv')
  Config.html_path = os.path.join(report.report_path, 'html')
  Config.png_path = os.path.join(Config.html_path, 'png')
  
  os.makedirs(Config.csv_path, exist_ok=True)
  os.makedirs(Config.html_path, exist_ok=True)
  os.makedirs(Config.png_path, exist_ok=True)

