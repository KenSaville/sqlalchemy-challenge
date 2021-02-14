import numpy as np

import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/date/precipitation_on_date/<date><br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/temp_start_date/<date><br/>"
        f"/api/v1.0/temp_start_end/<date_start>/<date_end>"
    )

#@app.route("/api/v1.0/date/precipitation/<date>")
@app.route("/api/v1.0/date/precipitation_on_date/<date>")
def precipitation(date):
    # Create a session connecting DB
    session = Session(engine)

    """Return a list of precipitation amounts"""
    # Query all precipitation amounts
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date == date).all()

    session.close()

 # Createdictionary from the row data and append to a list of dates and precipitation
    date_precip = []
    for date, precipitation in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = precipitation
        date_precip.append(precip_dict)

    return jsonify(date_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create session to DB
    session = Session(engine)

    """Return a list of stations"""
    # Query stations
    station_results = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(station_results)


@app.route("/api/v1.0/temperature")

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query last year of temperature observations
    temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    tobs_list = []
    for date, temp in temp_obs:
        temp_obs_dict = {}
        temp_obs_dict["date"] = date
        temp_obs_dict["temperature"] = temperature_observation
        tobs_list.append(temp_obs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/temperature_given_start_date/<date>")
def temp_start_date(date):
    # Create session
    session = Session(engine)

    """Return a list of temperatures"""
    # Query stations
    tempe_start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()

    session.close()

    return jsonify(temp_start_date_results)


@app.route("/api/v1.0/temperature_given_start_end/<date_start>/<date_end>")
def temperature_start_end(date_start, date_end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures"""
    # Query stations
    temperature_start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date_start).filter(Measurement.date <= date_end).all()

    session.close()

    return jsonify(temperature_start_end_results)
# @app.route("/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug=True)