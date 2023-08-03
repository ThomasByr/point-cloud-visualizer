#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#! PCV - point cloud visualizer
#!
#! Copyright (c) 2023, ThomasByr.
#! AGPL-3.0-or-later (https://www.gnu.org/licenses/agpl-3.0.en.html)
#! All rights reserved.
#!
#! Redistribution and use in source and binary forms, with or without
#! modification, are permitted provided that the following conditions are met:
#!
#! * Redistributions of source code must retain the above copyright notice,
#!   this list of conditions and the following disclaimer.
#!
#! * Redistributions in binary form must reproduce the above copyright notice,
#!   this list of conditions and the following disclaimer in the documentation
#!   and/or other materials provided with the distribution.
#!
#! * Neither the name of this software's authors nor the names of its
#!   contributors may be used to endorse or promote products derived from
#!   this software without specific prior written permission.
#!
#! This program is free software: you can redistribute it and/or modify
#! it under the terms of the GNU Affero General Public License as published by
#! the Free Software Foundation, either version 3 of the License, or
#! (at your option) any later version.
#!
#! This program is distributed in the hope that it will be useful,
#! but WITHOUT ANY WARRANTY; without even the implied warranty of
#! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#! GNU Affero General Public License for more details.
#!
#! You should have received a copy of the GNU Affero General Public License
#! along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from argparse import ArgumentParser

if sys.version_info < (3, 10):
  raise RuntimeError('This program requires Python 3.10 or later.')


def parser() -> ArgumentParser:
  from src.version import __version__

  parser = ArgumentParser(description=f'PCV - point cloud visualizer v{__version__}')
  parser.add_argument(
    '-V',
    '--version',
    action='version',
    version=f'%(prog)s v{__version__}',
  )
  parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    default=False,
    required=False,
    help='print debug messages',
  )
  parser.add_argument(
    '-c',
    '--cfg',
    type=str,
    metavar='PATH',
    default=None,
    required=False,
    help='path to the json config file (since 0.1.2) (default: auto-detect)',
  )
  parser.add_argument(
    '-s',
    '--save',
    type=str,
    metavar='PATH',
    default=None,
    required=False,
    help='save the current scene to a .npy file (since 0.1.2) (default: do not save)',
  )
  parser.add_argument(
    '--no-exe',
    action='store_true',
    default=False,
    required=False,
    help='do not open open3D - valid when used with --save (since 0.1.3) (default: False)',
  )
  parser.add_argument(
    '--only',
    type=int,
    metavar='N',
    default=None,
    required=False,
    help='only parse the first N files registers in the config file (since 0.1.3) (default: parse all)',
  )
  return parser


if __name__ == '__main__':
  from src import *

  args = parser().parse_args()
  app = App(args) # create and run app
