import customtkinter as ctk
import random
import pyperclip
import datetime

# Setup theme
ctk.set_appearance_mode("system")  # ["light", "dark", "system"]
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# Character sets
LETTERS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
NUMBERS = list("0123456789")
SYMBOLS = list("!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")

# Password strength evaluator
def evaluate_strength(pwd):
    length = len(pwd)
    has_num = any(char.isdigit() for char in pwd)
    has_sym = any(char in SYMBOLS for char in pwd)
    has_upper = any(char.isupper() for char in pwd)
    has_lower = any(char.islower() for char in pwd)

    score = sum([has_num, has_sym, has_upper, has_lower])

    if length >= 12 and score == 4:
        return "Strong"
    elif length >= 8 and score >= 3:
        return "Medium"
    else:
        return "Weak"

# Password generation
def generate_password():
    try:
        n_letters = int(entry_letters.get())
        n_numbers = int(entry_numbers.get())
        n_symbols = int(entry_symbols.get())

        password_list = (
            random.choices(LETTERS, k=n_letters) +
            random.choices(NUMBERS, k=n_numbers) +
            random.choices(SYMBOLS, k=n_symbols)
        )
        random.shuffle(password_list)
        password = ''.join(password_list)
        entry_result.delete(0, ctk.END)
        entry_result.insert(0, password)

        pyperclip.copy(password)
        label_strength.configure(text=f"Strength: {evaluate_strength(password)}")

        save_password(password)
    except ValueError:
        entry_result.delete(0, ctk.END)
        entry_result.insert(0, "❌ Invalid Input")

# Save passwords to file
def save_password(pwd):
    with open("passwords.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {pwd}\n")

# Copy password manually
def copy_password():
    pyperclip.copy(entry_result.get())

# GUI setup
app = ctk.CTk()
app.title("Modern Password Generator")
app.geometry("450x400")

ctk.CTkLabel(app, text="🔐 Password Generator", font=("Arial", 24, "bold")).pack(pady=20)

frame_inputs = ctk.CTkFrame(app)
frame_inputs.pack(pady=10)

entry_letters = ctk.CTkEntry(frame_inputs, placeholder_text="Letters", width=120)
entry_letters.grid(row=0, column=0, padx=10, pady=10)

entry_numbers = ctk.CTkEntry(frame_inputs, placeholder_text="Numbers", width=120)
entry_numbers.grid(row=0, column=1, padx=10, pady=10)

entry_symbols = ctk.CTkEntry(frame_inputs, placeholder_text="Symbols", width=120)
entry_symbols.grid(row=0, column=2, padx=10, pady=10)
btn_generate = ctk.CTkButton(app, text="Generate", command=generate_password)
btn_generate.pack(pady=10)

entry_result = ctk.CTkEntry(app, width=300, height=35, font=("Arial", 14), justify="center")
entry_result.pack(pady=10)

label_strength = ctk.CTkLabel(app, text="Strength: ", font=("Arial", 14))
label_strength.pack(pady=5)

btn_copy = ctk.CTkButton(app, text="📋 Copy Password", command=copy_password)
btn_copy.pack(pady=5)

app.mainloop()
