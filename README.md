# Pocket Calendar Generator

![image](https://github.com/user-attachments/assets/965c7066-05af-41e4-a703-c59450fcaae9)

## Installation

### Pocket Calendar

- Add Forte font (either to `~/.fonts`) or if using the Devcontainer into this directory
- Alternatively you could change the font under `variante2.tex`

```tex
\setmainfont{Forte} % SELECT FONT
```

### FetchLessonsFromGMOPortal

- Install geckodriver [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
  - Unzip the correct file
  - copy the `geckodriver` file into this directory

## Usage
- Replace `images/dummyImage.png` with your own image (e.g. your timetable)
  - (Optional, only works if your school is using the "schulportal") run `fetchLessonsFromGmoPortal.py`
- Replace `images/dummyLogo.png` with your own logo (e.g. your school logo)
- If needed adjust the paths in `titlepage.tex`
- Fill your informations/ customizations into `lessons.tex`
- Run
```bash
$ make
```
- Your pocket calendar is now located in the `output` folder
