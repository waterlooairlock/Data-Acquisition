from command_handler import *
from secret import MONGOURI
import pymongo


@command_handler.route("/arduinos/get_readings")
def get_readings():
    if 'sensor_type' not in request.args:
        api_logger.warning(
            "get_readings called without 'sensor_type' declared: Aborted")
        return
    if 'sensor_id' not in request.args:
        api_logger.warning(
            "get_readings called without 'sensor_id' declared: Aborted")
        return
    # Read arguements into variables
    sensor_type = request.args['sensor_type']
    sensor_id = int(request.args['sensor_id'])

    try:
        dbclient = pymongo.MongoClient(MONGOURI)
        mydb = dbclient["watlock"]

    except BaseException:
        api_logger.error(
            "Connection to database failed: Aborted")

    sensor_readings_collection = mydb['sensor_readings']
    response = dict()
    try:
        readings = list(
            sensor_readings_collection.find(
                {
                    "sensor_type": sensor_type,
                    "sensor_id": sensor_id}).sort(
                "timestamp",
                pymongo.DESCENDING).limit(20))
        for reading in readings:
            reading["_id"] = str(reading["_id"])
        response["readings"] = readings
        return response
    except BaseException:
        response["readings"] = []
        return response
