Visual Studio Code
==================

Installing Visual Studio Code
------------------------------

Initial setup is easy following instructions on the website:
https://code.visualstudio.com/docs/setup/linux

Copied from there:

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install apt-transport-https code
```

Link config files to my personal repo
---------------------------------------------

Remove the default settings file and replace it with a symlink

```bash
rm ~/.config/Code/User/settings.json
ln -s ./VScode/settings.json ~/.config/Code/User/settings.json
```

Install Extensions
------------------

```bash
extensions=( \
    Dart-Code.dart-code \
    DavidAnson.vscode-markdownlint \
    James-Yu.latex-workshop \
    ms-python.python ms-vscode.Go \
    rogalmic.bash-debug \
    truefire.lilypond \
    vsmobile.vscode-react-native \
    )
for i in "${extensions[@]}"; do 
    code --install-extension $i
done
```
