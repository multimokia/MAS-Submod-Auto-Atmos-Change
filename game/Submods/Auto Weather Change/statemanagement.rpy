init -20 python in awc.statemanagement:
    import datetime
    from enum import Enum
    import store

    class ConnectivityState(Enum):
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
        if not store.awc.utils.testConnection():
            _now = datetime.datetime.now()
            store.awc.globals.current_connectivity_status = ConnectivityState.Offline

            #We setup a timeout here. If this is passed, we should fallback to stock behaviour.
            if (
                store.mas_timePastSince(
                    store.awc.globals.weather_offline_timeout_dt,
                    datetime.timedelta(minutes=30),
                    _now
                )
            ):
                if store.awc.globals.weather_offline_timeout_dt is None:
                    store.awc.globals.weather_offline_timeout_dt = _now + datetime.timedelta(minutes=30)
                    store.awc.globals.current_connectivity_status = ConnectivityState.AwaitingReconnect

                else:
                    store.awc.globals.current_connectivity_status = ConnectivityState.Offline

            #We need to set this to AwaitingReconnect here to avoid getting caught in Offline forever
            elif store.awc.globals.weather_offline_timeout_dt is not None:
                store.awc.globals.current_connectivity_status = ConnectivityState.AwaitingReconnect

        else:
            #Timeout is no longer necessary
            store.awc.globals.weather_offline_timeout_dt = None
            store.awc.globals.current_connectivity_status = ConnectivityState.Connected
