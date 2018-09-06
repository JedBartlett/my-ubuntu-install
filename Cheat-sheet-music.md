Converting Midi to mp3
======================

timidity <input>.midi -Ow -o - | lame - -b 64 <output>.mp3
