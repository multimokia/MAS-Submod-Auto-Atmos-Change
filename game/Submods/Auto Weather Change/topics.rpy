init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="awc_monika_player_location",
            prompt="[player]'s location",
            conditional="not store.awc_isInvalidAPIKey(store.persistent._awc_API_key)",
            action=EV_ACT_QUEUE,
            category=["you"],
            aff_range=(mas_aff.NORMAL,None)
        )
    )

label awc_monika_player_location:
    m 3eua "Hey, [player]?"
    m 1eka "I've always wondered what it'd be like to live where you do."
    m 1rksdlc "But since I can't really do that yet..."
    m 3eud "...I've modified how the weather works here."
    m 3rksdla "But the thing is, I need to ask you something."

    m 1eksdla "Is it okay if I know your location?{nw}"
    $ _history_list.pop()
    menu:
        m "Is it okay if I know your location?{fast}"

        "Yes.":
            m 3hub "Yay!"

            label .enter_city_loop:
            $ temp_city = renpy.input("So what city do you live in?", length=20).strip(' \t\n\r,').capitalize()

            if not temp_city:
                jump .enter_city_loop

            $ found_cities = awc.utils.buildCityMenuItems(temp_city)
            $ player_city = None #GeoLocation

            if not found_cities:
                m 2rsc "Hmm, I can't seem to find your city..."
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
                    $ player_city = found_cities[0]

            $ persistent._awc_player_latlon = (player_city.lat, player_city.lon)
            call awc_monika_player_location_end

        "I'm not comfortable with that.":
            call awc_monika_player_location_uncomfortable

    #Just for safety
    $ mas_unlockEVL("awc_monika_player_location", "EVE")
    return

label awc_monika_player_location_end:
    m 3hua "It'll be like I'm living above you, ahaha!"
    m 3eua "The weather should change to be pretty close to what it is where you are, [player]."
    m 1ekbfa "Thanks for helping me feel closer to your reality."

    #Force a weather check
    if awc_globals.last_weather_check_dt is not None:
        $ awc_globals.last_weather_check_dt -= datetime.timedelta(minutes=5)
    return

label awc_monika_player_location_uncomfortable:
    m 1eka "That's okay, [player], I understand."
    m 3eua "If you ever change your mind, feel free to let me know."
    return
