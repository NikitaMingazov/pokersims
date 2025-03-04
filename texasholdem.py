# algorithm : calculate your best hand, then enumerate the hands that beat it, then return the probability that at least one of your opponents has it
# if your best hand is indeterminate, then enumerate the possibilities, and do the above for each and return the average
#TODO: 1: implement hand evaluation, 2: deck generation and drawing, 3: potential hand enumeration
import sys
from math import prod

# prime table used for indexing
prime = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,  # Spades (0)
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,  # Hearts (1)
    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,  # Diamonds (2)
    173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239  # Clubs (3)
]
class Card:
    def __init__(self, suit, value):
        self.suit = suit  # 0: Spades, 1: Hearts, 2: Diamonds, 3: Clubs
        self.value = value  # 1: 2, 2: 3, ..., 13: Ace

    def __repr__(self):
        suits = ['S', 'H', 'D', 'C']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return f"{values[self.value - 1]}{suits[self.suit]}"

class Hand:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("Hand must contain exactly 5 cards.")
        self.cards = cards
        self.value_class = self.evaluate_hand()  # Hand strength (1: single, 9: royal flush)
        # self.metadata (defined in evaluate_hand)

    # Returns the hand strength class (1: single, 9: royal flush)
    def evaluate_hand(self):
        # stub
        return 1  # Default to single for now

    #TODO: fix logic to properly evaluate card values, currently this has false negatives in cases like equal pair but unequal high card
    def beats(self, other):
        """Compare two hands and return True if self beats other."""
        if self.value_class > other.value_class:
            return True
        elif self.value_class == other.value_class:
            return self.compare_metadata(other)
        else:
            return False

    def compare_metadata(self, other):
        """Compare metadata based on value_class using match-case."""
        match self.value_class:
            case 1:  # Single
                return max(self.cards, key=lambda x: x.value).value > max(other.cards, key=lambda x: x.value).value
            case 2:  # Pair
                return self.metadata['pair'] > other.metadata['pair']
            case 3:  # Two Pair
                return (self.metadata['pair1'], self.metadata['pair2']) > (other.metadata['pair1'], other.metadata['pair2'])
            case 4:  # Three of a Kind
                return self.metadata['triple'] > other.metadata['triple']
            case 5:  # Straight
                return self.metadata['straight_high'] > other.metadata['straight_high']
            case 6:  # Flush
                return max(self.cards, key=lambda x: x.value).value > max(other.cards, key=lambda x: x.value).value
            case 7:  # Full House
                return (self.metadata['triple'], self.metadata['pair']) > (other.metadata['triple'], other.metadata['pair'])
            case 8:  # Four of a Kind
                return self.metadata['quad'] > other.metadata['quad']
            case 9:  # Royal Flush
                return False  # Royal flushes are always a draw
            case _:
                raise ValueError("Invalid value_class")

    def __repr__(self):
        return f"Hand(cards={self.cards}, value_class={self.value_class}, metadata={self.metadata})"
# format input into an array of Card
def parse_cards(input_str):
    suit_map = {'S': 0, 'H': 1, 'D': 2, 'C': 3}
    value_map = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9,
                 'j': 10, 'q': 11, 'k': 12, 'a': 13, 'ace': 13, 'jack': 10, 'queen': 11, 'king': 12}

    cards = []
    for card_str in input_str.split(','):
        card_str = card_str.strip().lower()
        value = value_map[card_str[:-1]]
        suit = suit_map[card_str[-1].upper()]
        cards.append(Card(suit, value))
    return cards
# a bitmask is used to index hands
def compute_hand_index(cards):
    """Compute the unique index for a set of cards using prime products and reassigned suits."""
    # Group cards by suit
    suits = {0: [], 1: [], 2: [], 3: []}
    for card in cards:
        suits[card.suit].append(card.value)

    # Calculate the bitmask value of the suit
    suit_weights = {}
    for suit, values in suits.items():
        if values:
            weight = 0
            for value in values:
                weight |= 1 << (value - 1) # Set the bit that corresponds to the card's value
            suit_weights[suit] = weight

    # Sort suits by weight in descending order and reassign suit numbers
    sorted_suits = sorted(suit_weights.items(), key=lambda x: -x[1])
    reassigned_suits = {original_suit: new_suit for new_suit, (original_suit, _) in enumerate(sorted_suits)}

    # Compute the index as the product of primes for (reassigned suit, value) pairs
    index = 0
    for card in cards:
        reassigned_suit = reassigned_suits[card.suit]
        index |= 1 << reassigned_suit * 13 + (card.value - 1)
    return index

# Stub for probability calculation
def P(hand, players):
    # TODO: Implement probability calculation
    return 0.0

def main():
    if len(sys.argv) < 3:
        print("Usage: python texasholdem.py <player_count> <cards>")
        sys.exit(1)

    player_count = int(sys.argv[1])
    input_str = sys.argv[2]

    hand = parse_cards(input_str)
    hand_index = compute_hand_index(hand)

    print(f"Hand: {hand}")
    print(f"Hand Index: {hand_index}")

    probability = P(hand, player_count)
    print(f"Probability of winning: {probability}")

if __name__ == "__main__":
    main()
