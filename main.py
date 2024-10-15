import random
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

CARD_WIDTH = 100  # Width of the card images
CARD_HEIGHT = 150  # Height of the card images
global player_balance


def calculate_hand_value(hand):
    """Calculate the value of a hand."""
    value = sum(card[1] for card in hand)
    if any(card[1] == 11 for card in hand) and value > 21:
        value -= 10
    return value


def display_hands():
    """Update the display of hands."""
    for widget in player_frame.winfo_children():
        widget.destroy()
    for widget in dealer_frame.winfo_children():
        widget.destroy()

    for card, value in player_hand:
        card_image = Image.open(f"images/{card}.png").resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
        card_photo = ImageTk.PhotoImage(card_image)
        label = tk.Label(player_frame, image=card_photo)
        label.image = card_photo
        label.pack(side=tk.LEFT, padx=5)

    if show_all_dealer_cards:
        for card, value in dealer_hand:
            card_image = Image.open(f"images/{card}.png").resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
            card_photo = ImageTk.PhotoImage(card_image)
            label = tk.Label(dealer_frame, image=card_photo)
            label.image = card_photo
            label.pack(side=tk.LEFT, padx=5)
    else:
        card_image = Image.open(f"images/{dealer_hand[0][0]}.png").resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
        card_photo = ImageTk.PhotoImage(card_image)
        label = tk.Label(dealer_frame, image=card_photo)
        label.image = card_photo
        label.pack(side=tk.LEFT, padx=5)

        hidden_card = Image.open("images/back.png").resize((CARD_WIDTH, CARD_HEIGHT), Image.LANCZOS)
        hidden_card_photo = ImageTk.PhotoImage(hidden_card)
        label = tk.Label(dealer_frame, image=hidden_card_photo)
        label.image = hidden_card_photo
        label.pack(side=tk.LEFT, padx=5)

    player_hand_value = calculate_hand_value(player_hand)
    dealer_hand_value = calculate_hand_value(dealer_hand) if show_all_dealer_cards else dealer_hand[0][1]

    player_value_label.config(text=f"Your hand value: {player_hand_value}")
    if show_all_dealer_cards:
        dealer_value_label.config(text=f"Dealer's hand value: {calculate_hand_value(dealer_hand)}")
    else:
        dealer_value_label.config(text="Dealer's hand value: Hidden")


def hit():
    """Player chooses to hit."""
    global player_balance
    player_hand.append(random.choice(deck))
    if calculate_hand_value(player_hand) > 21:
        end_game("bust")
    else:
        display_hands()


def stand():
    """Player chooses to stand."""
    global show_all_dealer_cards
    show_all_dealer_cards = True
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(random.choice(deck))
    display_hands()
    if calculate_hand_value(dealer_hand) > 21:
        end_game("dealer_bust")
    else:
        determine_winner()


def double_down():
    """Player chooses to double down."""
    global player_balance, player_wager
    player_wager *= 2
    player_balance -= player_wager // 2
    update_balance()
    player_hand.append(random.choice(deck))
    display_hands()
    if calculate_hand_value(player_hand) > 21:
        end_game("bust")
    else:
        stand()


def end_game(result):
    """End the game and show result."""
    global player_score, dealer_score, player_balance, player_wager
    global show_all_dealer_cards
    show_all_dealer_cards = True  # Reveal the dealer's hand
    display_hands()

    if result == "bust":
        dealer_score += 1
        messagebox.showinfo("Game Over", "You busted! Dealer wins!")
    elif result == "dealer_bust":
        player_score += 1
        player_balance += player_wager * 2
        messagebox.showinfo("Game Over", "Dealer busted! You win!")
    else:
        determine_winner()

    update_scoreboard()
    reset_game()


def determine_winner():
    """Determine the winner of the game."""
    global player_score, dealer_score, player_balance, player_wager
    player_hand_value = calculate_hand_value(player_hand)
    dealer_hand_value = calculate_hand_value(dealer_hand)

    if player_hand_value > dealer_hand_value:
        player_score += 1
        player_balance += player_wager * 2
        messagebox.showinfo("Game Over", "You win!")
    elif player_hand_value < dealer_hand_value:
        dealer_score += 1
        messagebox.showinfo("Game Over", "Dealer wins!")
    else:
        player_balance += player_wager
        messagebox.showinfo("Game Over", "It's a stand-off!")
    update_scoreboard()
    update_balance()
    reset_game()


def update_scoreboard():
    """Update the scoreboard."""
    scoreboard_label.config(text=f"Score - Player: {player_score} | Dealer: {dealer_score}")


def update_balance():
    """Update the player's balance."""
    balance_label.config(text=f"Balance: ${player_balance}")


def reset_game():
    """Reset the game for a new round."""
    global player_hand, dealer_hand, show_all_dealer_cards, player_wager, player_balance
    if player_balance <= 0:
        messagebox.showinfo("Game Over", "You are out of balance. Game over!")
        root.quit()

    player_wager = simpledialog.askinteger("Wager", f"Your balance is ${player_balance}. Enter your wager:", minvalue=1,
                                           maxvalue=player_balance)
    player_balance -= player_wager
    update_balance()

    player_hand = [random.choice(deck), random.choice(deck)]
    dealer_hand = [random.choice(deck), random.choice(deck)]
    show_all_dealer_cards = False
    display_hands()

    if calculate_hand_value(player_hand) == 21:
        end_game("blackjack")


def start_game():
    """Start the game."""
    global player_balance
    player_balance = simpledialog.askinteger("Balance", "Enter your starting balance:", minvalue=1)
    reset_game()
    root.mainloop()


# Initialize game variables
deck = [(f"{rank}_of_{suit}", value) for suit in ["hearts", "diamonds", "clubs", "spades"] for rank, value in zip(
    ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"],
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])]
random.shuffle(deck)

player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0
show_all_dealer_cards = False
player_balance = 0
player_wager = 0

# Create the main window
root = tk.Tk()
root.title("Blackjack")
root.geometry("800x600")

# Set the background image
background_image = ImageTk.PhotoImage(Image.open("images/background.png").resize((800, 600), Image.LANCZOS))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create frames for hands
player_frame = tk.Frame(root, bg="green")
player_frame.pack(side=tk.BOTTOM, pady=20)

dealer_frame = tk.Frame(root, bg="green")
dealer_frame.pack(side=tk.TOP, pady=20)

# Create labels for hand values
player_value_label = tk.Label(root, text="", bg="green", fg="white", font=("Helvetica", 16))
player_value_label.pack(side=tk.BOTTOM)

dealer_value_label = tk.Label(root, text="", bg="green", fg="white", font=("Helvetica", 16))
dealer_value_label.pack(side=tk.TOP)

# Create balance label
balance_label = tk.Label(root, text="Balance: $0", bg="green", fg="white", font=("Helvetica", 16))
balance_label.pack()

# Create scoreboard
scoreboard_label = tk.Label(root, text="Score - Player: 0 | Dealer: 0", bg="green", fg="white", font=("Helvetica", 16))
scoreboard_label.pack()

# Create buttons for actions
button_frame = tk.Frame(root, bg="green")
button_frame.pack(side=tk.BOTTOM, pady=10)

hit_button = tk.Button(button_frame, text="Hit", command=hit, bg="yellow", font=("Helvetica", 16))
hit_button.pack(side=tk.LEFT, padx=20)

stand_button = tk.Button(button_frame, text="Stand", command=stand, bg="yellow", font=("Helvetica", 16))
stand_button.pack(side=tk.RIGHT, padx=20)

double_down_button = tk.Button(button_frame, text="Double Down", command=double_down, bg="yellow",
                               font=("Helvetica", 16))
double_down_button.pack(side=tk.LEFT, padx=20)

# Start the game
start_game()