import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Card values and suits
suits = ["♥", "♦", "♣", "♠"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}

# Deck of cards
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append((rank, suit))
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

# Hand of cards
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card[0]]
        if card[0] == "A":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Blackjack game logic
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.wins = 0
        self.losses = 0
        self.load_stats()

    def hit(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.adjust_for_ace()
        if self.player_hand.value > 21:
            self.end_game("Bust! You went over 21. Dealer wins.")

    def stand(self):
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
            self.dealer_hand.adjust_for_ace()
        self.end_game()

    def end_game(self, message=None):
        if not message:
            if self.dealer_hand.value > 21:
                message = "Dealer busts! You win!"
                self.wins += 1
            elif self.player_hand.value > self.dealer_hand.value:
                message = "You win!"
                self.wins += 1
            elif self.player_hand.value < self.dealer_hand.value:
                message = "Dealer wins!"
                self.losses += 1
            else:
                message = "It's a tie!"
        messagebox.showinfo("Game Over", message)
        self.save_stats()
        self.reset_game()

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.gui.update_display()

    def load_stats(self):
        if os.path.exists("blackjack_stats.json"):
            with open("blackjack_stats.json", "r") as file:
                stats = json.load(file)
                self.wins = stats.get("wins", 0)
                self.losses = stats.get("losses", 0)

    def save_stats(self):
        stats = {"wins": self.wins, "losses": self.losses}
        with open("blackjack_stats.json", "w") as file:
            json.dump(stats, file)

# Function to create ASCII card visuals
def create_card_visual(card, hidden=False):
    rank, suit = card
    if hidden:
        return [
            "┌─────────┐",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "│░░░░░░░░░│",
            "└─────────┘"
        ]
    return [
        f"┌─────────┐",
        f"│{rank.ljust(2)}       │",
        "│         │",
        f"│    {suit}    │",
        "│         │",
        f"│       {rank.rjust(2)}│",
        "└─────────┘"
    ]

# Function to display cards in a row
def display_cards(cards, hidden=False):
    card_visuals = []
    for i, card in enumerate(cards):
        if hidden and i == 0:  # Hide the first card for the dealer
            card_visuals.append(create_card_visual(card, hidden=True))
        else:
            card_visuals.append(create_card_visual(card))
    # Combine card visuals line by line
    combined = []
    for line in range(7):  # Each card has 7 lines
        combined_line = ""
        for card in card_visuals:
            combined_line += card[line] + " "
        combined.append(combined_line)
    return "\n".join(combined)

# GUI for the game
class BlackjackGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Blackjack")
        self.window.geometry("600x400")  # Set initial window size

        # Win/Loss Tracker
        self.stats_label = tk.Label(self.window, text=f"Wins: {self.game.wins}  Losses: {self.game.losses}", font=("Courier", 12), anchor="w")
        self.stats_label.pack(pady=10, anchor="w")

        # Labels for player and dealer hands
        self.player_label = tk.Label(self.window, text="Player's Hand:", font=("Courier", 14))
        self.player_label.pack(pady=10)

        self.player_cards = tk.Label(self.window, text="", font=("Courier", 12))
        self.player_cards.pack()

        self.dealer_label = tk.Label(self.window, text="Dealer's Hand:", font=("Courier", 14))
        self.dealer_label.pack(pady=10)

        self.dealer_cards = tk.Label(self.window, text="", font=("Courier", 12))
        self.dealer_cards.pack()

        # Buttons for hit and stand
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, font=("Arial", 14), width=10)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, font=("Arial", 14), width=10)
        self.stand_button.pack(side=tk.RIGHT, padx=10)

        # Update the display
        self.update_display()

    def hit(self):
        self.game.hit()
        self.update_display()

    def stand(self):
        self.game.stand()
        self.update_display()

    def update_display(self):
        # Update win/loss stats
        self.stats_label.config(text=f"Wins: {self.game.wins}  Losses: {self.game.losses}")

        # Display player's cards
        player_cards_text = display_cards(self.game.player_hand.cards)
        self.player_cards.config(text=f"{player_cards_text}\nValue: {self.game.player_hand.value}")

        # Display dealer's cards (hide the first card initially)
        dealer_cards_text = display_cards(self.game.dealer_hand.cards, hidden=True)
        self.dealer_cards.config(text=dealer_cards_text)

# Start the game
if __name__ == "__main__":
    game = BlackjackGame()
    gui = BlackjackGUI(game)
    game.gui = gui
    gui.window.mainloop()