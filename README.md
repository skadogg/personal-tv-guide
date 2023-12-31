# Personal TV Guide
![Created by Pedrovisc from Noun Project](images/Tv-Guide-Created-by-Pedrovisc-from-Noun-Project-cropped-200px.png)


## About
Scrape your watchlist data from JustWatch and turn it into HTML to serve as your own TV Guide!

![screenshot](https://raw.githubusercontent.com/skadogg/personal-tv-guide/main/images/screenshot%202023-12-24.png)


- [About](#about)
- [Background](#background)
- [The code](#the-code)
  - [Credentials](#credentials)
  - [How to run it](#how-to-run-it)
    - [Start by scraping the data](#start-by-scraping-the-data)
    - [Build the HTML output](#build-the-html-output)
- [Acknowledgements](#acknowledgements)
  - [Icon](#icon)
  - [Theme](#theme)
  - [Badges](#badges)
  - [gitmoji](#gitmoji)


## Background
Remember the weekly TV guide that came with the newspaper? It was the only useful thing in there - aside from the comic section.

(I really need to figure out where to watch some *Kate & Allie* - great show!)

![1987](https://raw.githubusercontent.com/skadogg/personal-tv-guide/main/images/1987-TV-Featured1.jpg)


## The code

### Credentials
The first time you run it, you will be prompted to enter your JustWatch credentials. These get stored in a local file that will be ignored in any new commits you might make to the repository.

### How to run it

#### Start by scraping the data
Each of these will pause and wait for you to sign in, as mentioned above. Once they finish, they will write the data to .bin files. These will be used in the next step.

```
>>> python scrape_tv.py
>>> python scrape_movies.py
```

#### Build the HTML output
With the data scraped, we can generate an HTML file.

```
>>> python build_html.py
```


## Acknowledgements

### Icon
The *Tv Guide* icon was created by Pedrovisc from the [Noun Project](https://thenounproject.com/icon/tv-guide-193845/).

### Theme
The stylesheet is using the [Nord theme](https://www.nordtheme.com/).

### Badges
All badges are from [Shields.io](https://shields.io/), which I probably saw originally on [awesome-badges](https://github.com/badges/awesome-badges).

### gitmoji
💡 We try to use gitmoji to enhance our commit statements.

[![gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square)](https://gitmoji.dev/)