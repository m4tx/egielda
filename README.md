egielda [![Build Status](https://travis-ci.org/m4tx/egielda.svg?branch=master)](https://travis-ci.org/m4tx/egielda)
=======

e-Giełda is a project that aims to create easy and convenient way to trade books between students, both user-friendly and featureful.

The app is written in Python using Django. It makes use of HTML5 and CSS3 by using Semantic UI as a framework for user interface.

## Features
* Selling, buying books
* Categories of books
* Filling the information about the book automatically after typing the ISBN number (thanks to the Google Books API)
* Statistics:
  * Charts (visualising information about the amount of books sold, income, etc.)
  * Raw data about books sold in each day
  * Generating reports for each user about sold and unsold books
* Permissions support, built-in groups (administrator, moderator that can accept books from users and sell them)
* User verification support along with auto-verification via LDAP
* Settings stored in the database: buying/selling time interval, order validity time, static information on homepage, profit per book for organizers
* i18n support (Polish translation built-in)
* More...

## How it works, by and large
First of all, a user goes to Sell page and choose the books they want to sell. Then, they come with these books to the administrator/moderator, who "accepts" them - i.e. marks them as available for buying. Then, when it comes to Purchasing, this is quite similar: the user goes to Purchase page, choose the books they want to buy and goes to the moderator who executes their order. What's important there is that the order has a validity time and books that are reserved in particular order are unavailable to others for buying until the order times out.

In e-Giełda, there are two models with "Book" in name: BookType and Book. The difference between them is that BookType contains only a common data about the book (title, publisher, etc.), while Book is a "physical" book with an owner, sold/unsold state, etc.

## Dependencies
* Python 3.2
* Django 1.8
* ldap3 (though LDAP support is not enabled by default)
* Pillow

For building the assets:
* Node.js with gulp

For running tests:
* Selenium

## Third-party components
e-Giełda uses a few third-party components modified by us contained in `vendor/` directory. It includes:
* Patched version of [NVD3.js](http://nvd3.org/) by [Novus Partners](https://www.novus.com/) licensed under Apache License 2.0
* Slightly modified version of [jQuery Tablesorter](http://tablesorter.com/docs/) by [Christian Bach](https://twitter.com/lovepeacenukes) dual licensed under MIT License or GNU GPL v2/v3
* Slightly modified (removed all languages but Polish and English) [Moment.js](http://momentjs.com/) by Tim Wood and Iskren Chernev licensed under MIT License.

Descriptions of the modifications are provided in top file comments.

`vendor/` directory also contains two git submodules:
* Our [modified version](https://github.com/m4tx/egielda-Semantic-UI) of [Semantic UI](http://www.semantic-ui.com/) by [Jack Lukic](http://www.jacklukic.com) licensed under MIT License
* [semantic-tokenfield](https://github.com/m4tx/semantic-tokenfield), our version of [bootstrap-tokenfield](https://github.com/sliptree/bootstrap-tokenfield) by [Sliptree](https://sliptree.com/) licensed under MIT License

Also, it uses following components that are loaded from CDN or downloaded as Node.js modules:
* [D3.js](http://d3js.org/) by [Mike Bostock](http://bost.ocks.org/mike/) licensed under BSD License
* [jQuery](http://jquery.com/) and [jQuery UI](http://jquery.com/) by The jQuery Foundation, Inc., both licensed under MIT License
* [jQuery DateTimePicker plugin](http://xdsoft.net/jqplugins/datetimepicker/) by [Chupurnov Valeriy](https://github.com/xdan) licensed under MIT License

e-Giełda uses Google Books API ([Terms of Service](https://developers.google.com/books/terms)) as well.

## Installation
These are commands used to properly install development version of e-Giełda:

```bash
# We recommend creating a virtualenv first
virtualenv -p python3 egielda
cd egielda
source bin/activate
# Actual installing
git clone --recursive https://github.com/m4tx/egielda.git
cd egielda
pip install -r requirements.txt
python manage.py migrate
# Build the assets
npm install
# In order to make translations working
python manage.py compilemessages
# Superuser may be useful
python manage.py createsuperuser
```
Remember that you shouldn't use default `settings.py` on production. Also, bear in mind that SQLite is unsuitable for anything but e-Giełda development.

Please note that our migration script automatically creates three groups (moderator, admin, sysadmin) and gives them some permissions. If you change anything and want to restore default permissions for these groups, you have to remove **all** permissions from at least one group, then run `migrate`.

e-Giełda uses gulp tool to build CSS and JS files. `postinstall` script in npm calls `gulp build` automatically (actually, `npm run gulp build`, in case that gulp is not installed globally).

## LDAP Support
LDAP support can be enabled in `settings.py` file by setting `USE_LDAP_VERIFICATION` value to True and filling out the rest of `LDAP_*` settings below.

Enabling LDAP support changes user verification behavior. "School ID" field disappears from registration form, and when one clicks "Register", e-Giełda checks whether a user with provided personal data exists in LDAP. If so then the user is automatically verified, and otherwise the next form is shown, allowing them to verify their account "the normal way", i.e. by uploading a scan of their school ID.

## License
Copyright (C) 2014-2015 [Mateusz Maćkowski](http://m4tx.pl) and Tomasz Zieliński

e-Giełda is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

e-Giełda is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with e-Giełda.  If not, see http://www.gnu.org/licenses/.
