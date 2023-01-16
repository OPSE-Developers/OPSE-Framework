Changelog v2.0.0 (2023-01-14)
=================================

Project's structure rework
----------
- Rename `RELEASES.md` to `CHANGELOG.md`
- Add `utils/init.py` for pre-checks
- Add `utils/stdin.py` for user's input
- Add `utils/stdout.py` for display
- Update `.gitignore`
- Update `README.md`
- Update `utils/config/Config.py`
- Change paths in `.gitsubmodule`
- Move `view/menu.py` into `utils/menu.py`
- Merge `exceptions/*` into `utils/exceptions.py`
- Merge `utils/Colors.py` into `utils/stdout.py`
- Merge `utils/config/default_config.py` into `Config.py`
- Merge `utils/make_research.py` into `classes/Research.py`
- Merge `Opse.py` and `core/opse.py` into `opse.py`
- Merge `utils/DataType*.py` into `utils/datatypes.py`
- Remove `RELEASES.md`
- Remove `core/` folder
- Remove `docs/*`

Concept
----------
- Add `*args` and `**kwargs` to diverse classes
- Remove Data Visibility

Webview
----------
- Remove Options page

Parser
----------
- Remove `--research` option
- Remove `--gui` option

Global Fix
----------
- Fix automatic requirements download
- Fix NoneType error
- Fix CTRL-C for API
- Fix webview crashes without names
- Fix enrich_profile active tools


Changelog v1.1.0 (2023-01-02)
=================================

GUI Rework
----------
- Now integrated into the Framework
- All pages have been redesigned
- Remove [opse.py](./opse.py) subparser. Gui is now an option (`-G` or `--gui`)

Global Fix
----------
- Fix multi input args on CLI & GUI
- Add args control (gender , birthdate)
- Handle the case where no options are entered in the CLI mode