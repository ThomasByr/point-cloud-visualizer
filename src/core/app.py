from __future__ import annotations

import os
import sys
import signal
import logging
import random
from threading import Thread

from typing import Any
from datetime import datetime

from argparse import Namespace
from dataclasses import dataclass
from open3d import visualization
from open3d import geometry
from open3d import utility

import pyjson5
import numpy as np

from .config import Config
from .point import *

from ..log.logger import init_logger

__all__ = ['App']


@dataclass
class Args:
  verbose: bool         # verbose logging
  cbid: bool            # force color by id
  cfg: str | None       # config path
  frac: float | None    # fraction of points to render
  save: str | None      # save path
  make_parent: bool     # make parent directory of save path if it does not exist
  no_exe: bool          # no gui
  only: set[int] | None # only parse this many files


class App:

  def __init__(self, args: Namespace) -> None:
    self.__check_args(args)
    self.args = Args(
      verbose=args.verbose,
      cbid=args.cbid,
      cfg=args.cfg or self.__get_json_config_path(),
      frac=args.frac,
      save=args.save,
      make_parent=args.make_parent,
      no_exe=args.no_exe,
      only=args.only,
    )

    log_lvl = logging.DEBUG if self.args.verbose else logging.INFO
    self.log = init_logger(log_lvl)
    self.log.debug('Received json config file path (%s)', self.args.cfg)
    if not os.path.isfile(self.args.cfg):
      self.log.critical('Invalid json config file path supplied (%s)', self.args.cfg)
      sys.exit(1)

    self.vis: visualization.Visualizer = None
    self.pc: geometry.PointCloud = None     # point cloud geometry
    if not self.args.no_exe:
      self.vis = visualization.Visualizer() # pylint: disable=no-member
      self.pc = geometry.PointCloud()
      self.vis.create_window(window_name='Point Cloud Visualizer', height=600, width=800)
      self.log.info('GUI up and ready 🚀')

    self.log.info('Setting up the application...')
    self.points: list[Point] = [] # list of points (from all files)

    signal.signal(signal.SIGINT, self.__on_end) # register the signal handler
    signal.signal(signal.SIGTERM, self.__on_end)
    self.log.info('Registered handlers')

    self.__setup() # setup the application
    self.log.info('Application setup complete')

    # run the gui
    self.__run()

  def __check_args(self, args: Namespace) -> None:
    """
    check the arguments passed to the application

    ## Parameters
    ```py
    >>> args : Namespace
    ```
    arguments passed to the application
    """
    if args.cbid and args.no_exe:
      raise RuntimeError('Passing --cbid with --no-exe will have no effect')
    if args.frac and args.no_exe:
      raise RuntimeError('Passing --frac with --no-exe will have no effect')
    if args.frac and (args.frac <= 0 or args.frac > 1):
      raise RuntimeError(f'Invalid value for --frac : {args.frac} (should be > 0 and <= 1)')
    if args.save and os.path.isdir(args.save):
      raise RuntimeError(f'Invalid save path supplied : {args.save} is a directory')
    if args.make_parent and not args.save:
      raise RuntimeError('Passing --make-parent without --save will do nothing')
    if args.save and not os.path.exists(os.path.dirname(args.save)):
      if args.make_parent:
        os.makedirs(os.path.dirname(args.save), exist_ok=False)
      else:
        raise RuntimeError(f'Invalid save path supplied : parent directory of {args.save} does not exist')
    if args.no_exe and not args.save:
      raise RuntimeError('Passing --no-exe without --save will do nothing')
    if args.only and any(map(lambda x: x <= 0, args.only)): # pylint: disable=bad-builtin
      raise RuntimeError(f'Invalid value for --only : {args.only} (should be > 0)')

  def __get_json_config_path(self) -> str:
    # search for the config.json file or any json file recursively
    auto_filenames = {'config', 'cfg', 'init', 'ini'}
    found: set[str] = set()
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
      dirs[:] = list(filter(lambda d: not d.startswith(('.', '__')), dirs)) # ignore hidden directories
      for file in files:
        if file.endswith(('.json', '.jsonc', '.json5')):                    # if json
          found.add(os.path.join(root, file))
          if os.path.splitext(file)[0].lower() in auto_filenames:           # if common name
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
    for cfg in cfgs:                              # get the points from all the files
      self.points.extend(self.__load_points(cfg)) # load (somewhat slow)
    end_ts = datetime.now()

    delta_seconds = (end_ts - start_ts).total_seconds()
    self.log.info('Parsed %s points in %.3f s', format(len(self.points), '_'), delta_seconds)

  def __load_points(self, cfg: Config) -> list[Point]:
    points: list[Point] = []                    # list of points
    offset = Point(*cfg.source_xyz, *([0] * 4)) # offset location (r,g,b,id to 0 for add method)
    basename = os.path.basename(cfg.file_path)  # basename for logging
    self.log.debug('Loading file: [...]/%s', basename)
    self.log.debug('Offset: %s', offset)
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
      self.log.critical('Failed to read file: %s\n%s', cfg.file_path, e)
      sys.exit(1)
    self.log.debug('Loaded %s points from file: [...]/%s', format(len(points), '_'), basename)
    return points

  def __create_pc_geometry(self) -> None:
    if self.args.no_exe:
      return

    points = self.points
    if self.args.frac:

      _start_ts = datetime.now()
      size = int(len(points) * self.args.frac)
      points = random.sample(points, size)
      _end_ts = datetime.now()
      _delta_seconds = (_end_ts - _start_ts).total_seconds()
      self.log.info('Pulled %s points randomly for rendering in %.3f s', format(len(points), '_'),
                    _delta_seconds)

    start_ts = datetime.now()
    self.pc.points = utility.Vector3dVector(map(lambda p: p.get_xyz(), points))                 # pylint: disable=bad-builtin
    self.pc.colors = utility.Vector3dVector(map(lambda p: p.get_color(self.args.cbid), points)) # pylint: disable=bad-builtin
    self.vis.add_geometry(self.pc)
    end_ts = datetime.now()

    delta_seconds = (end_ts - start_ts).total_seconds()
    self.log.info('Created point cloud geometry in %.3f s', delta_seconds)

  def __save_pc(self) -> None:

    def __save_npy(filepath: str):
      # save point data but not object data
      np.save(filepath, np.array(self.points, dtype=float), allow_pickle=False)
      self.log.info('Saved point cloud to %s', filepath)

    if self.args.save:
      # launch the save function in a separate thread
      Thread(target=__save_npy, args=(self.args.save,)).start()

  def __setup(self) -> None:
    """
    setup the application
    """
    # load the json file and create the configs
    raw_data = None
    with open(self.args.cfg, 'r', encoding='utf-8') as f:
      try:
        raw_data = pyjson5.decode_io(f, 4, some=False) # pylint: disable=no-member
      except pyjson5.Json5DecoderException as e:       # pylint: disable=no-member
        self.log.critical(
          'Failed to parse json config file : '
          'maximum nesting level could be reached, please check your file\n%s', e)
        sys.exit(1)
    default: dict[str, Any] = raw_data['default']
    configs: list[dict[str, Any]] = raw_data['configs']
    cfgs = [Config.from_json(json=cfg, **default) for cfg in configs]

    fset: list[int] = None
    if self.args.only and any(map(lambda x: x > len(cfgs), self.args.only)): # pylint: disable=bad-builtin
      fset = sorted(list(filter(lambda x: x > len(cfgs), self.args.only)))
      self.log.warning('Omitted invalid values for --only : %s', fset)

    # parse the files (slicing with None has no effect on small lists)
    if fset:
      self.args.only -= set(fset)
    self.__parse_files([cfgs[i - 1] for i in self.args.only] if self.args.only else cfgs)
    # create the point cloud geometry
    self.__create_pc_geometry()
    # save the point cloud if needed
    self.__save_pc()

  def __run(self) -> None:
    """
    run the gui
    """
    running = not self.args.no_exe
    while running:
      running = self.vis.poll_events()
      self.vis.update_geometry(self.pc)
      self.vis.update_renderer()

  def __del__(self) -> None:
    """ cleanup """
    try:
      self.vis.destroy_window()
      self.pc.clear()
    except AttributeError: # --no-exe case
      pass
