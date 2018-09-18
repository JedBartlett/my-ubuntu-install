
Installing editors
==================

Install gdebi-core - use that to install atom
---------------------------------------------

```
sudo apt install gdebi-core
wget -O atom-amd64.deb https://atom.io/download/deb
sudo gdebi atom-amd64.deb
apm install latex AtLilyPond lilycompile pdf-view
```

Link config files to my personal repo
---------------------------------------------
ln -s ./atom/config.cson ~/.atom/config.cson
ln -s ./atom/github.cson ~/.atom/github.cson
ln -s ./atom/keymap.cson ~/.atom/keymap.cson
