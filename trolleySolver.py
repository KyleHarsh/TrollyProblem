import json
import random
import copy

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

if __name__ == '__main__':
    print_track("Track 1", track1_innocent, track1_guilty, track1_weight)
    print_track("Track 2", track2_innocent, track2_guilty, track2_weight)

    print("\nRESULT")
    print("------")
    print(f"{winner} LIVES")
    print(f"{loser} DIES")
