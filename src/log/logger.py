import logging

from .fmt import *

__all__ = ['init_logger']


def init_logger(log_lvl: int = logging.INFO) -> logging.Logger:
  """
  Initializes the logger for the application

  ## Parameters
  - `log_lvl` - int, (optional)
  the logging level (see `logging` module for more info)
  defaults to `logging.INFO`

  ## Returns
  `logging.Logger` - a new logger on the root level
  """
  logger = logging.getLogger()
  logger.setLevel(log_lvl)

  # create console handler with a higher log level
  console_handler = logging.StreamHandler()
  console_handler.setLevel(log_lvl)
  console_handler.setFormatter(UsefulFormatter())

  logger.addHandler(console_handler)
  return logger
