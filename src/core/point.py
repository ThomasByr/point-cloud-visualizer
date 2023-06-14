import re
import numpy as np

from functools import lru_cache

import random

__all__ = ['Point', 'PointFactory']


class SomewhatRandomColorGenerator:

  def __init__(self, seed: int = 42):
    self.__random = random.Random(seed)
    self.__passed: dict[int, tuple[float, float, float]] = {}

  @lru_cache(maxsize=None)
  def __call__(self, id: int = None) -> tuple[float, float, float]:
    id = id or -1
    try:
      return self.__passed[id]
    except KeyError:
      self.__passed[id] = self.__random.random(), self.__random.random(), self.__random.random()
      return self.__passed[id]


def get_maybe_rgb_color(r: int, g: int, b: int) -> tuple[int, int, int]:
  if r is not None and g is not None and b is not None:
    return r, g, b
  elif r is not None and g is not None:
    return r, g, g
  elif r is not None and b is not None:
    return r, r, b
  elif g is not None and b is not None:
    return b, g, b
  elif r is not None:
    return r, r, r
  elif g is not None:
    return g, g, g
  elif b is not None:
    return b, b, b
  else:
    raise ValueError('At least one of r, g, b must be not None')


class Point(np.ndarray):

  srcg = SomewhatRandomColorGenerator()

  def __new__(cls, x: float = 0, y: float = 0, z: float = 0, *args, **kwargs):
    """
    create a new point\\
    inherits from `np.ndarray`
    
    ## Parameters
    ```py
    >>> x : float, (optional)
    ```
    x coordinate\\
    defaults to `0`
    ```py
    >>> y : float, (optional)
    ```
    y coordinate\\
    defaults to `0`
    ```py
    >>> z : float, (optional)
    ```
    z coordinate\\
    defaults to `0`

    ## Optional Parameters
    the following parameters are optional and can be passed as keyword arguments or as positional arguments
    ```py
    >>> r, g, b : *int, (optional)
    ```
    red, green, blue color value\\
    defaults to `None`
    ```py
    >>> id : int, (optional)
    ```
    id of the class the point belongs to\\
    defaults to `None` or `-1`

    ## Returns
    ```py
    Point : new point
    ```
    """
    r = kwargs.pop('r', None)
    g = kwargs.pop('g', None)
    b = kwargs.pop('b', None)
    id = kwargs.pop('id', None)

    if r is None and len(args) > 0:
      r = args[0]
      args = args[1:]
    if g is None and len(args) > 0:
      g = args[0]
      args = args[1:]
    if b is None and len(args) > 0:
      b = args[0]
      args = args[1:]
    if id is None and len(args) > 0:
      id = args[0]
      args = args[1:]

    obj = np.array([x, y, z], dtype=float).view(cls)
    obj.__r: int = r
    obj.__g: int = g
    obj.__b: int = b
    obj.__id: int = id
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
    return self.__r

  @property
  def g(self) -> int:
    return self.__g

  @property
  def b(self) -> int:
    return self.__b

  @property
  def id(self) -> int:
    return self.__id

  def __repr__(self):
    return f'Point({self.x}, {self.y}, {self.z}) @ {self.id} | {self.r}, {self.g}, {self.b}'

  def __str__(self):
    return self.__repr__()

  def __getitem__(self, key: int | slice) -> float | np.ndarray:
    if isinstance(key, slice):
      return np.array([self[i] for i in range(*key.indices(len(self)))])
    return super().__getitem__(key)

  def __setitem__(self, key: int | slice, value: float | list[float]) -> None:
    if isinstance(key, slice):
      for i, v in zip(range(*key.indices(len(self))), value):
        self[i] = v
    else:
      super().__setitem__(key, value)

  def __delitem__(self, key: int | slice) -> None:
    if isinstance(key, slice):
      for i in range(*key.indices(len(self))):
        del self[i]
    else:
      super().__delitem__(key)

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
    x: float = None # required
    y: float = None # required
    z: float = None # required
    r: int = None
    g: int = None
    b: int = None
    id: int = None

    match = re.match(fmt, string)
    if match is None:
      raise RuntimeError('invalid fmt string format : no match')

    try:
      x = float(match.group('x'))
      y = float(match.group('y'))
      z = float(match.group('z'))
    except IndexError:
      raise RuntimeError('invalid fmt string format : x, y, z required')

    try:
      r = int(match.group('r'))
      g = int(match.group('g'))
      b = int(match.group('b'))
    except IndexError:
      pass

    try:
      id = int(match.group('id'))
    except IndexError:
      pass

    if x is None or y is None or z is None:
      raise ValueError(f'invalid string format from line \'{string}\' : x, y, z required')

    return cls(x, y, z, r=r, g=g, b=b, id=id)

  def get_color(self) -> tuple[float, float, float]:
    """
    get rbg color values\\
    returns either the color values passed in the constructor or a random color based on the id

    ## Returns
    ```py
    tuple[float, float, float] : (r, g, b) in range [0, 1]
    ```
    """
    if self.__r is None or self.__g is None or self.__b is None:
      return self.srcg(self.__id)
    else:
      r, g, b = get_maybe_rgb_color(self.__r, self.__g, self.__b)
      return r / 255., g / 255., b / 255.

  @staticmethod
  def new(x: float, y: float, z: float, o1: 'Point', o2: 'Point') -> 'Point':
    """
    creates a new point from a new x, y, z and the data from either o1 or o2 from wich ever is not None

    ## Parameters
    ```py
    >>> x : float
    ```
    new x coordinate
    ```py
    >>> y : float
    ```
    new y coordinate
    ```py
    >>> z : float
    ```
    new z coordinate
    ```py
    >>> o1 : Point
    ```
    point 1
    ```py
    >>> o2 : Point
    ```
    point 2

    ## Returns
    ```py
    Point : new Point object
    ```
    """
    return Point(x, y, z, r=o1.r or o2.r, g=o1.g or o2.g, b=o1.b or o2.b, id=o1.id or o2.id)

  # yapf: disable
  def __add__(self, other: 'Point') -> 'Point':
    return Point.new(self.x + other.x, self.y + other.y, self.z + other.z, self, other)
  def __sub__(self, other: 'Point') -> 'Point':
    return Point.new(self.x - other.x, self.y - other.y, self.z - other.z, self, other)
  def __mul__(self, other: 'Point') -> 'Point':
    return Point.new(self.x * other.x, self.y * other.y, self.z * other.z, self, other)
  def __truediv__(self, other: 'Point') -> 'Point':
    return Point.new(self.x / other.x, self.y / other.y, self.z / other.z, self, other)
  def __floordiv__(self, other: 'Point') -> 'Point':
    return Point.new(self.x // other.x, self.y // other.y, self.z // other.z, self, other)
  def __mod__(self, other: 'Point') -> 'Point':
    return Point.new(self.x % other.x, self.y % other.y, self.z % other.z, self, other)
  def __pow__(self, other: 'Point') -> 'Point':
    return Point.new(self.x ** other.x, self.y ** other.y, self.z ** other.z, self, other)
  def __lshift__(self, other: 'Point') -> 'Point':
    return Point.new(self.x << other.x, self.y << other.y, self.z << other.z, self, other)
  def __rshift__(self, other: 'Point') -> 'Point':
    return Point.new(self.x >> other.x, self.y >> other.y, self.z >> other.z, self, other)
  def __and__(self, other: 'Point') -> 'Point':
    return Point.new(self.x & other.x, self.y & other.y, self.z & other.z, self, other)
  def __xor__(self, other: 'Point') -> 'Point':
    return Point.new(self.x ^ other.x, self.y ^ other.y, self.z ^ other.z, self, other)
  def __or__(self, other: 'Point') -> 'Point':
    return Point.new(self.x | other.x, self.y | other.y, self.z | other.z, self, other)
  def __neg__(self) -> 'Point':
    return Point(-self.x, -self.y, -self.z, r=self.r, g=self.g, b=self.b, id=self.id)
  def __pos__(self) -> 'Point':
    return Point(+self.x, +self.y, +self.z, r=self.r, g=self.g, b=self.b, id=self.id)
  def __abs__(self) -> 'Point':
    return Point(abs(self.x), abs(self.y), abs(self.z), r=self.r, g=self.g, b=self.b, id=self.id)
  def __invert__(self) -> 'Point':
    return Point(~self.x, ~self.y, ~self.z, r=self.r, g=self.g, b=self.b, id=self.id)
  # yapf: enable

  # yapf: disable
  def __eq__(self, other: 'Point') -> bool:
    return self.x == other.x and self.y == other.y and self.z == other.z
  def __ne__(self, other: 'Point') -> bool:
    return self.x != other.x or self.y != other.y or self.z != other.z
  def __lt__(self, other: 'Point') -> bool:
    return self.x < other.x and self.y < other.y and self.z < other.z
  def __le__(self, other: 'Point') -> bool:
    return self.x <= other.x and self.y <= other.y and self.z <= other.z
  def __gt__(self, other: 'Point') -> bool:
    return self.x > other.x and self.y > other.y and self.z > other.z
  def __ge__(self, other: 'Point') -> bool:
    return self.x >= other.x and self.y >= other.y and self.z >= other.z
  def __bool__(self) -> bool:
    return bool(self.x or self.y or self.z)
  def __len__(self) -> int:
    return 3
  # yapf: enable


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
    """
    self.__fmt = fmt
    self.__make_groups()

  def __make_groups(self):
    self.__fmt = self.__fmt.replace('{x}', '(?P<x>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{y}', '(?P<y>[-+]?[0-9]*\.?[0-9]+)')
    self.__fmt = self.__fmt.replace('{z}', '(?P<z>[-+]?[0-9]*\.?[0-9]+)')

    self.__fmt = self.__fmt.replace('{r}', '(?P<r>[0-9]+)')
    self.__fmt = self.__fmt.replace('{g}', '(?P<g>[0-9]+)')
    self.__fmt = self.__fmt.replace('{b}', '(?P<b>[0-9]+)')

    self.__fmt = self.__fmt.replace('{id}', '(?P<id>[-+]?[0-9]+)')

    i = self.__fmt.count('{?}')
    while i > 0:
      self.__fmt = self.__fmt.replace('{?}', f'(?P<ignore{i}>.+?)', 1)
      i -= 1

  def __call__(self, string: str) -> Point:
    return Point.from_factory(string, self.__fmt)
