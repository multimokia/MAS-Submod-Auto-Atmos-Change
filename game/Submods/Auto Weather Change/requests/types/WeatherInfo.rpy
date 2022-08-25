init -10 python in awc.requests.types:
    from dataclasses import dataclass, field
    from enum import Enum

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
            return self.__unithandler(unit, self._temp)

        def get_temp_min(self, unit: TemperatureUnit=TemperatureUnit.Kelvin) -> float:
            return self.__unithandler(unit, self._temp_min)

        def get_temp_max(self, unit: TemperatureUnit=TemperatureUnit.Kelvin) -> float:
            return self.__unithandler(unit, self._temp_max)

        @staticmethod
        def _kelvin_to_celsius(kelvin) -> float:
            return kelvin - 273.15

        @staticmethod
        def _celsius_to_fahrenheit(celsius) -> float:
            return 1.8 * celsius + 32

        @staticmethod
        def _kelvin_to_fahrenheit(kelvin) -> float:
            return MainWeatherInfo._celsius_to_fahrenheit(
                MainWeatherInfo._kelvin_to_celsius(kelvin)
            )

        @staticmethod
        def __unithandler(unit: TemperatureUnit, temperature_value: float) -> float:
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
