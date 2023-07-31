# Point Cloud Visualizer - An Open3d point cloud viewer GUI

[![Linux](https://svgshare.com/i/Zhy.svg)](https://docs.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
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
    "pattern": "{?},{x},{y},{z},{?},{?},{?},{id}",
    "skip_first_line": true
  },
  "configs": [
    {
      "file_path": "in/Adapter1.csv",
      "source_xyz": [700, 360, 100]
    },
    ...
  ]
}
```

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
python pcv.py
```

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
    <summary> (click here to expand) </summary>

</details>

## 🐛 Bugs and TODO

**TODO** (first implementation version)

- [ ] parallelize the point cloud loading from different files

**Known Bugs** (latest fix)
