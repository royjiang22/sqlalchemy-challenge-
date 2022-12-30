import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/royjiang/Desktop/UCI-VIRT-DATA-PT-10-2022-U-LOLC/SurfUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
session = Session(engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    
    return (
        f"Welcome, List all available api routes. <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB

    station_results = session.query(Measurement.station).all()
    all_station_names = list(np.ravel(station_results))

    return jsonify(all_station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    tobss = session.query(Measurement.tobs).\
            filter(Measurement.station == 'USC00519281' ).\
            filter(Measurement.date >= '2017,8,23').all()
    tobs_list = list(np.ravel(tobss))
    return jsonify (tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):

    sel = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start).all()

    temp_list =[]
    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_list.append(temp_dict)

    return jsonify (temp_list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):

    sel = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temp_list =[]
    for min, max, avg in results:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["max"] = max
        temp_dict["avg"] = avg
        temp_list.append(temp_dict)

    return jsonify (temp_list)

    


if __name__ == '__main__':
    app.run(debug=True)
