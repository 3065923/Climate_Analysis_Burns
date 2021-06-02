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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/tobs")
def temp_analysis():

    # Create session (link) from Python to the DB
    session = Session(engine)

    # mas stands for most active station
    mas_data_sess= session.query(Measurement.station, func.min(Measurement.tobs).label('Lowest Temperature'), func.max(Measurement.tobs).label('Highest Temperature'), func.avg(Measurement.tobs).label('Average Temperature'))\
              .filter(Measurement.station == 'USC00519281').all()



    mas_data= [{'Station': result[0], 'Lowest Temperature': result[1], 'Highest Temperature': result[2], 'Averager Temperature': result[3]} for result in mas_data_sess]
    


    return jsonify(mas_data)




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

    session.close()

    # Create a dictionary from the row data and append to a list of prcp_data
    prcp_dict= [{result[1]: result[0]}for result in results]


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

    station_activity= [result[0] for result in station_act_sess]




    return jsonify(station_activity)





if __name__ == "__main__":
    app.run(debug=True)
