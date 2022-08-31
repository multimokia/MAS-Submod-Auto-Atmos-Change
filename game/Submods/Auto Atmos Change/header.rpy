init -990 python in mas_submod_utils:
    awc_submod = Submod(
        author="multimokia",
        coauthors=["Legendkiller21"],
        name="Auto Atmos Change",
        description="This submod allows Monika's room to match either the weather or the sunrise and sunset times (or both) to your own location.",
        version="3.0.0",
        settings_pane="auto_atmos_change_settings",
        version_updates={
            "multimokia_auto_atmos_change_v2_0_7": "multimokia_auto_atmos_change_v2_0_8",
            "multimokia_auto_atmos_change_v2_0_8": "multimokia_auto_atmos_change_v3_0_0"
        }
    )

init -989 python in awc:
    import store

    #Register the updater if needed
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod=store.mas_submod_utils.awc_submod,
            user_name="multimokia",
            repository_name="MAS-Submod-Auto-Atmos-Change",
            tag_formatter=lambda x: x[x.index('_') + 1:],
            update_dir="",
            attachment_id=None,
        )

label multimokia_auto_atmos_change_v2_0_7(version="v2_0_7"):
    return

label multimokia_auto_atmos_change_v2_0_8(version="v2_0_8"):
    return

label multimokia_auto_atmos_change_v3_0_0(version="v3_0_0"):
    python:
        #Attempt to migrate latlon from old vars
        if (
            persistent._awc_player_location.get("lat")
            and persistent._awc_player_location.get("lon")
        ):
            persistent._aac_player_latlon = (persistent._awc_player_location["lat"], persistent._awc_player_location["lon"])

        else:
            #We need to re-prompt for location. We'll recondition the setup topic for now
            #TODO: Build out a re-ask topic and queue that instead
            mas_setEVLPropValues(
                "awc_monika_player_location",
                conditional="mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)",
                action=EV_ACT_QUEUE
            )

        #Check if the apikey is invalid
        try:
            if awc.utils.checkIsinvalidAPIKey(persistent._awc_api_key):
                #Queue a topic saying the player needs to re-add their api key
                queueEvent("aac_need_readd_apikey")

        except (awc.utils.requests.ConnectionError, awc.utils.requests.ReadTimeout) as ex:
            #We can't trust the result here, we don't know if the API key is valid
            store.mas_submod_utils.submod_log.error(f"Failed to validate API key: {ex}")
            queueEvent("aac_need_readd_apikey")

        #_awc_api_key is deprecated with the API keys system
        safeDel("_awc_api_key")
        #_awc_player_location has been condensed down to a simple latlon tuple
        safeDel("_awc_player_location")

        #These now default to False
        persistent._aac_is_awc_enabled = False
        persistent._aac_is_ast_enabled = False

    return
