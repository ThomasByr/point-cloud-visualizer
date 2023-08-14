from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = ['Config']


@dataclass
class Config:
  file_path: str
  source_xyz: tuple[float, float, float] = (0, 0, 0)
  pattern: str = '{?},{x},{y},{z}'
  skip_first_line: bool = True

  def __post_init__(self):
    if not isinstance(self.file_path, str):
      raise TypeError('file_path must be a str')

    if not isinstance(self.source_xyz, (list, tuple)):
      raise TypeError('source_xyz must be a tuple')
    if len(self.source_xyz) != 3:
      raise ValueError('source_xyz must be a tuple of length 3')
    if not all(isinstance(x, (int, float)) for x in self.source_xyz):
      raise TypeError('source_xyz must be a tuple of float')

    if not isinstance(self.pattern, str):
      raise TypeError('pattern must be a str')

    if not isinstance(self.skip_first_line, bool):
      raise TypeError('skip_first_line must be a bool')

  @classmethod
  def from_json(cls, json: dict[str, Any] = None, **kwargs) -> 'Config':
    """
    create a Config from a json object

    ## Parameters
    ```py
    >>> json : dict[str, Any]
    ```
    case specific json object\\
    overrides any default values passed in kwargs

    ## Returns
    ```py
    Config : new Config object
    ```
    """
    if json:
      kwargs.update(json)
    return cls(**kwargs)
