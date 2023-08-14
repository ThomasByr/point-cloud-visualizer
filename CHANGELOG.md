# Changelog

<summary>The full history, or so was I told...</summary>

## Title for major version

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
