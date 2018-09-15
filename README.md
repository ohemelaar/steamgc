# Steam Games Categorizer

A Python script that fetches info about your Steam games and then generates tags accordingly.

**WARNING:** Manually changing your *sharedconfig.vdf* file can alter some Steam data like your play times. Use at your own risk.

## How to use it (short version)

1. Have Python 3.
1. Clone this repository.
1. Assign a temporary category to all your Steam games then close Steam.
1. Copy Steam's `sharedconfig.vdf` file to the root of the cloned repository.
1. Launch `steamgc.py`.
1. Replace Steam's `sharedconfig.vdf` with the the newly generated `sharedconfig.vdf.new`.

## How to use it (detailed version)

1. Be sure to have Python 3 (I use 3.6.5).
1. Clone this repository.
1. Assign a temporary category to all your games in Steam. This will force them to register in the `sharedconfig.vdf`file. Then, completely close Steam.
1. Copy your `sharedconfig.vdf` file in the root of this repository. On Ubuntu this file is located at `~/.steam/steam/userdata/<userid>/7/remote/sharedconfig.vdf`
1. Launch `steamgc.py`. On Ubuntu, this can be done by executing `./steamgc.py`.
1. Once the process is over, copy the newly created `sharedconfig.vdf.new` to the location of Steam's `sharedconfig.vdf` file, renaming it in the process.

## TODO

- Automatically fetch the .vdf file
- Merge/filter some tags (a run on a 360 games library yielded more than 400 different tags, beating the purpose of the script)
- Add options such as keeping the existing tags, tags format and prefixes
- Test the script on Windows and then add detailed README instructions for both platforms
- Check whether there is a limit for Steam store requests and eventually speed up the scrapper by sending multiple requests at the same time
- Make it available on pip
- Make a TUI, or even better a GUI
