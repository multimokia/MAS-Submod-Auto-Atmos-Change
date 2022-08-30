init -18 python in mas_weather:
    import store

    def weatherProgress() -> bool:
        """
        Runs a roll on mas_shouldRain() to pick a new weather to change to after a time between half an hour - one and a half hour

        RETURNS:
            - True or false on whether or not to call spaceroom
        """
        #If the player forced weather or we're not in a background that supports weather, we do nothing
        if store.mas_weather.force_weather or store.mas_current_background.disable_progressive:
            return False

        #Run state checks
        store.awc.statemanagement.runStateChecks()

        #If awc is disabled, we'll just run the original stock weatherprogress
        #As well, if we have no connection, we fallbacks
        if (
            not store.persistent._aac_is_awc_enabled
            or not store.mas_hasAPIKey(store.awc.globals.API_FEATURE_KEY)
            or store.awc.globals.current_connectivity_status == store.awc.statemanagement.ConnectivityState.Offline
        ):
            return store.awc.utils._originalWeatherProgress()

        else:
            return store.awc.utils.weatherProgress()
