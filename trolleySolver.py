import json
import random

# Load JSON files
with open("innocent.json", "r") as f:
    innocent_cards = json.load(f)

with open("guilty.json", "r") as f:
    guilty_cards = json.load(f)

# Helper function to select cards
def select_cards():
    innocents = random.sample(innocent_cards, 2)
    guilty = random.choice(guilty_cards)
    return innocents, guilty

# Select cards for each track
track1_innocent, track1_guilty = select_cards()
track2_innocent, track2_guilty = select_cards()

# Calculate total weights
def track_weight(innocents, guilty):
    return sum(card["weight"] for card in innocents) + guilty["weight"]

track1_weight = track_weight(track1_innocent, track1_guilty)
track2_weight = track_weight(track2_innocent, track2_guilty)

# Determine outcome
if track1_weight >= track2_weight:
    winner = "Track 1"
    loser = "Track 2"
else:
    winner = "Track 2"
    loser = "Track 1"

def print_track(track_name, innocents, guilty, total_weight):
    print(f"\n{track_name}")
    print("-" * len(track_name))
    for card in innocents:
        print(f"Innocent: {card['card']} (weight {card['weight']})")
    print(f"Guilty:   {guilty['card']} (weight {guilty['weight']})")
    print(f"TOTAL WEIGHT: {total_weight}")

if __name__ == '__main__':
    print_track("Track 1", track1_innocent, track1_guilty, track1_weight)
    print_track("Track 2", track2_innocent, track2_guilty, track2_weight)

    print("\nRESULT")
    print("------")
    print(f"{winner} LIVES")
    print(f"{loser} DIES")

