This is an experimental Traveler RPG subsector generator.

I've cribbed rules from around the net from classic and later versions of Traveler, as I've long since lost the original copies of the rulebooks. So I'm sure there are a ton of mistakes and inaccuracies.

The script randomly generates worlds for a subsector (80 hexes). I've assumed a 50% chance of a world in each hex. The world UWPs are dumpted to screen and an image is drawn of the subsector. 

I'm hoping to use this code to do something more interesting later (a procedurally generated starmap maybe?).

Usage:

python -m traveler-world-generator -v -o starmap.png -n names.txt

-v --verbose: Print long descriptions of planets (otherwise just prints UWP)
-o --output: Output file of starmap
-n --names: Text file of names. Names should be one per line, minimum 80 names. If omitted worlds will not be named.

A sample name file is provided: thanks to Chris Wood for the sources:

http://generators.christopherpound.com/
