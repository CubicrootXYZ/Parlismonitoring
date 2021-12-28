import datetime
import inspect


class Logger:
    def __init__(self, log_level="info"):
        levels = {
            'debug': 0,
            'info': 100,
            'error': 200
        }

        self.levels = []

        for l, v in levels.items():
            if v >= levels[log_level]:
                self.levels.append(l)

    def debug(self, message):
        self._log(message, "debug", inspect.stack()[
                  1][0].f_locals['self'].__class__.__name__ + "." + inspect.stack()[1][3])

    def info(self, message):
        self._log(message, "info", inspect.stack()[
                  1][0].f_locals['self'].__class__.__name__ + "." + inspect.stack()[1][3])

    def error(self, message):
        self._log(message, "error", inspect.stack()[
                  1][0].f_locals['self'].__class__.__name__ + "." + inspect.stack()[1][3])

    def _log(self, message, level, caller):
        if level in self.levels:
            print(
                f"{datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')} - [{level.upper()}] {caller}: {message}")
