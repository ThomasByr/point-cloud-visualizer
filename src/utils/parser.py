from argparse import ArgumentParser
from typing_extensions import override

from ..version import __version__

__all__ = ['parser']


def parser() -> ArgumentParser:

  class WeakArgsParser(ArgumentParser):

    @override
    def add_argument(self, *args, **kwargs) -> 'WeakArgsParser':
      super().add_argument(*args, **kwargs)
      return self

    def add_non_required_argument(self, *args, **kwargs) -> 'WeakArgsParser':
      kwargs['required'] = False
      return self.add_argument(*args, **kwargs)

    def add_true_false_argument(self, *args, **kwargs) -> 'WeakArgsParser':
      kwargs['action'] = 'store_true'
      if 'default' not in kwargs:
        kwargs['default'] = False
      return self.add_non_required_argument(*args, **kwargs)

    def add_path_argument(self, *args, **kwargs) -> 'WeakArgsParser':
      kwargs['type'] = str
      kwargs['metavar'] = 'PATH'
      if 'default' not in kwargs:
        kwargs['default'] = None
      return self.add_non_required_argument(*args, **kwargs)

  return WeakArgsParser(description=f'PCV - point cloud visualizer v{__version__}').add_argument(
    '-V',
    '--version',
    action='version',
    version=f'%(prog)s v{__version__}',
  ).add_true_false_argument(
    '-v',
    '--verbose',
    help='print debug messages',
  ).add_true_false_argument(
    '-i',
    '--cbid',
    help='force color by id in rendering - if both color and id are parsed (since 0.2.1) (default: False)',
  ).add_path_argument(
    '-c',
    '--cfg',
    help='path to the json config file (since 0.1.2) (default: auto-detect)',
  ).add_non_required_argument(
    '-f',
    '--frac',
    type=float,
    metavar='F',
    default=None,
    help=
    'fraction of the point cloud to be displayed - only affects rendering (since 0.2.1) (default: all points)',
  ).add_path_argument(
    '-s',
    '--save',
    help='save the current scene to a .npy file (since 0.1.2) (default: do not save)',
  ).add_true_false_argument(
    '--no-exe',
    help='do not open open3D - valid when used with --save (since 0.1.3) (default: False)',
  ).add_non_required_argument(
    '--only',
    type=int,
    metavar='N',
    default=None,
    help='only parse the first N registered files in the config file (since 0.1.3) (default: parse all)',
  )
