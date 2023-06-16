import os
import sys
import json
import signal

# from multiprocessing.pool import ThreadPool

from typing import Any
from datetime import datetime

from open3d import visualization
from open3d import geometry
from open3d import utility

from .config import Config
from .point import *

from ..log.logger import logger as log

__all__ = ['App']


class App:

  def __init__(self, json_data_path: str = None) -> None:
    json_data_path = json_data_path or self.__get_json_config_path()

    self.vis = visualization.Visualizer()
    self.vis.create_window(window_name='Point Cloud Visualizer', height=600, width=800)

    self.pc = geometry.PointCloud()
    self.points: list[Point] = []
    log.info('GUI up and ready 🚀')

    log.info('Setting up the application...')

    signal.signal(signal.SIGINT, self.__on_end) # register the signal handler
    signal.signal(signal.SIGTERM, self.__on_end)
    log.info('Registered handlers')

    self.__setup(json_data_path) # setup the application
    log.info('Application setup complete')

  def __get_json_config_path(self) -> str:
    # search for the config.json file or any .json file recursively
    found: set[str] = set()
    for root, _, files in os.walk(os.getcwd()):
      for file in files:
        if file.endswith('.json'):
          found.add(os.path.join(root, file))
          if 'config.json' in file:
            return os.path.join(root, file)

    if len(found) == 0:
      log.critical('No json config file found')
      sys.exit(1)
    return found.pop()

  def __on_end(self, signum: int, frame: Any) -> None:
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
    frame
    """
    print('\r', end='')
    log.warning(f'Received {signal.Signals(signum).name} signal ... Exiting')
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
    start_ts = datetime.now()
    # thp = ThreadPool(processes=os.cpu_count() or 1) # should be the default but just in case ...

    # for cfg in cfgs:
    #   thp.apply_async(self.__load_points, (cfg,), callback=self.points.extend)
    # thp.close()
    # thp.join()

    for cfg in cfgs:
      self.points.extend(self.__load_points(cfg))

    end_ts = datetime.now()

    delta_seconds = (end_ts - start_ts).total_seconds()
    log.info(f'Parsed {len(self.points):_} points in {delta_seconds:.2f} s')

  @staticmethod
  def __load_points(cfg: Config) -> list[Point]:
    points: list[Point] = []
    offset = Point(*cfg.source_xyz)
    with open(cfg.file_path, 'r', encoding='utf-8') as f:

      factory = PointFactory(cfg.pattern)     # just so that the fmt is not being parsed at every line
      start = 1 if cfg.skip_first_line else 0 # skip the first line if needed (should be the same at casting bool to int)

      for line in f.readlines()[start:]:
        try:
          points.append(factory(line) + offset)
        except Exception as e:
          log.critical(f'Failed to parse line: {line}\n{e}')
          sys.exit(1)
    return points

  def __create_pc_geometry(self) -> None:
    self.pc.points = utility.Vector3dVector(self.points)
    self.pc.colors = utility.Vector3dVector(list(map(lambda p: p.get_color(), self.points)))
    self.vis.add_geometry(self.pc)

    log.info('Created point cloud geometry')

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
    cfgs = [Config.from_json(cfg, **default) for cfg in configs]
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
