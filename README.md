# Personal TV Guide
This is some simple Python code to scrape my watchlist data from JustWatch and turn it into HTML to serve as my own TV Guide.

![screenshot](https://raw.githubusercontent.com/skadogg/personal-tv-guide/main/images/screenshot%202023-12-24.png)

  
- [Background](#background)
- [The code](#the-code)
  - [Scraping](#scraping)
  - [How to run it](#how-to-run-it)
    - [Start by scraping the data](#start-by-scraping-the-data)
    - [Build the HTML output](#build-the-html-output)
- [Acknowledgements](#acknowledgements)
  - [Theme](#theme)
  - [Badges](#badges)


## Background
Remember the weekly TV guide that came with the newspaper? It was the only useful thing in there - aside from the comic section.

(I really need to figure out where to watch some *Kate & Allie* - great show!)

![1987](https://raw.githubusercontent.com/skadogg/personal-tv-guide/main/images/1987-TV-Featured1.jpg)


## The code

### Scraping
The code does not currently have anything to [automate authentication](https://github.com/skadogg/personal-tv-guide/issues/2), so it just pauses to allow you to type in your credentials. After that, things go pretty smoothly.

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
>>> python scrape_movies.py
```


## Acknowledgements

### Theme
The stylesheet is using the [Nord theme](https://www.nordtheme.com/).

### Badges
All badges are from [Shields.io](https://shields.io/), which I probably saw originally on [awesome-badges](https://github.com/badges/awesome-badges).

