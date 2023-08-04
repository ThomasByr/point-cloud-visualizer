# Point Cloud Visualizer - An Open3d point cloud viewer GUI

[![Linux](https://svgshare.com/i/Zhy.svg)](https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![GitHub license](https://img.shields.io/github/license/ThomasByr/point-cloud-visualizer)](https://github.com/ThomasByr/point-cloud-visualizer/blob/master/LICENSE)
[![GitHub commits](https://badgen.net/github/commits/ThomasByr/point-cloud-visualizer)](https://GitHub.com/ThomasByr/point-cloud-visualizer/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/ThomasByr/point-cloud-visualizer)](https://gitHub.com/ThomasByr/point-cloud-visualizer/commit/)
[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/ThomasByr/point-cloud-visualizer/graphs/commit-activity)

[![Python Package Conda&Hatch](https://github.com/ThomasByr/point-cloud-visualizer/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/ThomasByr/point-cloud-visualizer/actions/workflows/python-package-conda.yml)
[![GitHub version](https://badge.fury.io/gh/ThomasByr%2Fpoint-cloud-visualizer.svg)](https://github.com/ThomasByr/point-cloud-visualizer)
[![Author](https://img.shields.io/badge/author-@ThomasByr-blue)](https://github.com/ThomasByr)

1. [✏️ In short](#️-in-short)
2. [👩‍🏫 Usage \& Setup](#-usage--setup)
3. [⚗️ Testing](#️-testing)
4. [⚖️ License](#️-license)
5. [🔄 Changelog](#-changelog)
6. [🐛 Bugs and TODO](#-bugs-and-todo)

## ✏️ In short

This project is a simple GUI for visualizing point clouds using the [Open3d](http://www.open3d.org/) library. This tool is written in Python.

Just provide a `config.json` file (in a "data" directory for eg.) following the model :

```json
{
  "default": {
    "pattern": "{?},{x},{y},{z},{r},{g},{b},{id}",
    "skip_first_line": true
  },
  "configs": [
    {
      "file_path": "<path to file n°1>.csv",
      "source_xyz": [<x1>, <y1>, <z1>]
    },
    {
      "file_path": "<path to file n°2>.csv",
      "source_xyz": [<x2>, <y2>, <z2>]
    },
    ...
  ]
}

```

Allowed fields for the `pattern` property are :

- `{?}` : anything we want to skip
- `{x}` : x coordinate of the point (float)
- `{y}` : y coordinate '''
- `{z}` : z coordinate '''
- `{r}` : red color component (int 0..=255)
- `{g}` : green color component '''
- `{b}` : blue color component '''
- `{id}` : id of the object (int)(\*)

(\*) _the id will be used to color the points in rendering if all color components are omitted_

`pattern` and `skip_first_line` fields can be overwritten in the `configs` array if needed. `source_xyz` is the position of the sensor in the scene.

Then obviously, you will need the point clouds files in a text file format (csv, txt, etc.) with the corresponding format :

```csv
---,XCoordinate,YCoordinate,ZCoordinate,RColor,GColor,BColor,ObjectID
0,-200.857966,-0.472143,10.636364,25,42,72,19
1,-202.754359,-0.273832,11.529021,25,42,72,19
...
```

## 👩‍🏫 Usage & Setup

> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> Please note we do not officially support Windows or MacOS, but we do provide some instructions for those who want to use it on these platforms.

You do not explicitly need a conda environment for the bot to run. But it is always recommended nontheless, especially because the next LTS of Ubuntu won't let users pip-install anything without a virtual environment. At the time of writing, this app requires `python >= 3.10` to run.

```bash
# Clone the repository
git clone git@github.com:ThomasByr/point-cloud-visualizer.git
cd point-cloud-visualizer
```

You can create and activate a conda environment with the following commands :

```bash
# Create the environment and install the dependencies
conda env create -f environment.yml
conda activate o3d
```

Finally, run the app by typing the following :

```bash
# Run app
python pcv.py -vis point_cloud.npy
```

| argument (\*)               | hint                                                  | default             |
| ----------------------- | ----------------------------------------------------- | ------------------- |
| `-h` or `--help`        | show help message **and exit**                        |                     |
| `-V` or `--version`     | show program's version number **and exit**            |                     |
| `-v` or `--verbose`     | increase output verbosity                             |                     |
| `-i` or `--cbid`        | force color by id (if color components are parsed)    |                     |
| `-c` or `--cfg` [PATH]  | path to the config file                               | auto detect in tree |
| `-f` or `--frac` [F]    | fraction of points to render (does not affect saving) | `1.0`               |
| `-s` or `--save` [PATH] | path to .npy file                                     | do not save scene   |
| `--no-exe`              | do not execute the app (if `--save`)                  |                     |
| `--only` [N]            | only parse the first N entries of the config file     | parse all entries   |

(\*) _[...] means the argument expects a value if specified ; but no arguments are required for the app to run_

## ⚗️ Testing

Make sure you have installed the dependencies for testing :

```bash
# inside conda environment
pip install -r requirements-dev.txt
```

Then, run the tests with the following command :

```bash
hatch run dev:check
```

or more manually :

```bash
python -m pytest
python -m pylint src
python -m yapf -dr src
```

## ⚖️ License

This project is licensed under the AGPL-3.0 new or revised license. Please read the [LICENSE](LICENSE.md) file. Additionally :

- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

- Neither the name of the point-cloud-visualizer authors nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

```LICENSE
Point Cloud Visualizer - An Open3d point cloud viewer GUI
Copyright (C) 2023 Thomas BOUYER

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
```

## 🔄 Changelog

Please read the [changelog](changelog.md) file for the full history !

<details>
  <summary>  Title for major version (click here to expand) </summary>

**v0.1** first working version

- implemented auto detect for the config file (basic recursive search in non-hidden directories)
- added a proper cli
- `--save`, `--no-exe` and `--only` options in v0.1.3
- more checks for command line arguments
- repo made public

**v0.2** a more complete version

- added `--cbid` and `--frac` to affect rendering _only_
- the parser is no longer bloating the main file

</details>

## 🐛 Bugs and TODO

**TODO** (first implementation version)

- [ ] parallelize the point cloud loading from different files
- [ ] add support for other file formats (las, ply, etc.)
- [ ] `{X}`, `{Y}` and `{Z}` fields in pattern for the position of the sensor

**Known Bugs** (latest fix)
