import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler


#set extension parameters
final_length = 50000    #length of extended temperature time series
trend_window = 10           #number of final years (of the prediction time series) from which to get average temperature trend (for extrapolation) 


# read PROVIDE data and select deciles
provide = pd.read_csv("tier1_temperature_summary.csv")
provide = provide.loc[(provide["quantile"] != 0.33) & (provide["quantile"] != 0.66)]
rows = len(provide)
provide.index = np.arange(0,rows,1)

# extend by linear extrapolation
provide_lastyear = int(provide.columns[-1])
provide_lasttemp = provide[str(provide_lastyear)]
min_temp = 0

provide_trend = (provide[str(provide_lastyear)] - provide[str(provide_lastyear-trend_window)])/trend_window
for i in np.arange(0, rows, trend_window-1):
    batch = provide_trend[i:i+trend_window-1]
    bmax = max(batch)
    bmin = min(batch)
    
    if bmin > 0:
        provide_trend[i:i+trend_window-1] = np.linspace(bmin, bmax, trend_window-1)

    elif bmax < 0:
        provide_trend[i:i+trend_window-1] = np.linspace(bmin, bmax, trend_window-1)

    else:
        provide_trend[i:i+trend_window-1] = np.zeros(trend_window-1)

provide_firstyear = int(provide.columns[2])
extension_lastyear = provide_firstyear + final_length - 1

extension_range = np.arange(provide_lastyear+1, extension_lastyear+1, 1)

extension = pd.concat([np.maximum(np.full(rows, min_temp), provide_lasttemp+provide_trend*(year-provide_lastyear)) for year in extension_range], axis=1, keys=[str(i) for i in extension_range])

# merge timeseries
provide_extension = pd.concat([provide, extension], axis=1)
provide_extension.to_csv(f"provide_extension_{provide_firstyear}-{extension_lastyear}.csv")

# select only non-runaway scenarios
provide_extension_filtered = provide_extension.loc[(provide_extension["scenario"] != "CurPol") & (provide_extension["scenario"] != "ModAct") & (provide_extension["scenario"] != "Ren_NZCO2")]
filtered_rows = len(provide_extension_filtered)
provide_extension_filtered.index = np.arange(0,filtered_rows,1)
provide_extension_filtered.to_csv(f"provide_extension_{provide_firstyear}-{extension_lastyear}_non-runaway.csv")

# read csv files (to avoid re-calculating extension)
provide_extension = pd.read_csv("provide_extension_1850-51849.csv")
provide_extension_filtered = pd.read_csv("provide_extension_1850-51849_non-runaway.csv")