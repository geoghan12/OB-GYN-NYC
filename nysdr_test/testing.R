setwd("/Users/sophiegeoghan/Desktop/nysdr_test")

# GynoBK=read.csv("GynoBK.csv",col.names=c("Malpractice","Education","Name","Field"))
# GynoMan=read.csv("GynoMan.csv",col.names=c("Malpractice","Education","Name","Field"))
# 
# allNYS=read.csv("allNYC_obgyn_manhattan_sunPM.csv",col.names=c("Malpractice","boro","Education","Name","Field"))
# 
# kagglePhys=read.csv("Physician_Compare_National_Downloadable_File.csv")
# 
# ped2=read.csv("allNYS_ped_2.csv")
# ped1=read.csv("allNYS_ped_1.csv")
# obgyn=read.csv("allNYS_obgyn_1.csv")
library(wordcloud)


obgyn=read.csv("clean_obgyn_nyc.csv")
ob=data.frame(obgyn)
schools=unique(obgyn$School)

wordcloud(obgyn.School)
