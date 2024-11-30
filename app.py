import streamlit as st
import pandas as pd
import seaborn as sns

fdf = pd.read_csv('A1CAP.csv')
# make a seaborn 2 lines for Real and Pred cols
fdf.plot(figsize=(30,10))

