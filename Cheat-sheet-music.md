Converting Midi to mp3
======================
```
timidity <input>.midi -Ow -o - | lame - -b 64 <output>.mp3
```

Can't upload .mp3s to github, so:

```
zip <output>.zip *.mp3
```
