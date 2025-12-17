

def print_cards(cardsJson):
    for i, card in enumerate(cardsJson):
        print(f"{i:<3}: {card['card']}")