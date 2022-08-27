init -200 python in awc.globals:
    import datetime

    #API Feature key for fetching the api key from MAS' APIKeys framework
    API_FEATURE_KEY = "AutoAtmosChange"

    #Set a default interval for checking
    WEATHER_CHECK_INTERVAL = datetime.timedelta(minutes=5)

    #Current connection state
    current_connectivity_status = None

    #Stores the time at which it should check whether weather should change
    last_weather_check_dt = None

    #Stores the time when we go back to normal progressive weather if no connection
    weather_offline_timeout_dt = None

    #Weather status keywords
    SUN_KW = ['clear', 'sun']
    THUNDER_KW = ['storm', 'hurricane', 'tornado', 'thunderstorm']
    SNOW_KW = ['snow', 'sleet']

    #Weather thresh constants
    OVERCAST_CLOUD_THRESH = 75
    RAIN_RATE_THRESH = 3
