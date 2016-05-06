This is an experimental Traveler RPG subsector generator.

I've cribbed rules from around the net from classic and later versions of Traveler, as I've long since lost the original copies of the rulebooks. There are a ton of mistakes and inaccuracies.

The script randomly generates worlds for a subsector (80 hexes). I've assumed a 50% chance of a world in each hex. The world UWPs are output in CSV format and an image is drawn of the subsector. 

I'm hoping to use this code to do something a bit more interesting at some point (a procedurally generated starmap maybe?).

Usage:

    python -m traveler-world-generator -v -o starmap.png -n names.txt > worlds.csv

Run `python -m traveler-world-generator --help` to see options.

A sample name file is provided - thanks to Chris Wood for the sources:

http://generators.christopherpound.com/

This script requires Python 3.5+ and Pillow.
