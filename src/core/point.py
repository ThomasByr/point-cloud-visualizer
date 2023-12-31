from __future__ import annotations

import re
import random
from functools import lru_cache

import logging
import numpy as np

__all__ = ['Point', 'PointFactory']


class SomewhatRandomColorGenerator:

  def __init__(self, seed: int = 42):
    self.__random = random.Random(seed)
    self.__passed: dict[int, tuple[float, float, float]] = {}

  @lru_cache(maxsize=256)
  def __call__(self, cid: int = None) -> tuple[float, float, float]:
    cid = cid or -1
    try:
      return self.__passed[cid]
    except KeyError:
      self.__passed[cid] = self.__random.random(), self.__random.random(), self.__random.random()
      return self.__passed[cid]


def get_maybe_rgb_color(r: int, g: int, b: int) -> tuple[int, int, int]:
  if r is not None and g is not None and b is not None:
    return r, g, b
  if r is not None and g is not None:
    return r, g, g
  if r is not None and b is not None:
    return r, r, b
  if g is not None and b is not None:
    return b, g, b
  if r is not None:
    return r, r, r
  if g is not None:
    return g, g, g
  if b is not None:
    return b, b, b
  raise ValueError('At least one of r, g, b must be not None')


class Point(np.ndarray):

  srcg = SomewhatRandomColorGenerator()

  def __new__(
    cls,
    x: float = 0,
    y: float = 0,
    z: float = 0,
    r: int = None,
    g: int = None,
    b: int = None,
    cid: int = None,
  ):
    """
    create a new point\\
    inherits from `np.ndarray`\\

    ## Caution
    When doing arithmetic operations, please make sure that `r`, `g`, `b` and `cid` of one of the points are `0`\\
    Otherwise, you will loose information about the color and the class id of the point\\
    `__eq__` and `__ne__` only compare the coordinates of the points
  
    ## Returns
    ```py
    Point : new point
    ```
    """
    r = -1 if r is None else r
    g = -1 if g is None else g
    b = -1 if b is None else b
    cid = -1 if cid is None else cid
    obj = np.array([x, y, z, r, g, b, cid], dtype=float).view(cls)
    return obj

  @property
  def x(self) -> float:
    return self[0]

  @x.setter
  def x(self, value: float):
    if not isinstance(value, (int, float)):
      raise TypeError('x must be a float')
    self[0] = value

  @property
  def y(self) -> float:
    return self[1]

  @y.setter
  def y(self, value: float):
    if not isinstance(value, (int, float)):
      raise TypeError('y must be a float')
    self[1] = value

  @property
  def z(self) -> float:
    return self[2]

  @z.setter
  def z(self, value: float):
    if not isinstance(value, (int, float)):
      raise TypeError('z must be a float')
    self[2] = value

  @property
  def r(self) -> int:
    return self[3]

  @property
  def g(self) -> int:
    return self[4]

  @property
  def b(self) -> int:
    return self[5]

  @property
  def id(self) -> int:
    return self[6]

  def __repr__(self):
    return f'Point({self.x}, {self.y}, {self.z}) @ {self.id} | {self.r}, {self.g}, {self.b}'

  def __str__(self):
    return self.__repr__()

  def __eq__(self, other):
    return np.array_equal(self[:3], other[:3])

  def __ne__(self, other):
    return not self == other

  @classmethod
  def from_factory(cls, string: str, fmt: str) -> 'Point':
    """
    creates a new point from a string provided by the factory\\

    ## Parameters
    ```py
    >>> string : str
    ```
    string, generally from a `readline` call
    ```py
    >>> fmt : str
    ```
    formated string provided by the factory

    ## Returns
    ```py
    Point : new point
    ```
    """
    return cls.__on_end_from(string, fmt)

  @classmethod
  def __on_end_from(cls, string: str, fmt: str) -> 'Point':
    x: float = None  # required
    y: float = None  # required
    z: float = None  # required
    r: int = None
    g: int = None
    b: int = None
    cid: int = None
    sx: float = None # if one is specified, all must be
    sy: float = None
    sz: float = None

    if (match := re.match(fmt, string)) is None:
      raise RuntimeError('invalid fmt string format : no match')

    try:
      x = float(match.group('x'))
      y = float(match.group('y'))
      z = float(match.group('z'))
    except IndexError as e:
      raise RuntimeError('invalid fmt string format : x, y, z required') from e

    try:
      r = int(match.group('r'))
    except IndexError:
      pass
    try:
      g = int(match.group('g'))
    except IndexError:
      pass
    try:
      b = int(match.group('b'))
    except IndexError:
      pass

    try:
      cid = int(match.group('id'))
    except IndexError:
      pass

    try:
      sx = float(match.group('X'))
      sy = float(match.group('Y'))
      sz = float(match.group('Z'))
    except IndexError:
      pass

    if x is None or y is None or z is None:
      raise ValueError(f'invalid string format from line \'{string}\' : x, y, z required')
    # if one of the source coordinates is specified, all must be
    if any((sx, sy, sz)):
      if not all((sx, sy, sz)):
        raise ValueError(f'invalid string format from line \'{string}\' : X, Y, Z required')
      x += sx
      y += sy
      z += sz

    return cls(x, y, z, r, g, b, cid)

  def get_color(self, cbid: bool = False) -> tuple[float, float, float]:
    """
    get rbg color values\\
    returns either the color values passed in the constructor or a random color based on the id

    ## Parameters
    ```py
    >>> cbid : bool, (optional)
    ```
    if `True`, the color will be based on the id of the point,
    otherwise, it will be the color passed in the constructor if any

    ## Returns
    ```py
    tuple[float, float, float] : (r, g, b) in range [0, 1]
    ```
    """
    if cbid or all(self[3:6] < 0):
      return self.srcg(self.id)
    r, g, b = get_maybe_rgb_color(self.r, self.g, self.b)
    return r / 255., g / 255., b / 255.

  def get_xyz(self) -> np.ndarray:
    """
    get xyz values

    ## Returns
    ```py
    tuple[float, float, float] : (x, y, z)
    ```
    """
    return self[:3]


class PointFactory:

  def __init__(self, fmt: str) -> None:
    """
    ```py
    >>> fmt : str, (optional)
    ```
    string format\\
    valid fields are:
    - `{x}`: x coordinate (float), required
    - `{y}`: y coordinate (float), required
    - `{z}`: z coordinate (float), required
    - `{r}`: red value (int between 0 and 255)
    - `{g}`: green value (int between 0 and 255)
    - `{b}`: blue value (int between 0 and 255)
    - `{id}`: unique identifier (int)
    - `{X}`: the x coordinate of the source point (float)
    - `{Y}`: the y coordinate of the source point (float)
    - `{Z}`: the z coordinate of the source point (float)
    - `{?}`: any field that would be ignored
    """
    self.log = logging.getLogger('factory')
    self.__fmt = fmt
    self.__make_groups()

  def __make_groups(self):
    self.log.debug('Received fmt string : %s', self.__fmt)

    self.__fmt = self.__fmt.replace('{x}', r'(?P<x>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{y}', r'(?P<y>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{z}', r'(?P<z>[-+]?[0-9]*\.?[0-9]+)')

    self.__fmt = self.__fmt.replace('{r}', r'(?P<r>[0-9]+)')
    self.__fmt = self.__fmt.replace('{g}', r'(?P<g>[0-9]+)')
    self.__fmt = self.__fmt.replace('{b}', r'(?P<b>[0-9]+)')

    self.__fmt = self.__fmt.replace('{id}', r'(?P<id>[-+]?[0-9]+)')

    self.__fmt = self.__fmt.replace('{X}', r'(?P<X>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{Y}', r'(?P<Y>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{Z}', r'(?P<Z>[-+]?[0-9]*\.?[0-9]+)')

    i = self.__fmt.count('{?}')
    while i > 0:
      self.__fmt = self.__fmt.replace('{?}', f'(?P<ignore{i}>.+?)', 1)
      i -= 1

  def __call__(self, string: str) -> Point:
    return Point.from_factory(string, self.__fmt)
