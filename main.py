

# GOOGLE_CLIENT_ID= "351398082333-olmdonldfmsjgg8rri34cq73a43fqfdl.apps.googleusercontent.com"

# GOOGLE_CLIENT_SECRET="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"

from io import BytesIO
import logging
import flask
import json
import httplib2
import time
import webbrowser
import requests
import urllib.request
import pandas as pd
from datetime import datetime
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
import plotly
import plotly.express as px



app = flask.Flask(__name__)


CLIENT_ID = "351398082333-olmdonldfmsjgg8rri34cq73a43fqfdl.apps.googleusercontent.com"
CLIENT_SECRET = "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"

Sdate = str((datetime.now()).strftime("%Y-%m-%d"))

print(Sdate)

OAUTH_SCOPE = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.blood_glucose.read https://www.googleapis.com/auth/fitness.blood_pressure.read https://www.googleapis.com/auth/fitness.body_temperature.read https://www.googleapis.com/auth/fitness.location.read https://www.googleapis.com/auth/fitness.nutrition.read https://www.googleapis.com/auth/fitness.oxygen_saturation.read https://www.googleapis.com/auth/fitness.body.read https://www.googleapis.com/auth/fitness.reproductive_health.read'
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"


now = datetime.now()-timedelta(days=30)
to_day=(datetime.now())
print(to_day)
last_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
T_y_mid= int(time.mktime(last_day.timetuple())) * 1000000000
T_T_mid= int(time.mktime(to_day.timetuple())) * 1000000000
T_now= int(time.mktime(datetime.now().timetuple())) * 1000000000
DATA_SET = str(T_y_mid)+"-"+str(T_T_mid)
profile=None



REDIRECT_URI = 'http://127.0.0.1:3210/oauth2callback'

@app.route("/",methods=["GET","POST"])
def auth1():
	flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
	authorize_url = flow.step1_get_authorize_url()
	return flask.redirect(authorize_url)

@app.route("/oauth2callback",methods=["GET","POST"])
def assign():
  flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
  c = flask.request.args.get("code")
  code=c.strip()
  credentials = flow.step2_exchange(code)
  global profile
  profile=json.loads(credentials.to_json())["id_token"]
  http = httplib2.Http()
  http = credentials.authorize(http)
  fitness_service = build('fitness', 'v1', http=http)
  weightData=fetchData("derived:com.google.weight:com.google.android.gms:merge_weight",fitness_service)
  saveSpeed(weightData,'Weight')
  calories=fetchData('derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',fitness_service)
  saveSpeed(calories,'Calories')
  dist=fetchData('derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',fitness_service)
  saveSpeed(dist,'Distance')
  heightData=fetchData("derived:com.google.height:com.google.android.gms:merge_height",fitness_service)
  saveSpeed(heightData,'Height')
  heartData=fetchData('derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes',fitness_service)
  saveSpeed(heartData,'Heart')
  locationData=fetchData('derived:com.google.location.sample:com.google.android.gms:merge_location_samples',fitness_service)
  saveData(locationData,'Location.txt')
  speedData=fetchData("derived:com.google.speed:com.google.android.gms:merge_speed",fitness_service)
  saveSpeed(speedData,'Speed')
  activityData=fetchData("derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments",fitness_service)
  saveActivity(activityData,'Activity')
  steps=fetchData(DATA_SOURCE,fitness_service)
  saveActivity(steps,'Steps')
  stps="Data Cleared..."
  return flask.redirect(flask.url_for('homepage'))



@app.route("/homepage/",methods=["POST","GET"])
def homepage():
  day=0
  if(flask.request.method=="POST"):
    day=int(flask.request.form.get("days"))
    print(day)
  return flask.render_template("homepage.html",data=[
                                data_process('Steps')[day],
						   	    round(data_process('Distance')[day]/1000,4),
							    round(data_process('Calories')[day],12),
							    data_process('Heart')[day],
							   profile['name'],
							   profile['picture']
							   
							   
							   
 ])


@app.route("/homepage/overview",methods=["POST","GET"])
def overview():
  day=0
  if(flask.request.method=="POST"):
    day=int(flask.request.form.get("days"))
    print(day)
  return flask.render_template("homepage.html",data=[
                                data_process('Steps')[day],
						   	    round(data_process('Distance')[day]/1000,4),
							    round(data_process('Calories')[day],12),
							    data_process('Heart')[day],
							   profile['name'],
							   profile['picture']
							   
							   
							   
 ])




@app.route("/homepage/timer")
def timer_page():
     return flask.render_template("timer.html")




@app.route("/homepage/detailed")
def detailed():
     return flask.render_template("pixela.html",graphJSON=[graph_generator('Distance','blueviolet'),graph_generator('Steps','white'),graph_generator('Heart','pink'),graph_generator("Calories",'yellow')])
     




def nanoseconds(nanotime):
    dt = datetime.fromtimestamp(nanotime // 1000000000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def saveData(data,path):
	with open('./data/'+path, 'w') as inputfile:
		json.dump(data, inputfile)
	pass



def fetchData(dataStreamId,fitness_service):
	dist=fitness_service.users().dataSources().datasets().get(userId='me', dataSourceId=dataStreamId, datasetId=DATA_SET).execute()
	return dist


def saveActivity(activityData,path):
	S_time,E_time,Type=[],[],[]
	stps={}
	for i in range(len(activityData["point"])):
		last_point = activityData["point"][i]
		S_time.append(nanoseconds(int(last_point.get("startTimeNanos", 0))))
		E_time.append(nanoseconds(int(last_point.get("endTimeNanos", 0))))
		Type.append(last_point["value"][0].get("intVal", None))
		stps.update({last_point["value"][0].get("intVal", None):[nanoseconds(int(last_point.get("startTimeNanos", 0))),nanoseconds(int(last_point.get("endTimeNanos", 0)))]})
	adf = pd.DataFrame({'Start Time':S_time,'End Time':E_time,path:Type})
	adf.to_csv('./data/'+path+' '+Sdate+'.csv', columns=['Start Time','End Time',path], header=True,index = False)
	with open('./data/json/'+path+" "+Sdate+'.json', 'w') as outfile:
		json.dump(stps,outfile)

def saveSpeed(speedData,path):
  S_time,E_time,Speed=[],[],[]
  stps={}
  for i in range(len(speedData["point"])):
    last_point = speedData["point"][i]
    S_time.append(nanoseconds(int(last_point.get("startTimeNanos", 0))))
    E_time.append(nanoseconds(int(last_point.get("endTimeNanos", 0))))
    Speed.append(last_point["value"][0].get("fpVal", None))
    stps.update({last_point["value"][0].get("fpVal", None):[nanoseconds(int(last_point.get("startTimeNanos", 0))),nanoseconds(int(last_point.get("endTimeNanos", 0)))]})
  adf = pd.DataFrame({'Start Time':S_time,'End Time':E_time,path:Speed})
  adf.to_csv('./data/'+path+' '+Sdate+'.csv', columns=['Start Time','End Time',path], header=True,index = False)
  with open('./data/json/'+path+" "+Sdate+'.json', 'w') as outfile:
  	json.dump(stps,outfile)
	





def data_process(path):
    try:
        paths='./data/'+path+' '+Sdate+'.csv'
        db=pd.read_csv(paths)
        db["Start Time"]=pd.to_datetime(db["Start Time"]).dt.date
        db=db.groupby("Start Time").sum()
    except:
        _30="Data Unavailable"
        _7="Data Unavailable"
        _1="Data Unavailable"

    try:
        _30=db[path].sum()
        print(_30)
    except:
        _30="Data Unavailable"


    try:
        _7_1=0
        for i in range(-7,0):
            _7_1+=db[path][i]
        _7=_7_1
    except:
        _7="Data Unavailable"
        _30="Data Unavailable"



    try:
        _1=db[path][-1]
    except:
        _1="Data Unavailable"

    return [_1,_7,_30]

	
def graph_generator(path,color):
    paths='./data/'+path+' '+Sdate+'.csv'
    db=pd.read_csv(paths)
    db["Start Time"]=pd.to_datetime(db["Start Time"]).dt.date
    db=db.groupby("Start Time").sum()
    fig=px.bar(db,barmode='group',y=path,title=path)
    fig.update_layout(
         {
              'showlegend':False,
              'title_font_size':23,
              'font_family':'Poppins',
        'font_color':'rgb(240, 248, 255)',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'modebar_bgcolor':'rgb(240, 248, 255)',
        'bargap':0.3
        }
        )
    fig.update_traces(marker_color=str(color),marker_line_width=0)
    graphJSON=json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == "__main__":
	app.debug=True
	app.run(port=3210)
	
	
	print("Starting API services")
