from flask import Flask, json, jsonify, request, make_response, abort, render_template
import csv

app = Flask(__name__)

#Open CSV file
csvFile = open('/var/www/FlaskApps/PlagiarismDefenderApp/daily.csv','r')
#Reading CSV file
csvReader=csv.DictReader(csvFile)
#Converting CSV to JSON
jsonOutput = json.dumps([row for row in csvReader])
#Loading JSON data
jsonData = json.loads(jsonOutput)

#Definition for default page
@app.route('/', methods=['GET'])
def index():
   return jsonify({'Message' : 'Hola! You have reached Paramaiah Chandu\'s project'})

#Definition for WebPage.html
@app.route('/forecast/')
def WebPage():
   return render_template('WebPage.html')

#Definition for Forecasting temperature
@app.route('/forecast/<userDate>/', methods=['GET'])
def forecast_data(userDate):
 outputObject = []
 tmax = []
 tmin = []
 date = []

 for year in range(2013, 2018):
  for i in range(0,len(jsonData)):
   if jsonData[i]['DATE'] == str(year) + str(userDate)[4:]:
      userYear = str(userDate)[:4]

      for j in range(0, 7):
       if year == 2013:
          date.append(userYear + jsonData[i + j]['DATE'][4:])
          tmax.append(float(jsonData[i + j]['TMAX']))
          tmin.append(float(jsonData[i + j]['TMIN']))
       else:
          tmax[j] += float(jsonData[i + j]['TMAX'])
          tmin[j] += float(jsonData[i + j]['TMIN'])

 tmax[:] = [x/5 for x in tmax]
 tmin[:] = [y/5 for y in tmin]

 for i in range(0, 7):
    outputObject.append({"DATE":date[i], "TMAX":str(tmax[i]), "TMIN":str(tmin[i])})

 return json.dumps(outputObject)


if __name__ == '__main__':
    app.run(debug = True)
