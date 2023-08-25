from src.core.point import *


def test_create_point():
  p1 = Point()
  p2 = Point(1, 2, 3)
  p3 = Point(2, 2, 2)

  p4 = p2 + p3
  assert p1.x == 0 and p1.y == 0 and p1.z == 0
  assert p4 == Point(3, 4, 5)


def test_from_string():
  factory = PointFactory('{x},{y},{z}')
  p = factory('1,2,3')
  assert p == Point(1, 2, 3)

  factory = PointFactory('{x} {y} {z}')
  p = factory('1 2 3')
  assert p == Point(1, 2, 3)

  factory = PointFactory('{?} {x} {y} {z}')
  p = factory('bonjour 1 2 3')
  assert p == Point(1, 2, 3)

  factory = PointFactory('{x} {?} {y} {z}')
  p = factory('1 bonjour 2 3')
  assert p == Point(1, 2, 3)

  factory = PointFactory('{z},{y},{x}')
  p = factory('3,2,1')
  assert p == Point(1, 2, 3)

  factory = PointFactory('{x} {?} {y} {?} {z}')
  p = factory('1 bonjour 2 bonjour 3')
  assert p == Point(1, 2, 3)


def test_from_string_hard():
  factory = PointFactory('{x},{y},{z}')
  p = factory('1.123,2.123,3.123')
  assert p == Point(1.123, 2.123, 3.123)

  factory = PointFactory('{?},{x},{y},{z}')
  p = factory('1798,-1008.445443,968.787257,52.500958')

  factory = PointFactory('{?},{x},{y},{z},{?},{?},{?},{id}')
  p = factory('1798,-1008.445443,968.787257,52.500958,2,3,5,-1')


def test_from_string_with_source():
  factory = PointFactory('{x},{y},{z},{X},{Y},{Z}')
  p = factory('1,2,3,4,5,6')
  assert p == Point(5, 7, 9)

  p = factory('0,0,0,4,5,6')
  assert p == Point(4, 5, 6)
