init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="awc_monika_player_location",
            prompt="[player]'s location",
            conditional="mas_hasAPIKey(store.awc.globals.API_FEATURE_KEY)",
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
                    $ player_city = found_cities[0][1]

            $ persistent._aac_player_latlon = (player_city.lat, player_city.lon)
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
    if awc.globals.last_weather_check_dt is not None:
        $ awc.globals.last_weather_check_dt -= datetime.timedelta(minutes=5)
    return

label awc_monika_player_location_uncomfortable:
    m 1eka "That's okay, [player], I understand."
    m 3eua "If you ever change your mind, feel free to let me know."
    return


## 3.0.0 update topics
#=====================

label awc_need_readd_apikey:
    m 3eud "Oh I almost forgot...{w=0.3} {nw}"
    extend 3eua "I've been doing a bit of coding around here.{w=0.2} {nw}"
    extend 3rksdlb "The changes aren't {i}too{/i} big yet so there's nothing big to see ahaha~"
    m 1hub "That doesn't mean they're not important though!{w=0.2} {nw}"
    extend 3eua "I think they'll go a long way into keeping things more stable so I can add bigger things for us here."
    m 3eub "If you open the settings menu, you'll notice a handy little 'API Keys' tab!"
    m 1rksdlc "I tried to move your old key here, but for some reason I couldn't verify that it was still working..."
    m 1eka "So just to be sure, do you think you could create a new one for me?"
    m 3eud "You can sign up for the 'Current Weather Data' API here {a=https://openweathermap.org/api}{i}{u}here{/u}{/i}{/a}."
    m 1eub "After you do that, all I need you to do is copy the key and paste it in there for '[awc.globals.API_FEATURE_KEY]' and I should be good to go!"
    m 1hua "Thanks again, [mas_get_player_nickname()]~"
    return
