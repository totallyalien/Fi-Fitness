import pandas as pd
import plotly
import plotly.express as px
import json


db=pd.read_csv(r"C:\Users\trex4\OneDrive\Desktop\fitness website\data\Distance 2023-05-26.csv")
db["Start Time"]=pd.to_datetime(db["Start Time"]).dt.date
db=db.groupby("Start Time").sum()
fig=px.bar(db,barmode='group')
graphJSON=json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

print(db.head())