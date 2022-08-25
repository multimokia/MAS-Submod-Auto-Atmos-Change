init -10 python in awc.requests.types:
    from dataclasses import dataclass

    @dataclass
    class GeoLocation:
        """
        Represents a set of geolocation info for a given city

        FIELDS:
            name: City name
            local_names: a map of lowercase country codes to local names for the given city
            lat: latitude of the city
            lon: longitude of the city
            state: state/province the city is in
        """
        name: str
        lat: float
        lon: float
        country: str
        state: str
        local_names: dict[str, str] = None
