# Game Searcher

Game Searcher allows you to search for any PC game so you can find out where to buy the game for the lowest price without searching a bunch of websites

## Requirements
Python 3.6+

Use the package manager [pip](https://pip.pypa.io/) to install [requests](https://docs.python-requests.org/en/master/), [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and optionally [Typer](https://typer.tiangolo.com/) if you wish to run the command line version.

```bash
pip3 install requests
pip3 beautifulsoup4
pi3 install typer # optional if you want to use with command line
```

## Usage

```python
from Game import Game

game = Game() # makes a new Game object
game.search(game_name: str) # returns a tuple (found: bool, game: Game)
game.less_than_price(price: int) # returns a list of dict objects where game price is <= price given
game.store(store: str) # returns a dict of the shop, price, and link if the store sells the game
```

If you wanted to use it via the terminal (make sure [Typer](https://typer.tiangolo.com/) is installed)
```bash
python3 search_game.py --help # shows options for the command
python3 search_game.py 'game_name' # returns all the shops, prices, and links for the game
python3 search_game.py 'game_name' --quick-link # returns TinyUrl link to the game with the lowest price
python3 search_game.py 'game_name' --price INTEGER # return the shops with the prices less than or equal the price specified
python3 search_game.py 'game_name' --store TEXT # returns if the store specified sells the game
pyhton3 search_game.py 'game_name' --hush # does not list all the shops, prices, and links for the game
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the terms of the MIT license.