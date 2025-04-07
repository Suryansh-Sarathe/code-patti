import random
from deck import Deck
from rules import Rules

class Game:
    def __init__(self, num_players=4):
        self.deck = Deck()
        self.players = {0: [], 1: [],2: [], 3:[]}  # 0 = human, 1 = bot
        self.current_player = 0
        self.direction = 1
        self.played_cards = []
        self.initialize_hands()

    def initialize_hands(self):
        for pid in self.players:
            self.players[pid] = [self.deck.draw_card() for _ in range(7)]
        first_card = self.deck.draw_card()
        while first_card[1:] in ["W", "WR"]:  # Avoid wilds as first card
            self.deck.cards.append(first_card)
            random.shuffle(self.deck.cards)
            first_card = self.deck.draw_card()
        self.played_cards.append(first_card)

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 2

    def skip_turn(self):
        """Skip the next player's turn."""
        self.next_turn()
        self.next_turn()

    def reverse_turn_order(self):
        """Reverse the direction of turns."""
        self.direction *= -1

    def next_player_draw(self, num_cards):
        """Make the next player draw a specific number of cards."""
        next_player = (self.current_player + self.direction) % len(self.players)
        for _ in range(num_cards):
            self.players[next_player].append(self.deck.draw_card())
            
    def check_winner(self):
        """Check if a player has won the game."""
        for player, hand in self.players.items():
            if not hand:
                print(f"Player {player} wins!")
                return True
        return False

    def get_game_state(self):
        """Returns the game state with player card counts."""
        return {
            "player_card_counts": {player: len(hand) for player, hand in self.players.items()},
            "current_player": self.current_player,
            "top_card": self.played_cards[-1],
            "direction": "clockwise" if self.direction == 1 else "counterclockwise"
        }

    def play_turn(self, player, player_move=None, agent=None):
        """Handle a player's move."""
        if player != self.current_player:
            print("Not your turn!")
            return

        if player_move and Rules.is_valid_move(player_move, self.played_cards[-1]):
            self.played_cards.append(player_move)
            self.players[player].remove(player_move)
            Rules.apply_card_effect(player_move, self, agent)
            if not self.check_winner():
                self.next_turn()
        else:
            print("No valid moves, drawing a card...")
            drawn_card = self.deck.draw_card()
            self.players[player].append(drawn_card)
            if Rules.is_valid_move(drawn_card, self.played_cards[-1]):
                print(f"You drew {drawn_card}, and it can be played!")
            self.next_turn()

    
    def prompt_color_choice(self,action, agent):
        # chosen_color = input("Choose a color [R, G, B, Y]: ").strip().upper()
        chosen_color = agent.choose_color()
        print(self.players[self.current_player], "choose color")
        while chosen_color not in {'R', 'G', 'B', 'Y'}:
            # chosen_color = input("Invalid color. Choose from [R, G, B, Y]: ").strip().upper()
            chosen_color = agent.choose_color()
        self.set_next_color(chosen_color,action)

    
    def set_next_color(self, color, action):
        print(action + color, "color+action")
        self.played_cards[-1] = action + color  # <- correctly update top card
        print(self.played_cards[-1], "current top card")
        print(f"Color changed to {color}")

    
    def draw_card(self, player_name):
        if self.turn_order[self.current_player_idx] != player_name:
            return {'error': 'Not your turn'}
        drawn_card = self.deck.draw_card()
        self.players[player_name].append(drawn_card)
        self.next_turn()
        return {'message': 'Card drawn', 'card': drawn_card}

# Example Usage
if __name__ == "__main__":
    game = Game(num_players=4)
    print("Initial Player Hands:", game.get_game_state())
    # game.played_cards.append(game.deck.draw_card())  used it for just testing something
    print("Top Card:", game.played_cards[-1], game.played_cards)
