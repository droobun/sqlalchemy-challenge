import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func ,inspect, and_

from flask import Flask, jsonify
import datetime as dt
from datetime import datetime, date, time

# DB Setup
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    recent_year = (session.query(Measurement.date, Measurement.prcp).filter(
        and_(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23')).order_by(Measurement.date).all())



    """Return a list of all precipitation with dates"""

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(recent_year))

    return jsonify(all_names)

    #return JSON of stations

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    active_stations = session.query(Station.station).all()



    """Return a list of all station names"""


    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(active_stations))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs_year = session.query(Measurement.tobs).filter(and_(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23')).filter(Measurement.station == 'USC00519281').all()




    """Return a list of all tobs names"""


    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(tobs_year))

    return jsonify(all_names)

    

# Start the date route:

@app.route("/api/v1.0/start=<start>")
def start(start):
   
    session = Session(engine)

    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start_date).all()

    session.close()

    start_tobs = []

    for min, max, avg in results:
        tobs_dictionary = {}
        tobs_dictionary["Min"] = min
        tobs_dictionary["Max"] = max
        tobs_dictionary["Avg"] = avg
        start_tobs.append(tobs_dictionary)

    return jsonify(start_tobs)


 #start to end date route

@app.route("/api/v1.0/start=<start>/end=<end>")
def start_end(start, end):
    
    session = Session(engine)

    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, '%Y-%m-%d')

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
        .filter(Measurement.date.between(start, end)).all()

    session.close()

    start_end = []

    for min, max, avg in results:
        tobs_dictionary = {}
        tobs_dictionary["Min"] = min
        tobs_dictionary["Max"] = max
        tobs_dictionary["Avg"] = avg
        start_end.append(tobs_dictionary)

    return jsonify(start_end)


if __name__ == '__main__':
    app.run(debug=True)

