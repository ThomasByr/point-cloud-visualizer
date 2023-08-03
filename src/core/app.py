import os
import sys
import json
import signal
import logging

from typing import Any
from datetime import datetime

from open3d import visualization
from open3d import geometry
from open3d import utility

from .config import Config
from .point import *

from ..log.logger import init_logger

__all__ = ['App']


class App:

  def __init__(self, json_data_path: str = None, verbose: bool = False) -> None:
    log_lvl = logging.DEBUG if verbose else logging.INFO
    self.log = init_logger(log_lvl)

    json_data_path = json_data_path or self.__get_json_config_path()
    self.log.debug('Received json config file path (%s)', json_data_path)
    if not os.path.isfile(json_data_path):
      self.log.critical('Invalid json config file path supplied (%s)', json_data_path)
      sys.exit(1)

    self.vis = visualization.Visualizer() # pylint: disable=no-member
    self.vis.create_window(window_name='Point Cloud Visualizer', height=600, width=800)

    self.pc = geometry.PointCloud() # point cloud geometry
    self.points: list[Point] = []   # list of points (from all files)
    self.log.info('GUI up and ready 🚀')

    self.log.info('Setting up the application...')

    signal.signal(signal.SIGINT, self.__on_end) # register the signal handler
    signal.signal(signal.SIGTERM, self.__on_end)
    self.log.info('Registered handlers')

    self.__setup(json_data_path) # setup the application
    self.log.info('Application setup complete')

  def __get_json_config_path(self) -> str:
    # search for the config.json file or any .json file recursively
    found: set[str] = set()
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
      dirs[:] = list(filter(lambda d: not d.startswith(('.', '__')), dirs)) # ignore hidden directories
      for file in files:
        if file.endswith('.json'):
          found.add(os.path.join(root, file))
          if 'config.json' in file:
            return os.path.join(root, file)

    if len(found) == 0:
      self.log.critical('No json config file found in file tree')
      sys.exit(1)
    return found.pop()

  def __on_end(self, signum: int, frame: Any) -> None: # pylint: disable=unused-argument
    """
    signal handler for the SIGINT signal

    ## Parameters
    ```py
    >>> signum : int
    ```
    signal number

    ```py
    >>> frame : Any
    ```
    current stack frame
    """
    print('\r', end='')
    self.log.warning('Received %s signal ... Exiting', signal.Signals(signum).name)
    self.vis.destroy_window()
    sys.exit(0)

  def __parse_files(self, cfgs: list[Config]) -> None:
    """
    initially parse the files and store them in the database
    
    ## Parameters
    ```py
    >>> files : list[Config]
    ```
    list of configs
    """
    start_ts = datetime.now()                     # start timestamp
    for cfg in cfgs:                              # get the points from all the files
      self.points.extend(self.__load_points(cfg)) # load (somewhat slow)
    end_ts = datetime.now()                       # end timestamp

    delta_seconds = (end_ts - start_ts).total_seconds()
    self.log.info('Parsed %d points in %f s', len(self.points), round(delta_seconds, 3))

  def __load_points(self, cfg: Config) -> list[Point]:
    points: list[Point] = []                    # list of points
    offset = Point(*cfg.source_xyz, *([0] * 4)) # offset location (r,g,b,id to 0 to __add__)
    basename = os.path.basename(cfg.file_path)  # basename for logging
    self.log.debug('Loading file: ...%s', basename)
    try:
      with open(cfg.file_path, 'r', encoding='utf-8') as f:

        factory = PointFactory(cfg.pattern)     # just so that the fmt is not being parsed at every line
        start = 1 if cfg.skip_first_line else 0 # skip the first line if needed (should be the same at casting bool to int)

        for line in f.readlines()[start:]:
          try:
            points.append(factory(line) + offset)
          except Exception as e: # pylint: disable=broad-except
            self.log.critical('Failed to parse line: %s\n%s', line, e)
            sys.exit(1)

    except FileNotFoundError as e:
      self.log.error('Skipping unknown file: %s', e)
      return []
    except Exception as e: # pylint: disable=broad-except
      self.log.critical('Failed to read file: ...%s\n%s', basename, e)
      sys.exit(1)
    self.log.debug('Loaded %d points from file: ...%s', len(points), basename)
    return points

  def __create_pc_geometry(self) -> None:
    self.pc.points = utility.Vector3dVector(list(map(lambda p: p.get_xyz(), self.points)))   # pylint: disable=bad-builtin
    self.pc.colors = utility.Vector3dVector(list(map(lambda p: p.get_color(), self.points))) # pylint: disable=bad-builtin
    self.vis.add_geometry(self.pc)

    self.log.info('Created point cloud geometry')

  def __setup(self, json_data_path: str) -> None:
    """
    setup the application

    ## Parameters
    ```py
    >>> json_data_path : str
    ```
    path to the json data file
    """
    # load the json file and create the configs
    with open(json_data_path, 'r', encoding='utf-8') as f:
      raw_data = json.load(f)
    default: dict[str, Any] = raw_data['default']
    configs: list[dict[str, Any]] = raw_data['configs']
    cfgs = [Config.from_json(**default, json=cfg) for cfg in configs]
    # parse the files
    self.__parse_files(cfgs)
    # create the point cloud geometry
    self.__create_pc_geometry()

  def run(self) -> None:
    """
    run the gui
    """
    running = True
    while running:
      running = self.vis.poll_events()
      self.vis.update_geometry(self.pc)
      self.vis.update_renderer()

    self.vis.destroy_window()
