from orbit_predictor.locations import ET_CENTRO_ATOMICO
from orbit_predictor.sources import get_predictor_from_tle_lines

def getNextPass(line1, line2):
    try:
        predictor = get_predictor_from_tle_lines([line1, line2])
        return predictor.get_next_pass(ET_CENTRO_ATOMICO).aos.strftime("%Y-%m-%d %H:%M:%S")
    except:
        raise ValueError("Invalid TLE")

def getAngles(line1, line2):
    try:
        predictor = get_predictor_from_tle_lines([line1, line2])
        return predictor.get_position().elevation_deg, predictor.get_position().azimuth_deg
    except:
        raise ValueError("Invalid TLE")