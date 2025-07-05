import tkinter as tk
import random

class GameHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Casino Hub")
        self.geometry("500x1050")
        self.resizable(True, True)
        self.configure(bg="#2e2e2e")
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text="🎲 Casino Hub", font=("Arial", 24, "bold"), bg="#2e2e2e", fg="white")
        title.pack(pady=20)

        # Game Buttons
        btn_frame = tk.Frame(self, bg="#2e2e2e")
        btn_frame.pack(pady=20)

        games = [
            ("Dice Roller", self.show_dice_roller),
            ("Blackjack", self.show_blackjack),
            ("Casino Mines", self.show_mines),
            ("Roulette", self.show_roulette),
            ("Coin Flip", self.show_coin_flip),
        ]

        for game_name, command in games:
            btn = tk.Button(btn_frame, text=game_name, font=("Arial", 16), bg="#3a3a3a", fg="white", width=20,
                            command=command)
            btn.pack(pady=10)

        # Game Area
        self.game_frame = tk.Frame(self, bg="#1e1e1e")
        self.game_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.output_label = tk.Label(self.game_frame, text="Select a game to begin", font=("Arial", 14),
                                     bg="#1e1e1e", fg="white", wraplength=580)
        self.output_label.pack(pady=20)

    def clear_game_frame(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()

    # Dice Roller
    def show_dice_roller(self):
        self.clear_game_frame()

        label = tk.Label(self.game_frame, text="🎲 Dice Roller", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
        label.pack(pady=10)

        result = tk.Label(self.game_frame, text="Roll a dice!", font=("Courier", 20), bg="#1e1e1e", fg="lime")
        result.pack(pady=10)

        dice_frame = tk.Frame(self.game_frame, bg="#1e1e1e")
        dice_frame.pack(pady=10)

        dice_types = [4, 6, 8, 10, 12, 20]

        qty_frame = tk.Frame(self.game_frame, bg="#1e1e1e")
        qty_frame.pack(pady=10)
        tk.Label(qty_frame, text="Number of Dice:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=5)
        qty_entry = tk.Entry(qty_frame, width=5, font=("Arial", 14))
        qty_entry.insert(0, "1")
        qty_entry.pack(side=tk.LEFT)

        ascii_dice_art = {
            1: "[     ]\n[  *  ]\n[     ]",
            2: "[*    ]\n[     ]\n[    *]",
            3: "[*    ]\n[  *  ]\n[    *]",
            4: "[*   *]\n[     ]\n[*   *]",
            5: "[*   *]\n[  *  ]\n[*   *]",
            6: "[*   *]\n[*   *]\n[*   *]",
        }

        def roll_dice(sides):
            try:
                qty = int(qty_entry.get())
                if qty < 1:
                    qty = 1
            except ValueError:
                qty = 1

            rolls = [random.randint(1, sides) for _ in range(qty)]

            art_lines = [""] * 3
            for roll in rolls:
                art = ascii_dice_art.get(roll, f"[ {roll} ]\n[  ?  ]\n[     ]").split('\n')
                for i in range(3):
                    art_lines[i] += art[i] + "  "

            combined_art = '\n'.join(art_lines)
            result.config(text=combined_art + f"\n\nRolls: {rolls}\nTotal: {sum(rolls)}")

        for sides in dice_types:
            btn = tk.Button(dice_frame, text=f"D{sides}", font=("Arial", 14), bg="#3a3a3a", fg="white",
                            command=lambda s=sides: roll_dice(s))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    # Blackjack
    def show_blackjack(self):
        self.clear_game_frame()
        self.blackjack_setup()

    def blackjack_setup(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

        title = tk.Label(self.game_frame, text="🃏 Blackjack", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=10)

        info_frame = tk.Frame(self.game_frame, bg="#1e1e1e")
        info_frame.pack(pady=10)

        self.dealer_label = tk.Label(info_frame, text="Dealer's Hand:", font=("Arial", 16), bg="#1e1e1e", fg="white")
        self.dealer_label.grid(row=0, column=0, sticky="w", padx=10)

        self.dealer_cards_label = tk.Label(info_frame, text="", font=("Courier", 16), bg="#1e1e1e", fg="yellow")
        self.dealer_cards_label.grid(row=1, column=0, sticky="w", padx=10)

        self.player_label = tk.Label(info_frame, text="Your Hand:", font=("Arial", 16), bg="#1e1e1e", fg="white")
        self.player_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20,0))

        self.player_cards_label = tk.Label(info_frame, text="", font=("Courier", 16), bg="#1e1e1e", fg="lime")
        self.player_cards_label.grid(row=3, column=0, sticky="w", padx=10)

        self.status_label = tk.Label(self.game_frame, text="", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white")
        self.status_label.pack(pady=20)

        btn_frame = tk.Frame(self.game_frame, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        self.deal_button = tk.Button(btn_frame, text="Deal", font=("Arial", 14), bg="#3a3a3a", fg="white", width=10,
                                     command=self.blackjack_deal)
        self.deal_button.grid(row=0, column=0, padx=5)

        self.hit_button = tk.Button(btn_frame, text="Hit", font=("Arial", 14), bg="#3a3a3a", fg="white", width=10,
                                    command=self.blackjack_hit, state=tk.DISABLED)
        self.hit_button.grid(row=0, column=1, padx=5)

        self.stand_button = tk.Button(btn_frame, text="Stand", font=("Arial", 14), bg="#3a3a3a", fg="white", width=10,
                                      command=self.blackjack_stand, state=tk.DISABLED)
        self.stand_button.grid(row=0, column=2, padx=5)

        self.restart_button = tk.Button(btn_frame, text="Restart", font=("Arial", 14), bg="#3a3a3a", fg="white", width=10,
                                        command=self.show_blackjack)
        self.restart_button.grid(row=0, column=3, padx=5)

        self.status_label.config(text="Click Deal to start!")

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [f"{rank}{suit}" for suit in suits for rank in ranks]

    def blackjack_deal(self):
        if self.game_over:
            return

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.update_blackjack_display(hide_dealer_card=True)

        self.deal_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        if self.calculate_hand_value(self.player_hand) == 21:
            self.blackjack_end_game("Blackjack! You win!")

    def blackjack_hit(self):
        if self.game_over:
            return
        self.player_hand.append(self.deck.pop())
        self.update_blackjack_display(hide_dealer_card=True)
        if self.calculate_hand_value(self.player_hand) > 21:
            self.blackjack_end_game("Bust! You lose!")

    def blackjack_stand(self):
        if self.game_over:
            return
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.deal_button.config(state=tk.DISABLED)

        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_blackjack_display(hide_dealer_card=False)
            self.update()

        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if dealer_value > 21:
            self.blackjack_end_game("Dealer busts! You win!")
        elif dealer_value > player_value:
            self.blackjack_end_game("Dealer wins!")
        elif dealer_value < player_value:
            self.blackjack_end_game("You win!")
        else:
            self.blackjack_end_game("Push! It's a tie!")

    def blackjack_end_game(self, message):
        self.game_over = True
        self.status_label.config(text=message)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.deal_button.config(state=tk.DISABLED)
        self.update_blackjack_display(hide_dealer_card=False)

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                aces += 1
                value += 11
            else:
                value += int(rank)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def update_blackjack_display(self, hide_dealer_card=True):
        if hide_dealer_card:
            dealer_display = f"{self.dealer_hand[0]} [??]"
        else:
            dealer_display = ' '.join(self.dealer_hand) + f"  (Value: {self.calculate_hand_value(self.dealer_hand)})"
        player_display = ' '.join(self.player_hand) + f"  (Value: {self.calculate_hand_value(self.player_hand)})"

        self.dealer_cards_label.config(text=dealer_display)
        self.player_cards_label.config(text=player_display)

    # Casino Mines
    def show_mines(self):
        self.clear_game_frame()

        self.grid_size = 5
        self.num_mines = 5
        self.mines = set(random.sample(range(self.grid_size**2), self.num_mines))
        self.revealed = set()
        self.game_over = False
        self.score = 0

        title = tk.Label(self.game_frame, text="💣 Casino Mines", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=10)

        self.score_label = tk.Label(self.game_frame, text=f"Score: {self.score}", font=("Arial", 16), bg="#1e1e1e", fg="lime")
        self.score_label.pack(pady=5)

        self.status_label = tk.Label(self.game_frame, text="Click tiles to reveal safe spots. Avoid mines!", font=("Arial", 14), bg="#1e1e1e", fg="white")
        self.status_label.pack(pady=5)

        grid_frame = tk.Frame(self.game_frame, bg="#1e1e1e")
        grid_frame.pack(pady=10)

        self.buttons = []

        def on_click(idx):
            if self.game_over or idx in self.revealed:
                return
            if idx in self.mines:
                self.buttons[idx].config(text="💥", bg="red")
                self.status_label.config(text="Boom! You hit a mine. Game over.", fg="red")
                self.game_over = True
                # Reveal all mines
                for i in self.mines:
                    if i != idx:
                        self.buttons[i].config(text="💣", bg="#aa0000")
            else:
                self.buttons[idx].config(text="✅", bg="green")
                self.revealed.add(idx)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                if self.score == self.grid_size**2 - self.num_mines:
                    self.status_label.config(text="Congrats! You cleared all safe spots!", fg="lime")
                    self.game_over = True

        for i in range(self.grid_size**2):
            btn = tk.Button(grid_frame, text="", width=4, height=2, bg="#3a3a3a", fg="white", font=("Arial", 18, "bold"),
                            command=lambda i=i: on_click(i))
            btn.grid(row=i // self.grid_size, column=i % self.grid_size, padx=5, pady=5)
            self.buttons.append(btn)

        restart_btn = tk.Button(self.game_frame, text="Restart", font=("Arial", 16), bg="#3a3a3a", fg="white",
                                command=self.show_mines)
        restart_btn.pack(pady=15)

    # Roulette (placeholder)
    def show_roulette(self):
        self.clear_game_frame()
        label = tk.Label(self.game_frame, text="🎡 Roulette (Coming Soon)", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
        label.pack(pady=20)

    # Coin Flip game
    def show_coin_flip(self):
        self.clear_game_frame()

        title = tk.Label(self.game_frame, text="🪙 Coin Flip", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=20)

        self.coin_label = tk.Label(self.game_frame, text="Flip the coin!", font=("Arial", 48), bg="#1e1e1e", fg="yellow")
        self.coin_label.pack(pady=40)

        result_label = tk.Label(self.game_frame, text="", font=("Arial", 24), bg="#1e1e1e", fg="lime")
        result_label.pack(pady=20)

        def flip():
            self.coin_label.config(text="🪙")
            result_label.config(text="Flipping...")
            self.update()

            # Simple flip animation
            for _ in range(10):
                self.coin_label.config(text=random.choice(["🪙", "✨", "💫", "🔄"]))
                self.update()
                self.after(50)

            outcome = random.choice(["Heads", "Tails"])
            result_label.config(text=f"Result: {outcome}")
            if outcome == "Heads":
                self.coin_label.config(text="🙂")
            else:
                self.coin_label.config(text="🙃")

        flip_btn = tk.Button(self.game_frame, text="Flip Coin", font=("Arial", 16), bg="#3a3a3a", fg="white", command=flip)
        flip_btn.pack(pady=20)


if __name__ == "__main__":
    app = GameHub()
    app.mainloop()