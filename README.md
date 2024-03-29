# PocketCalendarGenerator
Tool to create a Pocket Calendar (optimized for A6)

<p align="center">
<img src="https://user-images.githubusercontent.com/35701737/188839229-931ce0d4-9820-493c-ba5f-56797a858d4a.png" height="350" />
</p>

## Usage

**You need to have [Inkscape](https://inkscape.org/) installed.**

### Install python packages
`pip install -r requirements.txt`

### Modify lessons.txt
Format: 
```
Mo1
Mo2
Mo3
Mo4
Mo5
Mo6
Mo7

Di1
Di2
Di3
.
.
.

```
### Run script
`python3 main.py`  
<img src="https://user-images.githubusercontent.com/35701737/188840718-4254eda2-f166-4096-b298-1a45999261f4.png" height="135"/>

### Generating the title page
Open the file `TitlePage/titlepage.tex`.    
- Replace **Hausaufgabenheft** with your title
- Replace **Max Mustermann** with your name
- Replace `images/logo.png` with the path to your logo
- Replace `images/timetable.png` with the path to your timetable image
  
Now you can compile the file using your favourite LaTex Compiler. (e.g. texlive or miktex).
If you don't want to install any LaTex compiler on your system you should check out Overleaf.