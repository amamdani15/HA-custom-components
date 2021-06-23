"""Constants for the Islamic Prayer component."""
DOMAIN = "islamic_prayer_times_custom"
NAME = "Islamic Prayer Times"
PRAYER_TIMES_ICON = "mdi:calendar-clock"

FUTURE_DAYS = 7

API_URL = "http://api.aladhan.com/timings"

SENSOR_TYPES = {
    "Fajr": "prayer",
    "Sunrise": "time",
    "Dhuhr": "prayer",
    "Asr": "prayer",
    "Maghrib": "prayer",
    "Isha": "prayer",
    "Sunset" : "time",
    "Imsak": "time",
    "Midnight": "time",
}

CONF_CALC_METHOD = "calculation_method"
CONF_SCHOOL = "school"
CONF_MIDNIGHT_MODE = "midnightMode"
CONF_LAT_ADJ_METHOD = "latitudeAdjustmentMethod"
CONF_CUSTOM_FAJR_ANGLE = "customFajrAngle"
CONF_MAGHRIB_ANGLE_OR_MINS_AFTER_SUNSET = "maghribAngleOrMinsAfterSunset"
CONF_ISHA_ANGLE_OR_MINS_AFTER_SUNSET = "ishaAngleOrMinsAfterSunset"

CALC_METHODS = {
    "Shia Intha-Ashari": 0,
    "Karachi": 1,
    "ISNA": 2,
    "MWL": 3,
    "Makkah": 4,
    "Egypt": 5,
    "Tehran": 7,
    "Gulf": 8,
    "Kuwait": 9,
    "Qatar": 10,
    "Singapore": 11,
    "France": 12,
    "Turkey": 13,
    "Russia": 14,
    "Custom": 99
}
SCHOOLS = ["Shafi", "Hanafi"]
LAT_ADJ_METHODS = ["Middle of the Night", "One Seventh", "Angle Based"]
MIDNIGHT_MODES = ["Standard", "Jafari"]


DEFAULT_CALC_METHOD = "ISNA"
DEFAULT_SCHOOL = "Shafi"
DEFAULT_MIDNIGHT_MODE = "Standard"
DEFAULT_LAT_ADJ_METHOD = "Angle Based"

DATA_UPDATED = "Islamic_prayer_data_updated"
