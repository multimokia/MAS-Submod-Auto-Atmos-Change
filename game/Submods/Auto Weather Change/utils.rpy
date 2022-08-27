#The api key we'll use to access Open Weather Network's data
default persistent._awc_API_key = None #TODO: REPLACE WITH API KEYS FRAMEWORK

#Whether or not we have Auto Weather Change enabled
default persistent._awc_enabled = True

#Whether or not we have Auto Sun Times enabled
default persistent._awc_ast_enabled = True

init -50:
    #Player's latitude/longitude
    default persistent._awc_player_latlon = None

init -1 python:
    tt_awc_desc = (
        "Enable this to allow progressive weather to automatically match the weather at your location."
    )

    tt_ast_desc = (
        "Enable this to allow the sunrise and sunset times in MAS to match your location."
    )

#Our settings + Status pane
screen auto_atmos_change_settings():
    $ submods_screen_tt = store.renpy.get_screen("submods", "screens").scope["tooltip"]
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000

        hbox:
            if bool(store.mas_hasAPIKey(store.awc.globals.API_FEATURE_KEY)):
                style_prefix "check"
                box_wrap False
                textbutton _("Auto Weather Change"):
                    action ToggleField(persistent, "_awc_enabled")
                    selected persistent._awc_enabled
                    hovered SetField(submods_screen_tt, "value", tt_awc_desc)
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

                textbutton _("Auto Sun Times"):
                    action Function(store.awc_utils.toggleAST)
                    selected persistent._awc_ast_enabled
                    hovered SetField(submods_screen_tt, "value", tt_ast_desc)
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

            else:
                text "Please add a valid API key to use this submod.": #You can create one {a=https://openweathermap.org/api}{i}{u}here{/u}{/i}{/a}.":
                    xalign 1.0 yalign 0.0
                    style "main_menu_version"

    if bool(persistent._awc_API_key):
        text "API Key Valid":
            xalign 1.0 yalign 0.0
            xoffset -10
            style "main_menu_version"

init -18 python:
    #Initialize the lookup
    awc_buildCityLookupDict()

    #Create our async wrapper for weather progress
    await_weatherProgress = store.mas_threading.MASAsyncWrapper(
        store.awc_weatherProgress
    )

init -10 python in awc.utils:
    import store
    def toggleAST():
        """
        Toggles the auto-sun-times functionality
        """
        if store.persistent._awc_ast_enabled:
            store.persistent._awc_ast_enabled = False

        else:
            #If we're enabling this, we should reajust the values
            store.persistent._awc_ast_enabled = True
            store.persistent._mas_sunrise = dtToMASTime(store.awc.utils.getSunriseDT())
            store.persistent._mas_sunset = dtToMASTime(store.awc.utils.getSunsetDT())

    #And do the startup check here too
    if (
        store.persistent._awc_ast_enabled
        and store.awc_canGetAPIWeath()
        and testConnection()
    ):
        store.persistent._mas_sunrise = dtToMASTime(store.awc_getSunriseDT())
        store.persistent._mas_sunset = dtToMASTime(store.awc_getSunsetDT())


# Api key setup
init -21 python in awc.utils:
    import store
    import requests
    import autoatmoschange
    from autoatmoschange.requests.types import GeoLocation, WeatherInfo

    def testURL(url: str) -> bool:
        """
        Attempts to open the url provided

        IN:
            url - url to test

        OUT:
            True if successful, False otherwise
        """
        try:
            requests.head(url, timeout=1)

        except requests.ConnectionError as exc:
            store.mas_submod_utils.submod_log.error(exc)
            return False

        return True

    def testConnection() -> bool:
        """
        Checks if we have internet connection

        OUT:
            True if connection was successful, False otherwise
        """
        return testURL("http://www.google.com")

    def checkIsinvalidAPIKey(api_key)- > bool:
        """
        Checks if api key is invalid
        NOTE: This checks against London, GB as a known location

        IN:
            api_key - api key to check

        OUT:
            True if the request returns a 401 error (invalid), False otherwise
        """
        return requests.get(
            BASE_URL.format(
                lat=51.5085,
                lon=-0.1257,
                apikey=api_key
            )
        ).status_code == 401

#Helper methods
init -19 python in awc.utils:
    import store
    from enum import Enum
    import datetime
    import time
    import random
    from store.awc.statemanagement import ConnectivityState

    #Keep a reference to the original weatherProgress function as we intend to extend its functionality vs replace it.
    _originalWeatherProgress = store.mas_weather.weatherProgress

    def dtToMASTime(dt: datetime.datetime) -> int:
        """
        Converts a datetime.datetime to MAS time (settings menu)

        IN:
            dt - datetime.datetime object of the time to convert to MAS time

        OUT:
            the time in MAS settings time.
        """
        return dt.minute + dt.hour * 60

    def buildCityMenuItems(city_name: str) -> list[tuple]:
        """
        Builds a displayable city name/list of names (for buttons/dlg)

        IN:
            city_name - the city to build the full name for

        OUT:
            list of display names for the city in the form for a scrollable menu

        ASSUMES: There is an API key registered for the key stored in awc.globals.API_FEATURE_KEY
        """
        geolocations: list[GeoLocation] = autoatmoschange.requests.api.fetch_geolocation(
            city_name,
            store.mas_getAPIKey(store.awc.globals.API_FEATURE_KEY)
        )

        rv = list()
        #TODO: We'll filter out geolocations which are within 5% of each other
        for geolocation in geolocations:
            scrollable_list.append((
                f"{geolocation.name}, {geolocation.country_name}",
                geolocation,
                False,
                False
            ))

        return rv

    def getWeatherInfoForLocation(lat, long) -> WeatherInfo:
        """
        Gets weather for the given latitude/longitude

        IN:
            lat - latitidue
            lon - longitude

        OUT:
            WeatherInfo for the weather at the given location
        """
        return autoatmoschange.requests.api.fetch_weather_info(
            lat,
            lon,
            store.mas_getAPIKey(store.awc.globals.API_FEATURE_KEY)
        )

    def getCurrentWeather() -> WeatherInfo | None:
        """
        Gets the weather for the currently assigned player location

        OUT:
            WeatherInfo for the current location, or None if api key is invalid
        """
        try:
            return getWeatherInfoForLocation(*persistent._awc_player_latlon)
        except requests.ConnectionError as ex:
            store.mas_submod_utils.submod_log.error(ex)

        return None

    def weatherInfoToMASWeather(weath: WeatherInfo | None = None) -> store.MASWeather:
        """
        TODO: ME
        """
        if weath is None:
            weath = getCurrentWeather()

        return store.mas_weather_def

    def weatherProgress():
        """
        Extension for weatherProgress, building in the auto atmos behaviour
        """
        #Otherwise we do stuff
        if (
            store.mas_timePastSince(
                store.awc.globals.last_weather_check_dt,
                store.awc.globals.WEATHER_CHECK_INTERVAL
            )
        ):
            store.awc.globals.last_weather_check_dt = datetime.datetime.now() + store.awc.globals.WEATHER_CHECK_INTERVAL

            #In the case we're waiting for a reconnect, simply hold off.
            if store.awc.globals.current_connectivity_status == ConnectivityState.AwaitingReconnect:
                return False

            #We can't get here if we're offline, therefore we must be connected!
            else:
                #We have connection and a valid url. Get weath from api
                new_weather = weatherInfoToMASWeather()

                #Do we need to change weather?
                if new_weather != store.mas_current_weather:
                    #Let's see if we need to scene change
                    if store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        new_weather
                    ):
                        store.mas_idle_mailbox.send_scene_change()

                    #Now we change weather
                    store.mas_changeWeather(new_weather)

                    #Play the rumble in the back to indicate thunder
                    if new_weather == store.mas_weather_thunder:
                        renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")

            return True
