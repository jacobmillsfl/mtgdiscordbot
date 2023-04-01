import requests
import json
from .emojis import Emojis

class CardSdk:
    API_QUERY_URL = "https://api.scryfall.com/cards/search"

    @staticmethod
    def parse_search_terms(query: str):
        card_name = query
        set = ""
        if "|" in query:
            parts = query.split("|")
            card_name = parts[0].strip()
            set = parts[1].strip()
        return card_name, set

    @staticmethod
    def search(search_terms: str) -> str:
        result = ""

        card_name, set = CardSdk.parse_search_terms(search_terms)
        search_query = f"?q={card_name}"
        if set:
            search_query += f"|{set}"

        print(f"{CardSdk.API_QUERY_URL}?q={card_name}")
        response = requests.get(f"{CardSdk.API_QUERY_URL}?q={card_name}")
        if response.ok:
            response_json = json.loads(response.text)
            data = response_json["data"]
            matched_card = None
            for potential_card in data:
                card = Card(potential_card)
                if card.name_matches(card_name):
                    matched_card = card
                    break
            if not matched_card:
                # Use the first match if we didn't find something precisely
                matched_card = Card(data[0])

            # Name/s
            for name in matched_card.names:
                result += f"**{name}**\n"

            # Images
            for image in matched_card.images:
                result += image + "\n"
            
            # Flavor
            if matched_card.flavor_text:
                result += "\n_" + matched_card.flavor_text + "_\n\n"
            
            # Legalities
            legalities = matched_card.legalities
            for format in legalities.keys():
                if format in ['commander', 'modern', 'standard','explorer','brawl']:
                    icon = Emojis.red_x.value
                    if matched_card.legalities[format] == 'legal':
                        icon = Emojis.check_mark.value
                    result += f"{icon}:\t{format.capitalize()}\n"
        else:
            return f"Error: Unable to find '{search_terms}'"
        return result

class Card:
    @staticmethod
    def parse(property : str, object : dict):
        result = ""
        if property in object:
            result= object[property]
        return result

    def name_matches(self, target_name : str) -> bool:
        found = False
        for name in self.names:
            if name.lower() == target_name.lower():
                found = True
                break
        return found

    def __init__(self, card_object : dict):
        self.names = []
        self.images = []

        name = Card.parse("name", card_object)
        self.names.append(name)
        self.color_identity = Card.parse("color_identity", card_object)
        self.keywords = Card.parse("keywords", card_object)
        self.legalities = Card.parse("legalities", card_object)
        self.set = Card.parse("set", card_object)
        self.set_name = Card.parse("set_name", card_object)
        self.prices = Card.parse("prices", card_object)
        self.flavor_text = Card.parse("flavor_text", card_object)

        image_uris = Card.parse("image_uris", card_object)
        if image_uris:
            self.images.append(image_uris["normal"])

        if "card_faces" in card_object:
            front = card_object["card_faces"][0]
            front_name = Card.parse("prices", front)
            if front_name:
                self.names.append(front_name)
            self.mana_cost = Card.parse("mana_cost", front)
            self.oracle_text = Card.parse("oracle_text", front)
            self.colors = Card.parse("colors", front)
            self.power = Card.parse("power", front)
            self.toughness = Card.parse("toughness", front)
            self.colors = Card.parse("colors", front)

            front_image_uris = Card.parse("image_uris", front)
            if front_image_uris:
                self.images.append(front_image_uris["normal"])

            back = card_object["card_faces"][1]
            back_name = back["name"]
            self.names.append(back_name)

            back_image_uris = Card.parse("image_uris", back)
            if back_image_uris:
                self.images.append(back_image_uris["normal"])
        else:
            self.mana_cost = Card.parse("mana_cost", card_object)
            self.oracle_text = Card.parse("oracle_text", card_object)
            self.colors = Card.parse("colors", card_object)
            self.power = Card.parse("power", card_object)
            self.toughness = Card.parse("toughness", card_object)
            self.colors = Card.parse("colors", card_object)

