
class botAlpha:
    def __init__(self, player_id):
        self.player_id = player_id

    def choose_card(self, hand, top_card):
        # Very simple logic: play first valid card
        for card in hand:
            if card[0] == top_card[0] or card[1] == top_card[1]:
                return card
        return None  # draw a card if nothing matches
