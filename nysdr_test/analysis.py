#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:13:34 2018

@author: sophiegeoghan
"""

# testing working with scraped data:
import numpy as np
import pandas as pd

df=pd.read_csv("GynoBK.csv",header=None)
df.columns=["Malpractice","Education","Name","Specialty"]
df.head()