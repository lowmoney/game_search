import requests
from bs4 import BeautifulSoup


SEARCH_URL = 'https://gg.deals/games/?title='
GAME_URL = 'https://gg.deals'

class Game():
    '''
    A class to that represents scrapped data for a searched game

    Attributes
    -----------
    name : str
        the name of the game after a search has completed
    shop : str
        the shop: steam, epic game store, etc. that sells the game for the cheapest price after a search has completed
    shops : [str]
        the shops: steam, epic game store, etc. that sells the game after a search has completed
    price : str
        the price of the game from the shop with the lowest price after a search has completed
    prices : [str]
        the prices that all the shops that sell the game have after a search has completed
    link : str
        the TinyUrl link to the shop that has the game for the lowest price after a search has completed
    links : [str]
        the TinyUrl links to the shops that have the game for the lowest price after a search has completed
    found : bool
        if the game was found then True, if not found or Error then False
    keyshops_shops : [str]
        the key shops: G2A, CDKeys, etc. that sells the game after a search has completed
    keyshops_prices : [str]
        the prices of the game in the key shops
    keyshops_links : [str]
        the links of the game in the key shops
    keyshops_found : bool
        if keyshops sell the game then True, if not found or Error then False

    Methods
    -------
    search(game_name:str) -> tuple
        returns (True, Game) if search was successful, otherwise returns (False, Game)

    list_shops -> [dict]
        returns an array of dict objects of the shop, price, and link to the shop where the game is sold

    link_to_lowest_price -> str
        returns the link of the game with the lowest price

    store(store:str) -> dict
        returns a dict of the shop, price, and link if the store sells the game or None if the shop does not sell the game

    less_than_price(price:int) - > [dict]
        returns a list of dict objects where price is >= price, empty list if none found
    '''
    def __init__(self):
        '''
        creates a new Game object

        Parameters
        ----------
        takes no parameters
        '''
        self.name:str = None
        self.shop:str = None
        self.shops:[str] = None
        self.price:str = None
        self.prices:[str] = None
        self.link:str = None
        self.links:[str] = None
        self.found:bool = False

        self.keyshops_shops:[str] = []
        self.keyshops_prices:[str] = []
        self.keyshops_links:[str] = []
        self.keyshop_found:bool = False
    
    def search(self, game_name:str) -> tuple:
        '''
        Given the game name, returns a tuple of (True, Game) if search was succesful
        returns (False, Game) if search was not succesful
        
        Parameters
        ----------
        game_name : str
            the name of the game to search
        '''

        # get the search page
        page = requests.get(SEARCH_URL+str(game_name))
        link_to_game:str = None

        if page.status_code == 200:
            page = page.text

            # try block that starts the scrapping
            try:
                soup = BeautifulSoup(page,'html.parser')

                # name of the game we found form the store, and the link to the game
                self.name = ((soup.find('div','details')).find('a','ellipsis title').text.strip())
                
                link_to_game = soup.find('a','game-link')['href']

                official_shop = requests.get(GAME_URL + link_to_game ).text
                soup = BeautifulSoup(official_shop,'html.parser')

                # some complicated list comprehensions to get all the shops,
                # prices, and links for the game
                shops = soup.find_all('a','shop-link')
                self.shops = [shop.img['alt'] for shop in shops]

                prices = soup.find_all('div','game-deals-item')
                self.prices = [price.find('span','game-price-current').text.strip().replace('~','').replace('$','').split('\n')[0] for price in prices]

                links = soup.find_all('a','full-link')
                self.links = [requests.get('http://tinyurl.com/api-create.php?url='+str('https://gg.deals'+ link['href'])).text for link in links]

                # if we were able to find all the data, make found = True
                self.found = True

            except Exception as e:
                # some error occured, could be that the page has changed some info
                # so the parser could not find the data
                print(f'when trying to find info on the game for official shops, an error occured\n{e}\n')
                return (False, self)

            try:
                # after getting the intial page, scrape the game page itself
                page = requests.get(GAME_URL + link_to_game ).text
                soup = BeautifulSoup(page,'html.parser')

                self.shop = soup.find('a','shop-link').img['alt']
                self.price = soup.find('span','game-price-current').text.strip().replace('~','').replace('$','').split('\n')[0]
                self.link = requests.get('http://tinyurl.com/api-create.php?url='+str('https://gg.deals'+ soup.find('a','full-link')['href'])).text
                self.found = True

                return (True, self)

            except Exception as e:
                print(f'when trying to scrape for the quick link for the game, an error occured\n{e}\n')
                return (False, None)

        else:
            # the server denied our request, raise warning
            raise Warning('the server denied our request to search on official shops')
            pass

        key_shops = requests.get(GAME_URL + (link_to_game+'?tab=keyshops'))
        if key_shops.status_code == 200:
            try:
                key_shops = key_shops.text
                soup = BeautifulSoup(key_shops,'html.parser')

                # some complicated list comprehensions to get all the shops,
                # prices, and links for the game
                shops = soup.find_all('a','shop-link')
                self.keyshops_shops = [shop.img['alt'] for shop in shops]

                prices = soup.find_all('div','game-deals-item')
                self.keyshops_prices = [price.find('span','game-price-current').text.strip().replace('~','').replace('$','').split('\n')[0] for price in prices]
                
                links = soup.find_all('a','game-hoverable full-link')
                self.keyshops_links = [requests.get('http://tinyurl.com/api-create.php?url='+str('https://gg.deals'+ link['href'])).text for link in links]

                self.keyshop_found = True


            except Exception as e:
                # some error occured, could be that the page has changed some info
                # so the parser could not find the data
                print(f'when trying to find info on the game for key shops, an error occured\n{e}\n this error has been passed')
                pass
        else:
            print('the server denied our request to search on keyshops')
            return(False, None)

        
        return(self.found, self)

    
    # left over function that may not be needed
    # def search(self, game_name:str) -> tuple:
    #     '''
    #     Given the game_name:str, adds a Tiny link to go to the game page. 
    #     Also, returns a tuple of True if the search was succesful, False if not successful.
    #     The Game object is always returned with information if search was successful
    #     '''
    #     page = requests.get(SEARCH_URL+str(game_name))

    #     if page.status_code == 200:
    #         try:
    #             # get the inital page for the game
    #             page = page.text

    #             soup = BeautifulSoup(page,'html.parser')
    #             self.name = ((soup.find('div','details')).find('a','ellipsis title').text.strip())
                
    #             link_to_game = soup.find('a','game-link')['href']

    #             try:
    #                 # after getting the intial page, scrape the game page itself
    #                 page = requests.get(GAME_URL + link_to_game ).text
    #                 soup = BeautifulSoup(page,'html.parser')

    #                 self.shop = soup.find('a','shop-link').img['alt']
    #                 self.price = soup.find('span','game-price-current').text.strip().replace('~','').replace('$','').split('\n')[0]
    #                 self.link = requests.get('http://tinyurl.com/api-create.php?url='+str('https://gg.deals'+ soup.find('a','full-link')['href'])).text
    #                 self.found = True

    #                 return (True, self)

    #             except Exception as e:
    #                 print(f'when trying to scrape for the quick link for the game, an error occured\n{e}\n')
    #                 return (False, None)
    #         except Exception as e:
    #             print(f'when trying to scrape for the game, an error occured\n{e}\n')
    #             return (False, None)
    
    @property
    def list_shops(self) -> [dict]:
        '''
        returns an array of dict objects of the shop, price, and link to the shop where the game is sold
        '''
        if self.found:
            shops = []

            for i in range(len(self.shops)-1):
                shops.append({'shop':self.shops[i], 'price':self.prices[i], 'link':self.links[i]})
            
            return shops

    @property
    def link_to_lowest_price(self) -> str:
        '''
        returns the link of the game with the lowest price
        '''
        if self.found:
            return self.link
        else:
            raise Warning('You have yet to search for a game')
            pass

    def store(self, store:str) -> dict:
        '''
        returns a dict of the shop, price, and link if the store sells the game or None if the shop does not sell the game

        Parameters
        ----------
        store : str
            the store name to search for
        
        Raises
        ------
        Warning
            if no game has been searched for, a warning is raised
        '''

        if self.found:
            shops = self.list_shops

            for shop in shops:
                if shop['shop'].lower() == store.lower():
                    return {'shop':shop['shop'], 'price':shop['price'], 'link':shop['link']}

            return None
        else:
            raise Warning('You have yet to search for a game')

    def less_than_price(self, price:int) -> [dict]:
        '''
        returns a list of dict objects where price is >= price, empty list if none found

        Parameters
        ----------
        pirce : int
            the price to compare

        Raises
        ------
        Warning
            if no game has been searched for, a warning is raised
        '''

        if self.found:
            shops = self.list_shops

            shops_less_than_or_equal_to_price = []

            for shop in shops:
                if float(shop['price']) <= price:
                    shops_less_than_or_equal_to_price.append({ 'shop':shop['shop'], 'price':shop['price'], 'link':shop['link'] })
            
            return shops_less_than_or_equal_to_price
        else:
            raise Warning('You have yet to search for a game')


    def __str__(self):
        if self.found:
            shops = self.list_shops

            games = '{}\n----------\n'.format(self.name)

            for shop in shops:
                games += 'shop: {} for {} -> {}\n'.format(shop['shop'], shop['price'], shop['link'])
            
            return games
        else:
            raise Warning('You have yet to search for a game')
            pass