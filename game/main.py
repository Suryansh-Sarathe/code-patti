
import zipfile
import importlib.util
import os
import shutil
from game_engine import Game
from rules import Rules

TEMP_DIR = "player_zips"

def load_bot(filepath, class_name, player_id):
    spec = importlib.util.spec_from_file_location(class_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bot_class = getattr(module, class_name)
    return bot_class(player_id=player_id)

def main():
    # Step 1: Extract ZIP
    zip_path = "submission.zip"
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    # Step 2: Identify bot files
    bot_files = sorted([f for f in os.listdir(TEMP_DIR) if f.endswith(".py")])
    assert len(bot_files) == 4, "Expected exactly 4 bot files."

    # Step 3: Load bot classes dynamically
    bots = {}
    for i, filename in enumerate(bot_files):
        class_name = filename[:-3]  # Strip '.py'
        filepath = os.path.join(TEMP_DIR, filename)
        bots[i] = load_bot(filepath, class_name, player_id=i)

    # Step 4: Initialize game with 4 players
    game = Game(num_players=4)

    # Step 5: Game loop
    while True:
        state = game.get_game_state()
        current_player = state["current_player"]
        top_card = state["top_card"]

        print("\n---------------------------")
        print(f"Top card: {top_card}")
        for pid in range(4):
            print(f"Player {pid} has {len(game.players[pid])} cards: {game.players[pid]}")

        current_bot = bots[current_player]
        hand = game.players[current_player]
        move = current_bot.choose_card(hand, top_card)

        print(f"Player {current_player} plays: {move if move else 'draws a card'}")
        if move:
            game.play_turn(current_player, move, current_bot)
        else:
            game.play_turn(current_player)

        if game.check_winner():
            print(f"\n🏆 Player {current_player} ({bot_files[current_player]}) wins!")
            break

if __name__ == "__main__":
    main()
