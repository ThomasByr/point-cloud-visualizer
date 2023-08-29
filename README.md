# Point Cloud Visualizer - An Open3d point cloud viewer GUI

[![Linux](https://svgshare.com/i/Zhy.svg)](https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![GitHub license](https://img.shields.io/github/license/ThomasByr/point-cloud-visualizer)](https://github.com/ThomasByr/point-cloud-visualizer/blob/master/LICENSE)
[![GitHub commits](https://badgen.net/github/commits/ThomasByr/point-cloud-visualizer)](https://GitHub.com/ThomasByr/point-cloud-visualizer/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/ThomasByr/point-cloud-visualizer)](https://gitHub.com/ThomasByr/point-cloud-visualizer/commit/)
[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/ThomasByr/point-cloud-visualizer/graphs/commit-activity)

[![Python Package](https://github.com/ThomasByr/point-cloud-visualizer/actions/workflows/python-package.yml/badge.svg)](https://github.com/ThomasByr/point-cloud-visualizer/actions/workflows/python-package.yml)
[![GitHub release](https://img.shields.io/github/release/ThomasByr/point-cloud-visualizer)](https://github.com/ThomasByr/point-cloud-visualizer)
[![Author](https://img.shields.io/badge/author-@ThomasByr-blue)](https://github.com/ThomasByr)

1. [✏️ In short](#️-in-short)
2. [👩‍🏫 Usage \& Setup](#-usage--setup)
3. [⚗️ Testing](#️-testing)
4. [⚖️ License](#️-license)
5. [🔄 Changelog](#-changelog)
6. [🐛 Bugs and TODO](#-bugs-and-todo)

## ✏️ In short

This project is a simple GUI for visualizing raw-text point-clouds using the [Open3d](http://www.open3d.org/) library. It is meant to be used with a config file to load multiple point clouds at once. It also supports downsampling and saving the point cloud in a numpy array format.

Just provide a `config.json` file (supported schemes are json, jsonc, json5) following the model :

```json5
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

Allowed fields for the `pattern` property are (`x`, `y`, `z` are mandatory) :

- `{?}` : anything we want to skip
- `{x}` : x coordinate of the point (float)
- `{y}` : y coordinate '''
- `{z}` : z coordinate '''
- `{r}` : red color component (int 0..=255)
- `{g}` : green color component '''
- `{b}` : blue color component '''
- `{X}` : the x coordinate of the source point (float)  (\*)
- `{Y}` : the y coordinate of the source point (float)
- `{Z}` : the z coordinate of the source point (float)
- `{id}` : id of the object (int)(\*\*)

(\*) _if one of `{X}`, `{Y}` or `{Z}` is specified, all of them must be_

(\*\*) _the id will be used to color the points in rendering if all color components are omitted_

`pattern` and `skip_first_line` fields can be overwritten in the `configs` array if needed. `source_xyz` is the position of the sensor in the scene and only `file_path` is not set by default

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

You do not explicitly need a conda environment for the app to run. But it is always recommended nontheless, especially because the next LTS of Ubuntu won't let users pip-install anything without a virtual environment. At the time of writing, this app requires `python >= 3.8` to run. Note that because of open3d, we do not support python 3.11 yet. Furthermore, support has been removed for python 3.6 and 3.7.

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
python pcv.py -vips out/point_cloud.npy
```

<!-- markdownlint-disable MD051 -->

| argument (\*)                               | hint                                               | default             |
| ------------------------------------------- | -------------------------------------------------- | ------------------- |
| `-h` or `--help`                            | show help message **and exit**                     |                     |
| `-V` or `--version`                         | show program's version number **and exit**         |                     |
| `-v` or `--verbose`                         | increase output verbosity                          |                     |
| `-i` or `--cbid`                            | force color by id (if color components are parsed) |                     |
| `-c` or `--cfg` [PATH]                      | path to the config file                            | auto detect in tree |
| `-f` or `--frac` [F] [\*][1]                | fraction of points for downsampling                |                     |
| `-r` or `--voxel-size` [S] [\*][1]          | voxel size for downsampling                        |                     |
| `-d` or `--downsample`                      | feed back downsample to the saved point cloud      | render only         |
| `-s` or `--save` [PATH]                     | path to .npy file                                  | do not save scene   |
| `-p` or `--make-parent`                     | create parent directories if needed (for `--save`) |                     |
| `--no-exe`                                  | do not execute the app (if `--save`)               |                     |
| `--only` [(<=?N)\|(N(-N)?)(,\\s\*N(-N)?)\*] | only parse some entries of the config file (\*\*)  | parse all entries   |

[1]: ## "frac and voxel-size are mutually exclusive"

<!-- markdownlint-enable MD051 -->

(\*) _[...] means the argument expects a value if specified ; no arguments are required for the app to run_

(\*\*) _`N` is an integer, `<=N` means "less than or equal to N", eg. `only "<=3,5-7"` will parse the first 3 entries and the entries 5, 6 and 7 (note that both "-" endpoints are included)_

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

This project also includes the following notable packages and libraries:

- [Open3d](http://www.open3d.org/) (MIT License)
- [Numpy](https://numpy.org/) (BSD-3-Clause License)
- [PyJson5](https://github.com/Kijewski/pyjson5) (Apache License 2.0)
- [alive_progress](https://github.com/rsalmei/alive-progress) (MIT License)

## 🔄 Changelog

Please read the [changelog](changelog.md) file for the full history !

<details>
  <summary>  v0 - test release (click here to expand) </summary>

**v0.1** first working version

- implemented auto detect for the config file (basic recursive search in non-hidden directories)
- added a proper cli
- `--save`, `--no-exe` and `--only` options in v0.1.3
- more checks for command line arguments
- repo made public

**v0.2** a more complete version

- added `--cbid` and `--frac` to affect rendering _only_
- the parser is no longer bloating the main file
- fixed a bug where points where created with wrong color
- modified `--only` to accept range (type `--only "<=N"` for older behavior)
- support for json5 config files
- `--make_parent` option to not fail if the parent directory in `--save` does not exist

**v0.3** wide python support

- support for python 3.8 to 3.10 (removed 3.6 and 3.7)
- fixed artifacts from previous support
- passive wait for the window to close (see [known bugs](README.md#-bugs-and-todo))
- added `--voxel-size` as an alternative to `--frac`
- `--downsample` option to feed back the downsampling onto the saved file (previously, downsampling was only applied to the rendering)
- delayed import of open3d to speed up the cli
- complete refactoring of the logging system + check for color support
- made the "=" in "<=" for `--only` optional
- added "{X}", "{Y}" and "{Z}" to the pattern for the config file
- if both "source_xyz" and "{X}", "{Y}" and "{Z}" are present, the origin takes both into account
- new alive progress indicator based on pip (see [alive-progress](https://github.com/rsalmei/alive-progress))

</details>

## 🐛 Bugs and TODO

**TODO** (first implementation version)

- [ ] parallelize the point cloud loading from different files
- [ ] add support for other file formats (las, ply, etc.)
- [x] `{X}`, `{Y}` and `{Z}` fields in pattern for the position of the sensor (v0.3.5)

**Known Bugs** (latest fix)

- main thread is blocked while the gui is running
  - only manual closing of the window is possible
  - signal handling is not working
- alive progress bar does not supports color
