import numpy as np
import os
import pandas as pd
from pandas import DataFrame
import glob
import re

#import csv file with all scenarios for long-term run

path = '.' #insert path

os.chdir(path)
data = pd.read_csv('provide_extension_1850-51849_non-runaway.csv', index_col=[0])
#data.drop(['Unnamed: 0.1'], axis=1, inplace=True)
data


#import csv file with all scenarios for medium-term run

os.chdir(path)
data450 = pd.read_csv('tier1_temperature_summary.csv')
#data450.drop(['Unnamed: 0.1'], axis=1, inplace=True)
data450


#rename scenarios
data.scenario = [i.replace("_", "-") for i in data.scenario]
scenarios = pd.unique(data.scenario).tolist()


#rename scenarios
data450.scenario = [i.replace("_", "-") for i in data450.scenario]
scenarios = pd.unique(data450.scenario).tolist()


subset = ['GS-NZGHG', 'Neg-NZGHG', 'SP-NZGHG', 'ssp119', 'ssp534-over', 'Ref-1p5',
          'CurPol-OS-1.5C', 'ModAct-OS-1C', 'Neg-OS-0C', 'ModAct-OS-1.5C']

#narrow dataframes to selected scenarios
selection = data.loc[data.scenario.isin(subset)]
selection450 = data450.loc[data450.scenario.isin(subset)]
selection450 = selection450[selection450["quantile"] != 0.33]
selection450 = selection450[selection450["quantile"] != 0.66]

#extract convergence temperature
Tconv450 = selection450[["scenario", "quantile", "2300"]]
Tconv450 = Tconv450.rename({'2300': 'Tconv'}, axis=1)
Tconv450.to_csv("Tconv450.csv")
Tconv = selection[["scenario", "quantile", "51849"]]
Tconv = Tconv.rename({'51849': 'Tconv'}, axis=1)
Tconv.to_csv("Tconv.csv")

os.mkdir("files")

# save
save_scenario = {}
for i in range(len(selection)):
    print(i)
    selection.iloc[i, 2:]
    save_scenario = ("files/_{}_{}_Tlim{:.2f}_Tpeak{:.2f}.txt".format(selection.iloc[i, 0], 
                                                                      selection.iloc[i, 1], 
                                                                      selection.iloc[i, -1], 
                                                                      selection.max(axis=1).iloc[i]))
    np.savetxt(save_scenario, selection.iloc[i, 2:])