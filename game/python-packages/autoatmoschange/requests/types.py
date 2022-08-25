from dataclasses import dataclass, field
import datetime
from enum import Enum
from pytz import timezone

#Lookup for country code -> full country name
COUNTRY_CODE_LOOKUP = {
    "AF": "Afghanistan",
    "AX": "Åland Islands",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BH": "Bahrain",
    "BS": "Bahamas",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BQ": "Bonaire",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo",
    "CD": "Congo",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Côte d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CW": "Curaçao",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands (Malvinas)",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Territories",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard Island and McDonald Islands",
    "VA": "Holy See (Vatican City State)",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea",
    "KR": "Korea",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Lao",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macao",
    "MK": "Macedonia",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia",
    "MD": "Moldova",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestine",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin (French part)",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and the Grenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SX": "Sint Maarten (Dutch part)",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and the South Sandwich Islands",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syrian Arab Republic",
    "TW": "Taiwan",
    "TJ": "Tajikistan",
    "TZ": "Tanzania",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "US": "United States",
    "UM": "United States Minor Outlying Islands",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VE": "Venezuela, Bolivarian Republic of",
    "VN": "Viet Nam",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "WF": "Wallis and Futuna",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia"
}

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
    country_name: str
    state: str
    local_names: dict[str, str] = None

    def __init__(
        self,
        name: str,
        lat: float,
        lon: float,
        country: str,
        state: str,
        local_names: dict[str, str] = None
    ):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.country_name = COUNTRY_CODE_LOOKUP.get(country, country)
        self.state = state
        self.local_names = local_names


class TemperatureUnit(Enum):
    Kelvin = 0
    Celsius = 1
    Fahrenheit = 2

@dataclass
class LatLonPair:
    lon: float
    lat: float

@dataclass
class SimpleWeatherInfo:
    id: int
    main: str
    description: str
    icon: str

@dataclass
class MainWeatherInfo:
    feels_like: float
    pressure: float
    humidity: float
    _temp: float
    _temp_min: float
    _temp_max: float
    sea_level: float = None
    grnd_level: float = None

    def __init__(
        self,
        feels_like: float,
        pressure: float,
        humidity: float,
        temp: float,
        temp_min: float,
        temp_max: float,
        sea_level: float = None,
        grnd_level: float = None
    ):
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self._temp = temp
        self._temp_min = temp_min
        self._temp_max = temp_max
        self.sea_level = sea_level
        self.grnd_level = grnd_level

    def get_temp(self, unit: TemperatureUnit=TemperatureUnit.Kelvin) -> float:
        """
        Special getter which allows for the customization of temperature units as specified

        IN:
            unit - a TemperatureUnit value
                (Default: Kelvin)

        OUT:
            Temperature in the desired format
        """
        return self.__unithandler(unit, self._temp)

    def get_temp_min(self, unit: TemperatureUnit=TemperatureUnit.Kelvin) -> float:
        """
        Special getter which allows for the customization of temperature units as specified

        IN:
            unit - a TemperatureUnit value
                (Default: Kelvin)

        OUT:
            Temperature in the desired format
        """
        return self.__unithandler(unit, self._temp_min)

    def get_temp_max(self, unit: TemperatureUnit=TemperatureUnit.Kelvin) -> float:
        """
        Special getter which allows for the customization of temperature units as specified

        IN:
            unit - a TemperatureUnit value
                (Default: Kelvin)

        OUT:
            Temperature in the desired format
        """
        return self.__unithandler(unit, self._temp_max)

    @staticmethod
    def _kelvin_to_celsius(kelvin: float) -> float:
        return kelvin - 273.15

    @staticmethod
    def _celsius_to_fahrenheit(celsius: float) -> float:
        return 1.8 * celsius + 32

    @staticmethod
    def _kelvin_to_fahrenheit(kelvin: float) -> float:
        return MainWeatherInfo._celsius_to_fahrenheit(
            MainWeatherInfo._kelvin_to_celsius(kelvin)
        )

    @staticmethod
    def __unithandler(unit: TemperatureUnit, temperature_value: float) -> float:
        """
        Internal unit handler to convert temperatures
        """
        if unit == TemperatureUnit.Celsius:
            return MainWeatherInfo._kelvin_to_celsius(temperature_value)

        elif unit == TemperatureUnit.Fahrenheit:
            return MainWeatherInfo._kelvin_to_fahrenheit(temperature_value)

        return temperature_value

@dataclass
class WindWeatherInfo:
    speed: float
    deg: int
    gust: int = None

@dataclass
class CloudInfo:
    all: int

@dataclass
class SysInfo:
    type: int
    id: int
    country: str
    sunrise: float
    sunset: float
    message: float = None

    def __init__(
        self,
        type: int,
        id: int,
        country: str,
        sunrise: float,
        sunset: float,
        message: float = None,
    ):
        """
        """
        self.type = type
        self.id = id
        self.country = country
        self.sunrise = sunrise
        self.sunset = sunset
        self.message = message

        self._sunrise_localdt = datetime.datetime.fromtimestamp(sunrise)
        self._sunset_localdt = datetime.datetime.fromtimestamp(sunset)

    def get_sunrise(self, tzinfo: datetime.tzinfo = None) -> datetime.datetime:
        """
        Gets sunrise time

        IN:
            tzinfo - a tzinfo object representing a timezone to convert to
                (Default: Local time)

        OUT:
            datetime.datetime of the sunrise time of the city
        """
        if tzinfo is None:
            tzinfo = datetime.datetime.now().astimezone().tzinfo

        return self._sunrise_localdt.astimezone(tzinfo)

    def get_sunset(self, tzinfo: datetime.tzinfo = None) -> datetime.datetime:
        """
        Gets sunset time

        IN:
            tzinfo - a tzinfo object representing a timezone to convert to
                (Default: Local time)

        OUT:
            datetime.datetime of the sunset time of the city
        """
        if tzinfo is None:
            tzinfo = datetime.datetime.now().astimezone().tzinfo

        return self._sunset_localdt.astimezone(tzinfo)

@dataclass
class WeatherInfo:
    """
    Based off docs from https://openweathermap.org/current
    """
    coord: dict[str, float]
    weather: list[SimpleWeatherInfo]
    base: str
    main: MainWeatherInfo
    visibility: int
    wind: dict
    clouds: CloudInfo
    sys: SysInfo
    timezone: int
    id: int
    dt: int
    name: str
    cod: int
    rain: dict[str, float] = field(default_factory=lambda: dict())
    snow: dict[str, float] = field(default_factory=lambda: dict())

    def from_json(json_obj):
        """
        Initializes a WeatherInfo object from json
        """
        rv = WeatherInfo(**json_obj)

        rv.main = MainWeatherInfo(**json_obj["main"])
        rv.sys = SysInfo(**json_obj["sys"])
        return rv
