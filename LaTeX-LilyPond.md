
Installing TexStudio & texlive & lylauatex
==============================================================================
**References:**
- https://milq.github.io/install-latex-ubuntu-debian/
- **xzdec** is needed by the texlive package manager tlmgr to function
  properly.
- Instructions for downgrading the tlmgr repo was taken from:
  https://tex.stackexchange.com/questions/429714/tlmgr-remote-repository-is-newer-than-local-2017-2018
```
sudo apt update
sudo apt install texlive-full texstudio xzdec
# Downgrade the server used (Bionic packages are only shipping 2018 right now)
tlmgr option repository ftp://tug.org/historic/systems/texlive/2017/tlnet-final
tlmgr install lyluatex
```


Installing LilyPond
==============================================================================


```
cd ~/Downloads
wget http://download.linuxaudio.org/lilypond/binaries/linux-64/lilypond-2.18.2-1.linux-64.sh

sh lilypond-2.18.2-1.linux-64.sh

```

Then, edit ~/.bashrc to add the line:
```
PATH=~/bin:$PATH
```
and make sure that the `export $PATH` line is included at the end

**References:**
- http://lilypond.org/unix.html

Installing timidity
==============================================================================
Used for converting .midi to .mp3 files.
Soundfont is also required so that timidity has a set of instruments to play

https://unix.stackexchange.com/questions/97883/timidity-no-instrument-mapped-to-tone-bank-0-no-idea-which-one-is-missing
'''
sudo apt install timidity fluid-soundfont-gm
sudo sed -e 's|^source|#source|' -e '$a source /etc/timidity/fluidr3_gm.cfg' -i /etc/timidity/timidity.cfg
sudo /etc/init.d/timidity restart
```


Installing Frescobaldi
==============================================================================

```
sudo apt-get install frescobaldi
```

**References:**
- http://frescobaldi.org/download


Installing audivers
==============================================================================

Install JDK
---------------------------------------
```
sudo add-apt-repository ppa:webupd8team/java
sudo apt update
sudo apt install oracle-java9-installer oracle-java9-set-default
```
**References:**
- [Stack Overflow - Installing Oracle JDK](https://stackoverflow.com/a/29106006/6146369)
- [No support for JDK9 in audivers](https://github.com/Audiveris/audiveris/issues/51)

Install gradle
---------------------------------------
```
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install gradle 4.6
```
**References:**
- https://gradle.org/install/
- [Step-by-step install gradle on ubuntu
     ](https://howtoprogram.xyz/2016/09/06/install-gradle-ubuntu-16-04/)


Install Tesseract for OCR
---------------------------------------
```
sudo apt install tesseract-ocr
```
**References:**
- https://github.com/tesseract-ocr/tesseract

Clone and build audivers
---------------------------------------
```
cd ~/git/
git clone https://github.com/Audiveris/audiveris.git
gradle clean build
```

**References:**
- https://github.com/Audiveris/audiveris/wiki/Installation
