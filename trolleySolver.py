import json
import random
import copy
from util import print_cards

# Load JSON files
with open("innocent.json", "r") as f:
    innocent_cards = json.load(f)

with open("guilty.json", "r") as f:
    guilty_cards = json.load(f)

with open("modifier.json", "r") as f:
    modifiers = json.load(f)

# Helper function to select cards
def select_cards():
    innocents = random.sample(innocent_cards, 2)
    guilty = random.choice(guilty_cards)
    return innocents, guilty

# Apply one random modifier to one random card on the track
def apply_modifier(innocents, guilty):
    modifier = random.choice(modifiers)

    # Combine all cards on the track
    all_cards = innocents + [guilty]
    target_card = random.choice(all_cards)

    # Apply modifier
    target_card["modifier"] = modifier
    target_card["modified_weight"] = target_card["weight"] * modifier["modifier"]

    return modifier, target_card

# Calculate total weights (respect modifiers)
def track_weight(innocents, guilty):
    total = 0.0
    for card in innocents + [guilty]:
        total += card.get("modified_weight", card["weight"])
    return total

def random_tracks():
    # Select cards (deepcopy to avoid cross-track mutation)
    track1_innocent, track1_guilty = copy.deepcopy(select_cards())
    track2_innocent, track2_guilty = copy.deepcopy(select_cards())

    # Apply modifiers
    track1_modifier, track1_modified_card = apply_modifier(track1_innocent, track1_guilty)
    track2_modifier, track2_modified_card = apply_modifier(track2_innocent, track2_guilty)

    # Calculate weights
    track1_weight = track_weight(track1_innocent, track1_guilty)
    track2_weight = track_weight(track2_innocent, track2_guilty)

    # Determine outcome
    if track1_weight >= track2_weight:
        winner = "Track 1"
        loser = "Track 2"
    else:
        winner = "Track 2"
        loser = "Track 1"

    print_track("Track 1", track1_innocent, track1_guilty, track1_weight)
    print_track("Track 2", track2_innocent, track2_guilty, track2_weight)

    print("\nRESULT")
    print("------")
    print(f"{winner} LIVES")
    print(f"{loser} DIES")

def print_track(track_name, innocents, guilty, total_weight):
    print(f"\n{track_name}")
    print("-" * len(track_name))

    for card in innocents:
        weight = card.get("modified_weight", card["weight"])
        modifier = card.get("modifier")
        if modifier:
            print(
                f"Innocent: {card['card']} "
                f"(base {card['weight']:.2f} × {modifier['modifier']:.2f} "
                f"[{modifier['card']}] = {weight:.2f})"
            )
        else:
            print(f"Innocent: {card['card']} (weight {weight:.2f})")

    card = guilty
    weight = card.get("modified_weight", card["weight"])
    modifier = card.get("modifier")
    if modifier:
        print(
            f"Guilty:   {card['card']} "
            f"(base {card['weight']:.2f} × {modifier['modifier']:.2f} "
            f"[{modifier['card']}] = {weight:.2f})"
        )
    else:
        print(f"Guilty:   {card['card']} (weight {weight:.2f})")

    print(f"TOTAL WEIGHT: {total_weight:.2f}")

def custom_game():
    #track 1
    print("You will need to select 2 innocent cards and 1 guilty card for each track")
    print("You may then add at most one modifier to each card")
    print("To see the list of possible cards, at any point type:")
    print("  'i' for innocent")
    print("  'g' for guilty")
    print("  'm' for modifier")
    print("To select a card, simply input the number associated with that card")
    print("To end modifier selection, type 'stop'")

    in11 = None
    in12 = None
    g1 = None
    in21 = None
    in22 = None
    g2 = None

    while True:
        if in11 is None:
            inp = input("innocent--")
        elif in12 is None:
            inp = input("innocent--")
        elif g1 is None:
            inp = input("guilty--")
        elif in21 is None:
            inp = input("innocent--")
        elif in22 is None:
            inp = input("innocent--")
        elif g2 is None:
            inp = input("guilty--")
        else:
            print("To end modifier selection, type 'stop'")
            inp = input("modifier--")

        if inp == 'i':
            print("="*50)
            print("Innocent cards:")
            print_cards(innocent_cards)
            print("="*50)
            continue
        if inp == 'g':
            print("="*50)
            print("Guilty cards:")
            print_cards(guilty_cards)
            print("="*50)
            continue
        if inp == 'm':
            print("="*50)
            print("Modifier cards:")
            print_cards(modifiers)
            print("="*50)
            continue
        if inp == "stop":
            break

        try:
            inp = int(inp)
        except ValueError:
            print(f"{inp} is not a valid number")
            continue

        if inp < 0:
            print(f"{inp} is negative, input is expected to be positive")
            continue

        if in11 is None:
            if inp >= len(innocent_cards):
                print(f"{inp} is not a valid card number")
                continue
            in11 = innocent_cards[inp]
        elif in12 is None:
            if inp >= len(innocent_cards):
                print(f"{inp} is not a valid card number")
                continue
            in12 = innocent_cards[inp]
        elif g1 is None:
            if inp >= len(guilty_cards):
                print(f"{inp} is not a valid card number")
                continue
            g1 = guilty_cards[inp]
        elif in21 is None:
            if inp >= len(innocent_cards):
                print(f"{inp} is not a valid card number")
                continue
            in21 = innocent_cards[inp]
        elif in22 is None:
            if inp >= len(innocent_cards):
                print(f"{inp} is not a valid card number")
                continue
            in22 = innocent_cards[inp]
        elif g2 is None:
            if inp >= len(guilty_cards):
                print(f"{inp} is not a valid card number")
                continue
            g2 = guilty_cards[inp]
        else:
            if inp >= len(modifiers):
                print(f"{inp} is not a valid card number")
                continue
            print("type the track number followed by the card number of the card you would like to modify")
            print("  ex. '12' would be the second innocent card in track 1")
            num = input("--")
            try:
                num = int(num)
            except ValueError:
                print(f"{num} is not a valid number")
                continue
            match num:
                case 11:
                    in11["modifier"] = modifiers[inp]
                    in11["modified_weight"] = in11["weight"] * modifiers[inp]["modifier"]
                case 12:
                    in12["modifier"] = modifiers[inp]
                    in12["modified_weight"] = in12["weight"] * modifiers[inp]["modifier"]
                case 13:
                    g1["modifier"] = modifiers[inp]
                    g1["modified_weight"] = g1["weight"] * modifiers[inp]["modifier"]
                case 21:
                    in21["modifier"] = modifiers[inp]
                    in21["modified_weight"] = in21["weight"] * modifiers[inp]["modifier"]
                case 22:
                    in22["modifier"] = modifiers[inp]
                    in22["modified_weight"] = in22["weight"] * modifiers[inp]["modifier"]
                case 23:
                    g2["modifier"] = modifiers[inp]
                    g2["modified_weight"] = g2["weight"] * modifiers[inp]["modifier"]
                case _:
                    print("invalid number. expected \{11, 12, 13, 21, 22, 23\}")
                    continue
    
    if (    (in11 is None)
        or  (in12 is None)
        or  (g1 is None)
        or  (in21 is None)
        or  (in22 is None)
        or  (g2 is None)
        ):
        print("unfinished track(s) please stop only after all cards have been chosen.")
        return

    #calculate
    track1_weight = track_weight([in11, in12], g1)
    track2_weight = track_weight([in21, in22], g2)

    #printing
    if track1_weight >= track2_weight:
        winner = "Track 1"
        loser = "Track 2"
    else:
        winner = "Track 2"
        loser = "Track 1"

    print_track("Track 1", [in11, in12], g1, track1_weight)
    print_track("Track 2", [in21, in22], g2, track2_weight)

    print("\nRESULT")
    print("------")
    print(f"{winner} LIVES")
    print(f"{loser} DIES")
        

if __name__ == '__main__':
    print("="*30)
    print("Welcome to TRIAL BY TROLLY")
    print("="*30)

    while True:
        print("  to start a random game, enter 'r'")
        print("  to input a custom game, enter 'c'")

        inp = input("--")

        if inp == 'r':
            random_tracks()
            break
        if inp == 'c':
            #custom user input time
            custom_game()
            break
        print(f"invalid input: {inp}")

    
