class StreamStatsError(Exception):
    pass


class UnsupportedFormatError(StreamStatsError):
    pass


class InvalidEventError(StreamStatsError):
    pass


class InvalidTimePointError(StreamStatsError):
    pass


class ConfigCLIError(StreamStatsError):
    pass
