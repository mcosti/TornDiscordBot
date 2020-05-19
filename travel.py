from datetime import datetime
import requests
import locale
from discord import Embed
import logging

logger = logging.getLogger()

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
doctorn_uri = "wss://api.doctorn.rocks/travel-hub/live"
url = "https://arsonwarehouse.com/api/v1/foreign-stock"

drugs = {
    196: 'Cannabis',
    197: 'Ecstasy',
    198: 'Ketamine',
    199: 'LSD',
    200: 'Opium',
    201: 'PCP',
    203: 'Shrooms',
    204: 'Speed',
    205: 'Vicodin',
    206: 'Xanax'
}

plushies = {
    384: 'Camel plushie',
    273: 'Chamois plushie',
    258: 'Jaguar plushie',
    281: 'Lion plushie',
    269: 'Monkey plushie',
    266: 'Nessie plushie',
    274: 'Panda plushie',
    268: 'Red fox plushie',
    618: 'Stingray plushie',
    261: 'Wolverine plushie'
}

flowers = {
    282: 'African violet',
    717: 'Banana orchid',
    271: 'Ceibo flower',
    277: 'Cherry blossom',
    263: 'Crocus',
    260: 'Dahlia',
    272: 'Edelweiss',
    267: 'Heather',
    264: 'Orchid',
    276: 'Peony',
    385: 'Tribulus Omanese'
}

class ItemTypes:
    DRUG = 'DRUG'
    FLOWER = 'FLOWER'
    PLUSHIE = 'PLUSHIE'

class Item:
    def __init__(self, item_id, country, price, stock, reported_at):
        self.item_id = item_id
        self.country = country
        self.price = price
        self.stock = stock
        self.reported_at = reported_at

    @property
    def type(self):
        if self.item_id in drugs.keys():
            return ItemTypes.DRUG
        
        if self.item_id in plushies.keys():
            return ItemTypes.PLUSHIE
        
        if self.item_id in flowers.keys():
            return ItemTypes.FLOWER

    @property
    def name(self):
        if self.type == ItemTypes.DRUG:
            return drugs[self.item_id]

        if self.type == ItemTypes.PLUSHIE:
            return plushies[self.item_id]

        if self.type == ItemTypes.FLOWER:
            return flowers[self.item_id]

        raise Exception("Item has no name", self.item_id)

    @property
    def key(self):
        return f"{self.item_id}_{self.country}"

    def __repr__(self):
        return f"<Item {self.key} - {self.name} - {self.stock}>"


items = {}


def get_embeds():
    global items
    new_items = {}
    embeds = {
        ItemTypes.DRUG: [],
        ItemTypes.PLUSHIE: [],
        ItemTypes.FLOWER: []
    }

    values = get_api_items()
    for value in values['items']:
        item = Item(**value)
        if item.type is not None:
            new_items[item.key] = item

    if not items:
        items = new_items
        logging.info("First run")
        return embeds

    for key, old_item in items.items():
        new_item = new_items[key]

        if old_item.stock == 0 and new_item.stock != 0:
            embeds[new_item.type].append(generate_embed(new_item))
            logging.info(f"{new_item.key} - {new_item.name} is again in stock")
    
    items = new_items
    return embeds



def generate_embed(item: Item):
    embed = Embed(title=f"{item.name} is again in stock")
    embed.set_thumbnail(url=f"https://www.torn.com/images/items/{item.item_id}/small.png")
    embed.add_field(name="Country", value=item.country, inline=False)
    embed.add_field(name="Stock", value=item.stock, inline=False)
    embed.add_field(name="Price", value=locale.currency(item.price, grouping=True), inline=False)
    embed.add_field(name="Reported at", value=item.reported_at, inline=False)
    embed.set_footer(text="Data source: https://arsonwarehouse.com/api/v1/foreign-stock")
    return embed

def get_api_items():
    resp = requests.get(url)
    return resp.json()


if __name__ == '__main__':
    get_embeds()
    print(get_embeds())
    # print(196 in drugs.keys())
