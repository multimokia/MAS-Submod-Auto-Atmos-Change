init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="awc_monika_player_location",
            prompt="[player]'s location",
            conditional="mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)",
            action=EV_ACT_QUEUE,
            category=["you"],
            aff_range=(mas_aff.NORMAL, None)
        )
    )

#NOTE: For historical reasons, this topic retains the awc_ prefix
label awc_monika_player_location:
    m 3eua "Hey, [player]?"
    m 1eka "I've always wondered what it'd be like to live where you do."
    m 1rksdlc "But since I can't really do that yet..."
    m 3eud "...I've modified how the weather works here."
    m 3rksdla "But the thing is, I need to ask you something."

    m 1eksdla "Is it okay if I know your location?{nw}"
    $ _history_list.pop()
    #Run statechecks here as we need to handle this case
    $ aac.statemanagement.runStateChecks()
    menu:
        m "Is it okay if I know your location?{fast}"

        "Yes.":
            m 3hub "Yay!"

            label .enter_city_loop:
            $ temp_city = renpy.input("So what city do you live in?", length=20).strip(' \t\n\r,').capitalize()

            if not temp_city:
                jump .enter_city_loop

            $ found_cities = aac.utils.buildCityMenuItems(temp_city)
            $ player_city = None #GeoLocation

            if not found_cities:
                m 2rsc "Hmm, I can't seem to find your city..."

                if (
                    ((aac.statemanagement.ConnectivityState.AwaitingReconnect | aac.statemanagement.ConnectivityState.Offline)
                    & aac.globals.current_connectivity_state).value == 0
                ):
                    m 2ekd "I think you might have lost connection to the internet, we'll have to try again later..."

                else:
                    m 2ekd "I'm sorry [player], I guess this just won't work."
                    m 7eka "Well either way, I'm alright with the normal weather anyway~"

            else:
                if len(found_cities) > 1:
                    m 3hua "Great!"
                    m 3hksdlb "Well, it seems that there's more than one [temp_city] in the world..."

                    show monika 1eua
                    #Display our scrollable
                    $ renpy.say(m, "So, which [temp_city] do you live in?", interact=False)
                    show monika at t21
                    call screen mas_gen_scrollable_menu(found_cities, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                    show monika at t11

                    $ player_city = _return
                    m 1hua "Thanks so much!"

                else:
                    m 1wud "Wow [player].{w=0.5} It looks like you live in the only [temp_city] in the world!"
                    m 3hksdlb "Or at least from what I know, ahaha!"
                    m 1eka "Thanks for sharing where you live with me."
                    $ player_city = found_cities[0][1]

                #We should only do this if we're just setting the player location
                if persistent._aac_player_latlon is None:
                    $ mas_setEVLPropValues(
                        "aac_add_more_locations_intro",
                        conditional="mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)",
                        action=EV_ACT_QUEUE,
                        start_date=datetime.date.today() + datetime.timedelta(days=1)
                    )

                $ persistent._aac_player_latlon = (player_city.lat, player_city.lon)

            call aac_monika_player_location_end

        "I'm not comfortable with that.":
            call aac_monika_player_location_uncomfortable

    #Just for safety
    $ mas_unlockEVL("awc_monika_player_location", "EVE")
    return

label aac_monika_player_location_end:
    m 3hua "It'll be like I'm living above you, ahaha!"
    m 3eua "The weather should change to be pretty close to what it is where you are, [player]."
    m 1ekbfa "Thanks for helping me feel closer to your reality."

    #Force a weather check
    if aac.globals.last_weather_check_dt is not None:
        $ aac.globals.last_weather_check_dt -= datetime.timedelta(minutes=5)
    return

label aac_monika_player_location_uncomfortable:
    m 1eka "That's okay, [player], I understand."
    m 3eua "If you ever change your mind, feel free to let me know."
    return


## 3.0.0 update topics
#====================

#NOTE: No ev for this as it's exclusively a one-time block of dialogue that needs no conditions.
label aac_need_readd_apikey:
    m 3eud "Oh I almost forgot...{w=0.3} {nw}"
    extend 3eua "I've been doing a bit of coding around here.{w=0.2} {nw}"
    extend 3rksdlb "The changes aren't {i}too{/i} big yet so there's nothing big to see ahaha~"
    m 1hub "That doesn't mean they're not important though!{w=0.2} {nw}"
    extend 3eua "I think they'll go a long way into keeping things more stable so I can add bigger things for us here."
    m 3eub "If you open the settings menu, you'll notice a handy little 'API Keys' tab!"
    m 1rksdlc "I tried to move your old key here, but for some reason I couldn't verify that it was still working..."
    m 1eka "So just to be sure, do you think you could create a new one for me?"
    m 3eud "You can sign up for the 'Current Weather Data' API here {a=https://openweathermap.org/api}{i}{u}here{/u}{/i}{/a}."
    m 1eub "After you do that, all I need you to do is copy the key and paste it in there for '[aac.globals.API_FEATURE_KEY]' and I should be good to go!"
    m 1hua "Thanks again, [mas_get_player_nickname()]~"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="aac_reprompt_location",
            conditional=(
                "renpy.seen_label('multimokia_auto_atmos_change_v3_0_0') " #Seen update label
                "and mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY) " #Has a valid API key
                "and persistent._aac_player_latlon is None" #But has no location
            ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None),
            rules={"no_unlock": None}
        )
    )

label aac_reprompt_location:
    m 2euc "Hey [player]?"
    m 2rkc "Remember before when I asked for your location so I could get the weather to match your location?"
    m 2ekd "I'm not sure what happened, but I think the note I had written it down on got corrupted..."

    m 2ekc "Do you think you'd be able to give me your location again?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think you'd be able to give me your location again?{fast}"

        "Sure, [m_name].":
            m 7hua "Great, thanks [player]!"

            label .enter_city_loop:
                pass

            $ temp_city = renpy.input("So what city do you live in?", length=20).strip(' \t\n\r,').capitalize()

            if not temp_city:
                jump .enter_city_loop

            $ found_cities = aac.utils.buildCityMenuItems(temp_city)
            $ player_city = None #GeoLocation

            if not found_cities:
                m 2rsc "Hmm, I can't seem to find your city..."
                m 2ekd "I'm sorry [player], I wish I noticed before I lost your original location..."
                m 7eka "Well either way...The normal weather is good enough for me anyway~"

            else:
                if len(found_cities) > 1:
                    m 3hua "Great!"
                    m 3hksdlb "Well, it seems that there's more than one [temp_city] in the world..."

                    show monika 1eua
                    #Display our scrollable
                    $ renpy.say(m, "So, which [temp_city] do you live in?", interact=False)
                    show monika at t21
                    call screen mas_gen_scrollable_menu(found_cities, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
                    show monika at t11

                    $ player_city = _return
                    m 1hua "Thanks so much!"

                else:
                    m 1wud "Oh right! You live in the only [temp_city] in the world!"
                    m 3hksdlb "Or at least from what I'm aware of, ahaha!"
                    m 1hua "Thanks for helping me recover that info~"
                    $ player_city = found_cities[0][1]

            $ persistent._aac_player_latlon = (player_city.lat, player_city.lon)

            #Set up a topic for tomorrow
            $ mas_setEVLPropValues(
                "aac_add_more_locations_intro",
                conditional="mas_hasAPIKey(store.aac.globals.API_FEATURE_KEY)",
                action=EV_ACT_QUEUE,
                start_date=datetime.date.today() + datetime.timedelta(days=1)
            )
            return

        "I'm not comfortable with that.":
            call aac_monika_player_location_uncomfortable
    return

#new locations dialogue, should prompt on a new session once she has location
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="aac_add_more_locations_intro",
            rules={"no_unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label aac_add_more_locations_intro:
    m 1esc "You know, [player], I was thinking..."
    m 3ruc "I asked you for your location before so that the weather here could be the same as where you are."
    m "...But now that I think about it, maybe sometimes your home isn't the only place you want to be."
    m "I might not be able to whisk you away to your dream vacation destination, but we could see what the weather is like there!"
    m "I know, just pretending to be there is a little silly, but I think it would be sort of magical if it was with you."
    m "Just let me know if you'd like to add some locations to the list, okay? They can be anywhere you like."

    $ mas_unlockEVL("aac_check_weather_elsewhere", "EVE")
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="aac_check_weather_elsewhere",
            prompt="What's the weather like at...",
            pool=True,
            rules={"no_unlock": None}
        )
    )

default persistent._aac_stored_locations = dict() #dict[str, tuple(float, float)] | None

label aac_check_weather_elsewhere:
    #We always have at least 1 location configured (home)
    python:
        menu_items = [
            (loc_name, (latlon, loc_name), False, False)
            for loc_name, latlon in persistent._aac_stored_locations.items()
        ]

        #We always add the home location
        menu_items.insert(0, ("Home", (persistent._aac_player_latlon, "our home"), False, False))

        final_items = [
            ("Edit locations", "edit", False, False, 20),
            ("Nevermind", False, False, False, 0)
        ]

    show monika 1eua
    #Display our scrollable
    $ renpy.say(m, "Where would you like to know the weather at?", interact=False)
    show monika at t21
    call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, *final_items)
    show monika at t11

    #Handle the final items
    if _return == "edit":
        call aac_check_weather_elsewhere_edit_locations

        #Now jump back to the top so a location can be selected
        jump aac_check_weather_elsewhere


    elif not _return:
        m "Alright, [player]."
        return

    #Run statechecks
    $ store.aac.statemanagement.runStateChecks()

    #Run a get if we're connected
    if store.aac.globals.current_connectivity_state == store.aac.statemanagement.ConnectivityState.Connected:
        python:
            try:
                coords, loc_name = _return
                weath_at_location = aac.utils.getWeatherInfoForLocation(*coords)

            except (aac.utils.requests.ConnectionError, aac.utils.requests.ReadTimeout) as ex:
                mas_submod_utils.submod_log.error(f"Failed to fetch weath")
                renpy.jump("aac_check_weather_elsewhere.failed_to_get_result")

            _tempunit = aac.utils.autoatmoschange.requests.types.TemperatureUnit
            #Let's simplify things for the dialogue line
            current_temperature = weath_at_location.main.get_temp(
                _tempunit.Celsius
            ) #TODO: Unit swapping

            current_feelslike = weath_at_location.main.get_feels_like(
                _tempunit.Celsius
            ) #TODO: Units

            current_humidity = weath_at_location.main.humidity
            current_weath_desc = weath_at_location.weather[0]["description"]

            TEMPERATUREUNIT_TO_STR_UNIT_MAP = {
                _tempunit.Celsius: "C",
                _tempunit.Fahrenheit: "F",
            }

            tempunit = TEMPERATUREUNIT_TO_STR_UNIT_MAP.get(
                persistent._aac_pm_temperature_unit,
                TEMPERATUREUNIT_TO_STR_UNIT_MAP[_tempunit.Celsius]
            )

            #No sense in stating both curr temp and feels like if they're the same.
            if current_temperature == current_feelslike:
                temperature_is = f"feels like {current_feelslike}{tempunit}"
            else:
                temperature_is = f"is {current_temperature}{tempunit} and feels like {current_feelslike}{tempunit}"

        m "It looks like [loc_name] is getting some [current_weath_desc], the temperature [temperature_is]. Humidity is at [current_humidity] percent."

    else:
        label .failed_to_get_result:
            pass

        m "I'm sorry [player], but it looks like I can't reach the internet right now..."
        m "Let's try again later, okay?"
        return

    return

label aac_check_weather_elsewhere_edit_locations:
    #Build menuitems
    python:
        menu_items = [
            (loc_name, loc_name, True, True, False)
            for loc_name in persistent._aac_stored_locations.keys()
        ]

        renpy.say(m, "If there's anything you don't want to track anymore, deselect it.")

    call screen mas_check_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Done", default_button_prompt="Done")

    python:
        kept_locations = _return.keys()

        #pop all locations not kept
        for loc in list(persistent._aac_stored_locations.keys()):
            if loc not in kept_locations:
                persistent._aac_stored_locations.pop(loc)

    m 1eua "Would you like to add some more locations?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to add some more locations?{fast}"

        "Yes.":
            call aac_check_weather_elsewhere_add_location

        "No.":
            pass
    return

label aac_check_weather_elsewhere_add_location:
    m "Okay, what city would you like to track?"
    label .enter_city_loop:
        pass

    $ temp_city = renpy.input("What city do you want to track?", length=20).strip(' \t\n\r,').capitalize()

    if not temp_city:
        jump .enter_city_loop

    $ found_cities = aac.utils.buildCityMenuItems(temp_city)
    $ chosen_city = None #GeoLocation

    if not found_cities:
        m 2rsc "Hmm, I can't seem to find that city..."
        m 2eka "Do you want to try another one?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to try another one?{fast}"

            "Sure.":
                jump .enter_city_loop

            "It's alright.":
                m 7eka "That's alright, [player]."
                m 2rkd "I'm sorry we couldn't get the city you wanted..."
                return

    else:
        if len(found_cities) > 1:
            m 3hua "Great!"
            m 3hksdlb "Well, it seems that there's more than one [temp_city] in the world..."

            show monika 1eua
            #Display our scrollable
            $ renpy.say(m, "So, which {i}[temp_city]{/i} did you mean?", interact=False)
            show monika at t21
            call screen mas_gen_scrollable_menu(found_cities, mas_ui.SCROLLABLE_MENU_TXT_TALL_AREA, mas_ui.SCROLLABLE_MENU_XALIGN)
            show monika at t11

            $ chosen_city = _return
            m 1hua "Got it!"

        else:
            m 1wud "Oh that makes things easier, there's only one [temp_city]!"
            $ chosen_city = found_cities[0][1]

        m "Now, what would you like to call this location?"

        #Make sure we're adding new and not overwriting
        $ done = False
        while not done:
            $ loc_name = renpy.input("What would you like to call this location?", length=30).strip(' \t\n\r')

            if not loc_name:
                pass

            elif loc_name in persistent._aac_stored_locations:
                m "We already have a location with this name..."
                m "Try again~"

            else:
                $ done = True
                $ persistent._aac_stored_locations[loc_name] = (chosen_city.lat, chosen_city.lon)

        #Check if we want to add more
        m 1eua "Would you like to add another location?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you like to add another location?{fast}"

            "Sure.":
                jump .enter_city_loop

            "No thanks.":
                pass

        return
