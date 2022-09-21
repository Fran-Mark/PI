from orbit_predictor.locations import ET_CENTRO_ATOMICO, Location
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.predictors.accurate import HighAccuracyTLEPredictor
from datetime import timedelta as td

UTC_OFFSET = -3
MIN_ELEVATION_ANGLE = 10 #deg

def getNextPass(line1, line2):
    try:
        predictor = get_predictor_from_tle_lines([line1, line2])
        #Está en parámetro when_utc para buscar a partir de otro momento
        pred = predictor.get_next_pass(ET_CENTRO_ATOMICO, aos_at_dg=MIN_ELEVATION_ANGLE).aos + td(hours=UTC_OFFSET)
        return pred.strftime("%Y-%m-%d %H:%M:%S")
    except:
        raise ValueError("Invalid TLE")

def getCoordinates(line1, line2):
    try:
        predictor = get_predictor_from_tle_lines([line1, line2])
        #lat (deg), lon (deg), alt (km)
        return predictor.get_position().position_llh
    except:
        raise ValueError("Invalid TLE")

def getDopplerFactor(predictor : HighAccuracyTLEPredictor, location : Location):
    position = predictor.get_position()
    return location.doppler_factor(position)