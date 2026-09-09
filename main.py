import tkinter as tk

# ============================================================
# TRANSLATIONS
# ============================================================

LANGUAGES = {
    "English": {
        "title": "Calculator",
        "clear": "Clear",
        "backspace": "Backspace",
        "translate": "मराठी",
        "invalid": "Invalid Expression",
        "zero": "Cannot Divide by Zero",
    },
    "Marathi": {
        "title": "गणक",
        "clear": "साफ करा",
        "backspace": "मागे",
        "translate": "English",
        "invalid": "अवैध उदाहरण",
        "zero": "शून्याने भागाकार करता येत नाही",
    },
}


# English digits -> Marathi digits
ENGLISH_TO_MARATHI = str.maketrans("0123456789", "०१२३४५६७८९")

# Marathi digits -> English digits
MARATHI_TO_ENGLISH = str.maketrans("०१२३४५६७८९", "0123456789")


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Calculator")
root.geometry("360x520")
root.resizable(False, False)

current_language = "English"


# ============================================================
# DISPLAY
# ============================================================

display = tk.Entry(root, font=("Arial", 26), justify="right", bd=8, relief="sunken")

display.pack(fill="both", padx=10, pady=10, ipady=10)


# ============================================================
# CALCULATOR FUNCTIONS
# ============================================================


def click(value):
    """
    Add a number/operator to the display.
    """

    # Convert English digits to Marathi digits
    # when Marathi mode is active.
    if current_language == "Marathi":
        value = value.translate(ENGLISH_TO_MARATHI)

    display.insert(tk.END, value)


def clear():
    """
    Clear calculator display.
    """
    display.delete(0, tk.END)


def backspace():
    """
    Delete the last character.
    """
    value = display.get()

    display.delete(0, tk.END)
    display.insert(0, value[:-1])


def calculate():
    """
    Calculate the expression.
    """

    try:
        expression = display.get()

        # Convert Marathi digits to English digits
        # before performing calculation.
        expression = expression.translate(MARATHI_TO_ENGLISH)

        # Only allow calculator characters.
        allowed = "0123456789+-*/.() "

        if not all(char in allowed for char in expression):
            raise ValueError

        # Calculate expression
        result = eval(expression, {"__builtins__": None}, {})

        # Remove unnecessary .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        result = str(result)

        # Convert result to Marathi digits
        # if Marathi mode is active.
        if current_language == "Marathi":
            result = result.translate(ENGLISH_TO_MARATHI)

        display.delete(0, tk.END)
        display.insert(0, result)

    except ZeroDivisionError:

        display.delete(0, tk.END)
        display.insert(0, LANGUAGES[current_language]["zero"])

    except Exception:

        display.delete(0, tk.END)
        display.insert(0, LANGUAGES[current_language]["invalid"])


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(root)

button_frame.pack(expand=True, fill="both", padx=10, pady=10)


# ============================================================
# NUMBER / OPERATOR BUTTONS
# ============================================================

buttons = [
    ("7", 0, 0),
    ("8", 0, 1),
    ("9", 0, 2),
    ("/", 0, 3),
    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("*", 1, 3),
    ("1", 2, 0),
    ("2", 2, 1),
    ("3", 2, 2),
    ("-", 2, 3),
    ("0", 3, 0),
    (".", 3, 1),
    ("=", 3, 2),
    ("+", 3, 3),
]


number_buttons = []


for text, row, column in buttons:

    if text == "=":
        command = calculate

    else:
        command = lambda value=text: click(value)

    button = tk.Button(button_frame, text=text, font=("Arial", 18), command=command)

    button.grid(row=row, column=column, sticky="nsew", padx=3, pady=3)

    number_buttons.append((button, text))


# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 14), command=clear)

clear_button.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=3, pady=3)


# ============================================================
# BACKSPACE BUTTON
# ============================================================

backspace_button = tk.Button(
    button_frame, text="Backspace", font=("Arial", 14), command=backspace
)

backspace_button.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=3, pady=3)


# ============================================================
# TRANSLATE BUTTON
# ============================================================

translate_button = tk.Button(root, text="मराठी", font=("Arial", 14))

translate_button.pack(fill="x", padx=10, pady=(0, 10))


# ============================================================
# TRANSLATE INTERFACE
# ============================================================


def translate_interface():

    global current_language

    # Switch language
    if current_language == "English":
        current_language = "Marathi"
    else:
        current_language = "English"

    language = LANGUAGES[current_language]

    # Change window title
    root.title(language["title"])

    # Change Clear button
    clear_button.config(text=language["clear"])

    # Change Backspace button
    backspace_button.config(text=language["backspace"])

    # Change Translate button
    translate_button.config(text=language["translate"])

    # Convert numbers already displayed
    current_display = display.get()

    if current_language == "Marathi":

        current_display = current_display.translate(ENGLISH_TO_MARATHI)

    else:

        current_display = current_display.translate(MARATHI_TO_ENGLISH)

    display.delete(0, tk.END)
    display.insert(0, current_display)

    # Change number button labels
    for button, value in number_buttons:

        if current_language == "Marathi":

            if value.isdigit():
                button.config(text=value.translate(ENGLISH_TO_MARATHI))

        else:

            if value.isdigit():
                button.config(text=value)


translate_button.config(command=translate_interface)


# ============================================================
# RESIZE BUTTON GRID
# ============================================================

for row in range(5):
    button_frame.rowconfigure(row, weight=1)

for column in range(4):
    button_frame.columnconfigure(column, weight=1)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
