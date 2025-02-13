
require(dplyr)
require(tidyverse)


### SORTING OUT THE DATA

  names = c("simulation_length", "GIS_final_state", "THC_final_state", "WAIS_final_state", "AMAZ_final_state", "number_of_tippings", "GIS_tipped", "THC_tipped", "WAIS_tipped", "AMAZ_tipped")

  
  setwd("/no_feedbacks/") # insert path to result files

  list = list.files(recursive=T, pattern="0.txt")
  
  txt_data = (list %>%
                 map_dfc(read.table, row.names=names) %>%
                 t() %>%
                 as.data.frame() %>%
                 mutate_at(c(1:10), as.numeric) %>%
                 mutate(path = list,
                        any_tippings = ifelse(number_of_tippings>0, 1, 0)
                 )
  )

  path <- data.frame(path = list)
  
filename_data = ( path %>% rowwise() %>%
                    mutate(
                      filename = strsplit(as.character(path), "/"),
                      network = filename[1],
                      network_split = strsplit(network, "_"),
                      WAIS_to_THC = as.numeric(network_split[2]),
                      THC_to_AMAZ = as.numeric(network_split[3]),
                      couplings = gsub(pattern=".txt", replacement="", x=filename[3]),
                      couplings_split = strsplit(couplings, "_"),
                      coupling_strength = as.numeric(couplings_split[4]),
                      Tpeak = as.numeric(gsub(pattern="Tpeak", replacement="", x=couplings_split[3])),
                      scen_quant = strsplit(couplings_split[2], "_"),
                      quantile = as.numeric(str_sub(scen_quant, -3)),
                      scenario = str_sub(scen_quant, 1,-5)) %>%
                    select(-filename, -network_split, -network, -couplings_split, -scen_quant)
)



  results = (full_join(filename_data, txt_data) %>%
                group_by(scenario, quantile, coupling_strength, Tpeak) %>%
                summarise(count = n(),
                          any_tippings_prob = mean(any_tippings),
                          number_of_tippings_mean = mean(number_of_tippings),
                          number_of_tippings_sd = sd(number_of_tippings),
                          number_of_tippings_se = number_of_tippings_sd/sqrt(count),
                          GIS_tip_prob = mean(GIS_tipped),
                          THC_tip_prob = mean(THC_tipped),
                          WAIS_tip_prob = mean(WAIS_tipped),
                          AMAZ_tip_prob = mean(AMAZ_tipped)
                )
  )
  

setwd(" ") #insert path to main folder

temp = read.csv('Tconv450.csv')[-1]
#temp = read.csv('Tconv.csv')[-1] for long-term

  
final <- merge(results, temp)

write.csv(final, "results450.csv") #replace with "resultsLT.csv" for long-term
  
  