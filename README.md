# Personal TV Guide
![Personal TV Guide logo](./images/logo_text.png)

Scrape your JustWatch watchlist data and turn it into HTML to serve as your own **Personal TV Guide**! 

# Introduction
Remember the weekly [TV guide](./images/1987-TV-Featured1.jpg) that came with the newspaper? It was the only useful thing in there - aside from the [comic section](./images/tv1.jpg). **Personal TV Guide** creates a custom TV guide using the shows and movies from your watchlist. It also provides an easy way to see how much time you have left in a show.

# Installation

To install **Personal TV Guide**, follow these steps:

1. Clone the repository: `git clone https://github.com/skadogg/personal-tv-guide.git`
2. Navigate to the project directory: `cd personal-tv-guide`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a *my_data* folder for your private data: `mkdir my_data`
5. Copy the sample .env file to your main folder: `cp ./sample_files/.env-sample ./.env`
6. Start the project: `python run.py`

# Usage

To use **Personal TV Guide**, follow these steps:

1. Open the project in your favorite code editor.
2. Modify the .env file to fit your needs.
3. Start the project: `python run.py`.
5. Use the project as desired.
6. Open `./my_data/out.html` to view your **Personal TV Guide**.

![screenshot](images/screenshot2024-01-29.png)

# Contributing

If you'd like to contribute to **Personal TV Guide**, here are some guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes.
4. Write tests to cover your changes.
5. Run the tests to ensure they pass.
6. Commit your changes.
7. Push your changes to your forked repository.
8. Submit a pull request.

# License

**Personal TV Guide** is released under the GPL-3.0 license. See the [LICENSE](./LICENSE) file for details.

# Authors and Acknowledgment

**Personal TV Guide** was created by [Wes Anderson](https://github.com/skadogg).

Additional contributors include:

- [Ajay Jain](https://github.com/code-master-ajay)
- [Abhay](https://github.com/perriDplatypus)
- [Khalil Habib Shariff](https://github.com/Khaleelhabeeb)
- [Vivek Panchal](https://github.com/TechWithVP)
- [Rudransh Bhardwaj](https://github.com/rudransh61)
- [Leonardo Bringel](https://github.com/LeonardoBringel)

Thank you to all the contributors for their hard work and dedication to the project!

<!-- # Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project, you agree to abide by its terms. See the **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** file for more information. -->

# FAQ

Q: What is **Personal TV Guide**?

A: **Personal TV Guide** creates a custom TV guide using the shows and movies from your JustWatch watchlist. It also provides an easy way to see how much time you have left in a show.

Q: How do I install Project Title?

A: Follow the installation steps in the README file.

Q: How does **Personal TV Guide** read my JustWatch watchlists?

A: The first time you run the program, you will be prompted to enter your JustWatch credentials. These get stored in a local file in your private *my_data* folder.

Q: How do I customize my **Personal TV Guide**?

A: Update the .env file you created in Step #5 during Installation. Here's what each value does:

| Variable | Required? | Description |
| --- | :---: | --- |
| WHEN_TO_START | Y | The first hour in your guide's timeline |
| HOURS_TO_PRINT | Y | How many hours worth of data to include in timeline |
| STYLESHEET_PATH | Y | Where to find the CSS stylesheet |
| OUTFILE | Y | The name of the HTML file you want to generate |
| USE_KEYWORD_LIST | N | set to True to enable keyword lists. |
| *genre*_KEYWORDS | N | If creating custom rows in the table, enter a comma-separated list of strings to match. This is currently case-sensitive. |
| DEV_MODE | N | Set to False for normal use. When developing and testing, set to True to limit the number of titles read from the source. |

Q: How do I use Project Title?

A: Follow the usage steps in the README file.

Q: How do I contribute to Project Title?

A: Follow the contributing guidelines in the README file.

Q: What license is Project Title released under?

A: **Personal TV Guide** is released under the GPL-3.0 license. See the [LICENSE](./LICENSE) file for details.
