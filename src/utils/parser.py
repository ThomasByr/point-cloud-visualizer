from argparse import ArgumentParser

from ..version import __version__

__all__ = ['parser']


def parser() -> ArgumentParser:

  p = ArgumentParser(description=f'PCV - point cloud visualizer v{__version__}')
  p.add_argument(
    '-V',
    '--version',
    action='version',
    version=f'%(prog)s v{__version__}',
  )
  p.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    default=False,
    required=False,
    help='print debug messages',
  )
  p.add_argument(
    '-i',
    '--cbid',
    action='store_true',
    default=False,
    required=False,
    help='force color by id in rendering - if both color and id are parsed (since 0.2.1) (default: False)',
  )
  p.add_argument(
    '-c',
    '--cfg',
    type=str,
    metavar='PATH',
    default=None,
    required=False,
    help='path to the json config file (since 0.1.2) (default: auto-detect)',
  )
  p.add_argument(
    '-f',
    '--frac',
    type=float,
    metavar='F',
    default=None,
    required=False,
    help=
    'fraction of the point cloud to be displayed - only affects rendering (since 0.2.1) (default: all points)',
  )
  p.add_argument(
    '-s',
    '--save',
    type=str,
    metavar='PATH',
    default=None,
    required=False,
    help='save the current scene to a .npy file (since 0.1.2) (default: do not save)',
  )
  p.add_argument(
    '--no-exe',
    action='store_true',
    default=False,
    required=False,
    help='do not open open3D - valid when used with --save (since 0.1.3) (default: False)',
  )
  p.add_argument(
    '--only',
    type=int,
    metavar='N',
    default=None,
    required=False,
    help='only parse the first N files registers in the config file (since 0.1.3) (default: parse all)',
  )
  return p
