import logging

class Logger(logging.Logger):
    """Custom class to log data into files"""
    def __init__(self, name: str, package: str, level):
        super().__init__(name)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            filename=f'logs/{package}.log', encoding='utf-8', level=level)
        self.logging = logging

    def get_logging(self):
        return self.logging


