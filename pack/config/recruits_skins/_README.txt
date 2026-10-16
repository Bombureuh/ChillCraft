Recruits Skins
==============

Drop ordinary Minecraft player skins in this folder and your Recruits will
wear them. Subfolders are fine -- use them to organise, they do not change anything.

What works
----------
  * PNG files, exactly 64 x 64 pixels. That is the modern skin size.
  * Classic (4-pixel arms) and slim / Alex (3-pixel arms) skins, both.
  * Hat, jacket, sleeve and trouser overlay layers all render.

Legacy 64 x 32 skins from before Minecraft 1.8 are rejected; convert one first.

Classic or slim
---------------
Nothing inside a PNG records which arm width it was drawn for, so this mod guesses
by looking at the arm pixels. To be certain, say so in the name or the folder:

  city_archer_slim.png      forced slim
  city_archer_classic.png   forced classic
  slim/city_archer.png      every skin in this folder is slim

Renaming a file changes which Recruits wear it. Repainting a file in place does not.

Turning it on
-------------
Recruits has to be using its human model. In config/recruits-client.toml set
  RecruitsLookLikeVillagers = false
and restart the game -- Recruits picks its renderer once, at startup.

After changing files here, press F3+T or run /recruitsskins reload. No restart needed.
Run /recruitsskins status if something looks wrong; it says what loaded and what did not.

Choosing which units get which skins
-----------------------------------
By default every Recruit picks from every skin in this folder, and the subfolders
above are yours to organise however you like. Nothing more is needed.

If you want desert units to look different from snowy ones, or archers different
from shieldmen, there is an optional rules file one level up:

  config/recruitsskins-rules.toml

It arrives with everything switched off and worked examples commented out. Set
  selectionMode = "rules"
in config/recruitsskins-client.toml to use it. Until you actually edit the rules
file it changes nothing at all -- every Recruit still picks from everything.

Look at a Recruit and run /recruitsskins explain to see which rule chose its skin.

Good to know
------------
These files are yours alone. Nothing is ever uploaded or downloaded, and the server
neither knows nor cares. Two players with different folders see different Recruits;
that is expected. A modpack that ships identical files and the same selectionSeed
gives everyone the same Recruits.

With no usable skins here, Recruits look exactly as Recruits itself draws them.

If you share a modpack, only include skin artwork you have permission to distribute.
