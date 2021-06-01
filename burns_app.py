from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# # Dictionary of Justice League
# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent:Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

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


@app.route("/api/v1.0/burns-climate-analysis")
def justice_league():
    """Return the justice league data as json"""

    return jsonify(justice_league_members)


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




if __name__ == "__main__":
    app.run(debug=True)
