init -20 python in aac.statemanagement:
    import datetime
    from enum import IntFlag
    import store

    class ConnectivityState(IntFlag):
        """
        Enum representing connectivity
        """
        Offline = 1
        AwaitingReconnect = 2
        Connected = 4


    def runStateChecks():
        """
        Checks whether we should start or reset the offline timer and whether we timed out
        """
        if not store.aac.utils.testConnection():
            _now = datetime.datetime.now()
            store.aac.globals.current_connectivity_state = ConnectivityState.Offline

            #We setup a timeout here. If this is passed, we should fallback to stock behaviour.
            if (
                store.mas_timePastSince(
                    store.aac.globals.weather_offline_timeout_dt,
                    datetime.timedelta(minutes=30),
                    _now
                )
            ):
                if store.aac.globals.weather_offline_timeout_dt is None:
                    store.aac.globals.weather_offline_timeout_dt = _now + datetime.timedelta(minutes=30)
                    store.aac.globals.current_connectivity_state = ConnectivityState.AwaitingReconnect

                else:
                    store.aac.globals.current_connectivity_state = ConnectivityState.Offline

            #We need to set this to AwaitingReconnect here to avoid getting caught in Offline forever
            elif store.aac.globals.weather_offline_timeout_dt is not None:
                store.aac.globals.current_connectivity_state = ConnectivityState.AwaitingReconnect

        else:
            #Timeout is no longer necessary
            store.aac.globals.weather_offline_timeout_dt = None
            store.aac.globals.current_connectivity_state = ConnectivityState.Connected
