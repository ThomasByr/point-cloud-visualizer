from src.core.config import Config


def test_default():
  c = Config(file_path='somewhere.txt')
  assert c.file_path == 'somewhere.txt'
  assert c.source_xyz == (0, 0, 0)
  assert c.pattern == '{?},{x},{y},{z}'
  assert c.skip_first_line == True


def test_from_json():
  json_data = {
    'file_path': 'somewhere.txt',
    'source_xyz': (1, 2, 3),
    'pattern': '{x},{y},{z}',
    'skip_first_line': False
  }
  c = Config.from_json(json_data)
  assert c.file_path == 'somewhere.txt'
  assert c.source_xyz == (1, 2, 3)
  assert c.pattern == '{x},{y},{z}'
  assert c.skip_first_line == False


def test_from_multiple_json():
  json_data = {
    'file_path': 'somewhere_else.txt',
    'pattern': '{x},{y},{z}',
  }
  c = Config.from_json(json_data,
                       file_path='somewhere.txt',
                       source_xyz=(1, 2, 3),
                       pattern='{?},{x},{y},{z}',
                       skip_first_line=False)
  assert c.file_path == 'somewhere_else.txt'
  assert c.source_xyz == (1, 2, 3)
  assert c.pattern == '{x},{y},{z}'
  assert c.skip_first_line == False
