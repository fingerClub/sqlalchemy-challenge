# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurment = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
lastYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#return list of available routes
@app.route("/")
def home():
    return (f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/insertStart<br/>"
            f"/api/v1.0/insertStart/insertEnd"
    )

#return last 12 months of precipitation
@app.route("/api/v1.0/precipitation")
def get_rain():
    rain = session.query(measurment.date, measurment.prcp).filter(measurment.date >= lastYear).all()
    session.close()
    rainyDates = []
    for date, prcp in rain:
        rainDict = {}
        rainDict[date] = prcp
        rainyDates.append(rainDict)
    return jsonify(rainyDates)

#return all stations
@app.route("/api/v1.0/stations")
def get_stations():
    stations = session.query(station.station).all()
    session.close()
    stations = list(np.ravel(stations))
    return jsonify(stations)


#return all temperatures since last year for most active station
@app.route("/api/v1.0/tobs")
def get_temp():
    active12 = session.query(measurment.tobs).filter(measurment.station == 'USC00519281', measurment.date >= lastYear).all()
    session.close()
    active12 = list(np.ravel(active12))
    return jsonify(active12)

#return min, avg, and max temperatures from said start date till latest date in db
@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(measurment.tobs), func.avg(measurment.tobs), func.max(measurment.tobs)).filter(measurment.date >= start).all()
    session.close()
    D = {"TMIN": results[0][0],
         "TAVG": results[0][1],
         "TMAX": results[0][2]}
    return jsonify(D)

#return min, avg, and max temperatures from said start date till said end date
@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start, end):
    results = results = session.query(func.min(measurment.tobs), func.avg(measurment.tobs), func.max(measurment.tobs)).filter(measurment.date >= start).filter(measurment.date <= end).all()
    session.close()
    D = {"TMIN": results[0][0],
         "TAVG": results[0][1],
         "TMAX": results[0][2]}
    return jsonify(D)

#define main behavior
if __name__ == '__main__':
    app.run(debug=True)