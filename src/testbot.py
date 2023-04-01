
from utils.misc import card_match
from utils.card_sdk import CardSdk

MENU = """
-------------------
| Enter a command |
-------------------
1) Match card from text
2) Lookup card
3) Exit

Command: """

def repl():
    while True:
        option = input(MENU)
        if option == "1":
            text = input("Enter text in the form of [[Cardname]]: ")
            matches = card_match(text)
            for match in matches:
                print(f"Matched: {match}")
        elif option == "2":
            text = input("Enter cards to lookup in the form of [[Cardname]]: ")
            matches = card_match(text)
            if len(matches) == 0:
                print("Invalid input syntax")
            else:
                for match in matches:
                    print(f"Searching for card {match}")
                    result = CardSdk.search(match)
                    print(result)
        elif option == "3":
            print("Goodbye")
            exit(0)
        else:
            print("Invalid command...")


def test_search():
    print(CardSdk.search("Graveyard Trespasser"))
    print(CardSdk.search("Shock"))
    print(CardSdk.search("Shock|m21"))
    print(CardSdk.search(" Shock | m21 "))
    print(CardSdk.search("Sol Ring"))
    print(CardSdk.search("Erayo, Soratami Ascendant"))
    print(CardSdk.search("Arlinn Kord"))
    print(CardSdk.search("asdfj hadskf haf kfe"))

if __name__ == "__main__":
    #repl()
    test_search()
