egielda
=======

e-Giełda is a project that aims to create easy and convenient way to trade books between students. e-Giełda is a webapp that has a purpose to provide user-friendly interface for various actions like actual buying, generating reports and summaries, etc.

The app is written in Python using Django. It makes use of HTML5 and CSS3 by using Bootstrap v3 as a framework for the whole user interface.

## Features
* Selling, buying books
* Categories of books
* Filling the informations about the book automatically after typing the ISBN number (thanks to the Google Books API)
* Statistics:
  * Charts (visualising informations about the amount of books sold, income, etc.)
  * Raw data about books sold in each day
  * Generating reports for each user about sold and unsold books
* Permissions support, built-in groups (administrator, moderator that can accept books from users and sell them)
* Database setttings: buying/selling time interval, order validity time, static information on homepage, profit per book for organisators
* i18n support (Polish translation built-in)
* More...

## How it works, by and large
First of all, a user goes to Sell page and choose the books they want to sell. Then, they come with these books to the administrator/moderator, who "accepts" them - i.e. marks them as available for buying. Then, when it comes to Purchasing, this is quite similar: the user goes to Purchase page, choose the books they want to buy and goes to the moderator who executes their order. What's important there is that the order has a validity time and books that are reserved in particular order are unavailable to others for buying until the order times out.

In e-Giełda, there are two models with "Book" in name: BookType and Book. The difference between them is that BookType contains only a common data about the book (title, publisher, etc.), while Book is a "physical" book with an owner, sold/unsold state, etc.

## Dependencies
* Python 3.2 or newer (may also work with 3.0, though it wasn't tested)
* Django 1.7 or newer
* Django Widget Tweaks

For running tests:
* Selenium

## Third-party components
e-Giełda uses a few third-party components contained in vendor/ directory. It includes:
* [Bootstrap Datepicker](http://www.eyecon.ro/bootstrap-datepicker/) by Stefan Petre licensed under Apache License 2.0
* [NVD3.js](http://nvd3.org/) by [Novus Partners](https://www.novus.com/) licensed under Apache License 2.0
* Slightly modified version of [jQuery Tablesorter](http://tablesorter.com/docs/) by [Christian Bach](https://twitter.com/lovepeacenukes) dual licensed under MIT License or GNU GPL v2/v3
* Slightly modified (removed all languages but Polish and English) [Moment.js](http://momentjs.com/) by Tim Wood and Iskren Chernev licensed under MIT License. *Please note that this is version 2.6.0 since newer versions do not work with Bootstrap Datepicker.*

Also, it uses following components that are loaded from CDN:
* [Bootstrap](http://getbootstrap.com/) by [@mdo](http://twitter.com/mdo) and [@fat](http://twitter.com/fat) licensed under MIT License
* [Bootstrap Select](http://silviomoreto.github.io/bootstrap-select/3/) by [@caseyjhol](https://github.com/caseyjhol) licensed under MIT License
* [D3.js](http://d3js.org/) by [Mike Bostock](http://bost.ocks.org/mike/) licensed under BSD License
* [HTML5 Shiv](https://github.com/aFarkas/html5shiv) by [Alexander Farkas](https://github.com/aFarkas/), [Jonathan Neal](https://twitter.com/jon_neal), [Paul Irish](https://twitter.com/paul_irish), and [John-David Dalton](https://twitter.com/jdalton) dual licensed under MIT License or GNU GPL v2
* [jQuery](http://jquery.com/) by jQuery Foundation, Inc. licensed under MIT License
* [Respond.js](https://github.com/scottjehl/Respond) by [Scott Jehl](scottjehl.com) licensed under MIT License

## Installation
These are commands used to properly install development version of e-Giełda:

```bash
# We recommend creating a virtualenv first
virtualenv -p python3 egielda
cd egielda
source bin/activate
# Actual installing
git clone https://github.com/m4tx/egielda.git
cd egielda
pip install -r requirements.txt
python manage.py migrate
# In order to make translations working
python manage.py compilemessages
# Superuser may be useful
python manage.py createsuperuser
```
It uses SQLite database by default.

Please note that our migration script automatically creates three groups (moderator, admin, sysadmin) and gives them some permissions. If you change anything and want to restore default permissions for these groups, you have to remove **all** permissions from at least one group, then run `migrate`.

## License
Copyright (C) 2014 [Mateusz Maćkowski](http://m4tx.pl) and Tomasz Zieliński 

e-Giełda is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

e-Giełda is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
