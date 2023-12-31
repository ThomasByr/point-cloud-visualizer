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

if sys.version_info < (3, 8):
  raise RuntimeError('This program requires Python 3.8 or later.')

# pylint: disable=wrong-import-position
if __name__ == '__main__':
  from src.utils import parser
  n = parser().parse_args() # parse arguments before importing App
  from src.core import App  # also imports open3d and numpy which are slow
  App(n).run()              # instantiate and run App (check args here)
