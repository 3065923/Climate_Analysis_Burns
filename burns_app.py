from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################
# engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Instructions\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Measurement reference
Measurement = Base.classes.measurement

#Station measurement
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
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"By: Jake Burns<br/>"
        f"<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br>"
        f"/api/v1.0/start_date/end_date<br>"
        f"<br>"
        f"<br>"
        f"Notes: <br>"
        f"The 'start_date' API  returns TMIN,TMAX, TAVG from inputed start date to most recent date<br>"
        f"<br>"
        f"The 'start_date/end_date' API returns TMIN,TMAX, TAVG from inputed start date to inputed end date<br>"
        f"<br>"
        f"<br>"
        f"*Format for inputing date: YYYY-MM-DD"
    )


@app.route("/api/v1.0/<start_date>")


def tobs_from_date_start(start_date):
        
    # Create session (link) from Python to the DB
    session = Session(engine)

    start_range_temp= session.query(func.min(Measurement.tobs).label('Lowest Temperature'), func.max(Measurement.tobs).label('Highest Temperature'), func.avg(Measurement.tobs).label('Average Temperature'))\
              .filter(Measurement.date >= start_date).all()

    range_temp= [{'Lowest Temperature': result[0], 'Highest Temperature': result[1], 'Averager Temperature': result[2]} for result in start_range_temp]

    #Close Session
    session.close()

    return jsonify(range_temp)




@app.route("/api/v1.0/<start_date>/<end_date>")


def tobs_in_date_range(start_date=None, end_date=None):
        
    # Create session (link) from Python to the DB
    session = Session(engine)

    date_range_temp= session.query(func.min(Measurement.tobs).label('Lowest Temperature'), func.max(Measurement.tobs).label('Highest Temperature'), func.avg(Measurement.tobs).label('Average Temperature'))\
              .filter(Measurement.date.between(start_date, end_date)).all()

    range_temp_f= [{'Lowest Temperature': result[0], 'Highest Temperature': result[1], 'Averager Temperature': result[2]} for result in date_range_temp]

    #Close Session
    session.close()

    return jsonify(range_temp_f)




@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the justice league data as json"""

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Starting from the most recent data point in the database. 
    most_recent_date= dt.date(2017, 8, 23)
    

    # Calculate the date one year from the last date in data set.
    year_prior= most_recent_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.prcp, 
                        Measurement.date)\
                  .filter(Measurement.date > year_prior)\
                    .filter(Measurement.prcp != None).all()      #!= None  is sqlAlchemy equivalent to notnull()

    

    # Create a dictionary from the row data and append to a list of prcp_data
    prcp_dict= [{result[1]: result[0]}for result in results]

    #Close Session
    session.close()

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return the justice league data as json"""

    # Create session (link) from Python to the DB
    session = Session(engine)

    # List the stations and the counts in descending order.

    station_act_sess= session.query(Measurement.station, func.count(Measurement.station).label('Station Activity'))\
        .group_by(Measurement.station)\
        .order_by('Station Activity').all()

    # station_act_sess

    station_activity= {'Stations': [result[0] for result in station_act_sess]}

    #Close Session
    session.close()



    return jsonify(station_activity)



@app.route("/api/v1.0/tobs")
def temp_station_analysis():

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    most_recent_date= dt.date(2017, 8, 23)

    year_prior= most_recent_date - dt.timedelta(days=365)

   # Query the last 12 months of temperature observation data for this station and plot the results as a histogram

    #Most Active Staion: USC00519281

    temp_results = session.query(Measurement.station, Measurement.tobs, \
                            Measurement.date)\
                    .filter(Measurement.date > year_prior)\
                        .filter(Measurement.station == 'USC00519281')\
                        .filter(Measurement.tobs != None).all()      #!= None  is sqlAlchemy equivalent to notnull()

    #Close Session
    session.close()

    # List comprehension solution
    temp_rows = [{"Date": result[2], "Temperature": result[1]} for result in temp_results]


    return jsonify(temp_rows)




if __name__ == "__main__":
    app.run(debug=True)
