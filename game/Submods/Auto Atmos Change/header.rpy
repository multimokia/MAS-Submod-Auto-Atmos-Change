init -990 python in mas_submod_utils:
    aac_submod = Submod(
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

init -989 python in aac:
    import store

    #Register the updater if needed
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod=store.mas_submod_utils.aac_submod,
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
        #NOTE: If the transfer fails, a topic where Monika asks the player for their location again will be pushed
        #once a working API key has been added
        if (
            persistent._awc_player_location.get("lat")
            and persistent._awc_player_location.get("lon")
        ):
            persistent._aac_player_latlon = (persistent._awc_player_location["lat"], persistent._awc_player_location["lon"])

            #Since we've presumably had a location for a while now
            mas_setEVLPropValues(
                "aac_add_more_locations_intro",
                conditional="mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)",
                action=EV_ACT_QUEUE,
                start_date=datetime.date.today()
            )

        #In the case the initial setup topic was not seen for some reason, we should update its conditional as we have new checks
        with MAS_EVL("awc_monika_player_location") as aac_setup_evl:
            if aac_setup_evl.conditional is not None:
                aac_setup_evl.conditional = "mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)"
                aac_setup_evl.action = EV_ACT_QUEUE

        #Check if the apikey is invalid
        try:
            if aac.utils.checkIsInvalidAPIKey(persistent._awc_API_key):
                #Queue a topic saying the player needs to re-add their api key
                queueEvent("aac_need_readd_apikey")
            else:
                store.mas_api_keys.api_keys[store.aac.globals.API_FEATURE_KEY] = persistent._awc_API_key
                store.mas_api_keys.save_keys()

        except (aac.utils.requests.ConnectionError, aac.utils.requests.ReadTimeout) as ex:
            #We can't trust the result here, we don't know if the API key is valid
            store.mas_submod_utils.submod_log.error(f"Failed to validate API key: {ex}")
            queueEvent("aac_need_readd_apikey")

        #_awc_API_key is deprecated with the API keys system
        safeDel("_awc_API_key")
        #_awc_player_location has been condensed down to a simple latlon tuple
        safeDel("_awc_player_location")
        #_awc_enabled has been replaced to prevent crashloads and clean up ownership prefixes
        safeDel("_awc_enabled")
        #_awc_ast_enabled has also been replaced to prevent crashloads and clean up ownership
        safeDel("_awc_ast_enabled")

    return
