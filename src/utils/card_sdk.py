import requests
import json
from .emojis import Emojis

class CardSdk:
    API_QUERY_URL = "https://api.scryfall.com/cards/search"

    @staticmethod
    def search(cardname: str) -> str:
        result = ""
        response = requests.get(f"{CardSdk.API_QUERY_URL}?q={cardname}")
        if response.ok:
            response_json = json.loads(response.text)
            data = response_json["data"]
            card = data[0]
            for potential_card in data:
                if potential_card["name"].lower() == cardname.lower():
                    card = potential_card
                    break

            result += card["image_uris"]["normal"] + "\n"
            if "flavor_text" in card:
                result += "\n_" + card["flavor_text"] + "_\n\n"
            legalities = card["legalities"]
            for format in legalities:
                if format in ['commander', 'modern', 'standard']:
                    icon = Emojis.red_x.value
                    if legalities[format] == 'legal':
                        icon = Emojis.check_mark.value
                    result += f"{icon}:\t{format.capitalize()}\n"
        else:
            return f"API Error {response.status_code}"
        return result
