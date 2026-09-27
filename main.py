import tkinter as tk

from sympy import sympify, simplify, zoo, lambdify
from pint import UnitRegistry

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PINT UNIT REGISTRY
# ============================================================

ureg = UnitRegistry()


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
        "simplify": "Simplify",
        "convert": "Convert",
        "unit_converter": "Unit Converter",
        "unit_invalid": "Invalid Unit Conversion",
        "plot": "Plot",
    },
    "Marathi": {
        "title": "गणक",
        "clear": "साफ करा",
        "backspace": "मागे",
        "translate": "English",
        "invalid": "अवैध उदाहरण",
        "zero": "शून्याने भागाकार करता येत नाही",
        "simplify": "सोपे करा",
        "convert": "रूपांतर करा",
        "unit_converter": "एकक रूपांतरक",
        "unit_invalid": "अवैध एकक रूपांतरण",
        "plot": "आलेख",
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
root.geometry("400x900")
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
    Add a number, operator, or scientific function
    to the display.
    """

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
    Calculate the expression using SymPy.
    """

    try:
        expression = display.get()

        # Convert Marathi digits to English digits.
        expression = expression.translate(MARATHI_TO_ENGLISH)

        # Evaluate expression using SymPy.
        result = sympify(expression)

        # Check for division by zero.
        if result.has(zoo):
            raise ZeroDivisionError

        # Remove unnecessary formatting for integers.
        if getattr(result, "is_Integer", False):
            result = int(result)

        result = str(result)

        # Convert result to Marathi digits.
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


def simplify_expression():
    """
    Simplify a mathematical expression using SymPy.
    """

    try:
        expression = display.get()

        expression = expression.translate(MARATHI_TO_ENGLISH)

        result = simplify(sympify(expression))

        result = str(result)

        if current_language == "Marathi":
            result = result.translate(ENGLISH_TO_MARATHI)

        display.delete(0, tk.END)
        display.insert(0, result)

    except Exception:

        display.delete(0, tk.END)
        display.insert(0, LANGUAGES[current_language]["invalid"])


# ============================================================
# PLOT FUNCTION
# ============================================================


def plot_expression():
    """
    Plot a mathematical function using SymPy and Matplotlib.

    Example:
        x**2
        sin(x)
        cos(x)
        x**2 + 2*x + 1
    """

    try:
        expression = display.get()

        # Convert Marathi digits to English digits.
        expression = expression.translate(MARATHI_TO_ENGLISH)

        # Convert text into a SymPy expression.
        x = sympify("x")

        expr = sympify(expression)

        # Create a numerical function from the SymPy expression.
        function = lambdify(x, expr, "numpy")

        # Generate x values.
        x_values = np.linspace(-10, 10, 400)

        # Calculate y values.
        y_values = function(x_values)

        # Create graph.
        plt.figure(figsize=(7, 5))

        plt.plot(x_values, y_values, label=f"y = {expr}")

        plt.axhline(0, linewidth=0.8)

        plt.axvline(0, linewidth=0.8)

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title(f"Graph of y = {expr}")

        plt.grid(True)
        plt.legend()

        plt.show()

    except Exception:

        display.delete(0, tk.END)
        display.insert(0, LANGUAGES[current_language]["invalid"])


# ============================================================
# BASIC BUTTON FRAME
# ============================================================

button_frame = tk.Frame(root)

button_frame.pack(fill="both", padx=10, pady=5)


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
# SCIENTIFIC BUTTON FRAME
# ============================================================

scientific_frame = tk.Frame(root)

scientific_frame.pack(fill="both", padx=10, pady=5)


scientific_buttons = [
    ("√", "sqrt(", 0, 0),
    ("x²", "**2", 0, 1),
    ("sin", "sin(", 0, 2),
    ("cos", "cos(", 0, 3),
    ("tan", "tan(", 1, 0),
    ("log", "log(", 1, 1),
    ("(", "(", 1, 2),
    (")", ")", 1, 3),
]


for text, value, row, column in scientific_buttons:

    button = tk.Button(
        scientific_frame,
        text=text,
        font=("Arial", 13),
        command=lambda value=value: click(value),
    )

    button.grid(row=row, column=column, sticky="nsew", padx=3, pady=3)


# ============================================================
# SIMPLIFY BUTTON
# ============================================================

simplify_button = tk.Button(
    root, text="Simplify", font=("Arial", 13), command=simplify_expression
)

simplify_button.pack(fill="x", padx=10, pady=5)


# ============================================================
# PLOT BUTTON
# ============================================================

plot_button = tk.Button(root, text="Plot", font=("Arial", 13), command=plot_expression)

plot_button.pack(fill="x", padx=10, pady=5)


# ============================================================
# CLEAR / BACKSPACE BUTTONS
# ============================================================

clear_button = tk.Button(root, text="Clear", font=("Arial", 14), command=clear)

clear_button.pack(side="left", expand=True, fill="x", padx=(10, 3), pady=5)


backspace_button = tk.Button(
    root, text="Backspace", font=("Arial", 14), command=backspace
)

backspace_button.pack(side="left", expand=True, fill="x", padx=(3, 10), pady=5)


# ============================================================
# UNIT CONVERTER
# ============================================================

unit_frame = tk.LabelFrame(
    root, text="Unit Converter", font=("Arial", 12), padx=8, pady=8
)

unit_frame.pack(fill="x", padx=10, pady=10)


unit_value = tk.Entry(unit_frame, font=("Arial", 13))

unit_value.grid(row=0, column=0, columnspan=3, sticky="ew", padx=3, pady=3)

unit_value.insert(0, "100")


unit_from = tk.Entry(unit_frame, font=("Arial", 13))

unit_from.grid(row=1, column=0, sticky="ew", padx=3, pady=3)

unit_from.insert(0, "cm")


unit_arrow = tk.Label(unit_frame, text="→", font=("Arial", 14))

unit_arrow.grid(row=1, column=1, padx=3, pady=3)


unit_to = tk.Entry(unit_frame, font=("Arial", 13))

unit_to.grid(row=1, column=2, sticky="ew", padx=3, pady=3)

unit_to.insert(0, "m")


unit_result = tk.Label(
    unit_frame, text="Result: 1 meter", font=("Arial", 13), anchor="w"
)

unit_result.grid(row=2, column=0, columnspan=3, sticky="ew", padx=3, pady=5)


def convert_units():
    """
    Convert a physical quantity using Pint.
    """

    try:
        value = unit_value.get().strip()
        from_unit = unit_from.get().strip()
        to_unit = unit_to.get().strip()

        quantity = float(value) * ureg(from_unit)

        converted = quantity.to(to_unit)

        result = f"{converted.magnitude:g} {converted.units}"

        unit_result.config(text=f"Result: {result}")

    except Exception:

        unit_result.config(text=LANGUAGES[current_language]["unit_invalid"])


convert_button = tk.Button(
    unit_frame, text="Convert", font=("Arial", 13), command=convert_units
)

convert_button.grid(row=3, column=0, columnspan=3, sticky="ew", padx=3, pady=3)


for column in range(3):
    unit_frame.columnconfigure(column, weight=1)


# ============================================================
# TRANSLATE BUTTON
# ============================================================

translate_button = tk.Button(root, text="मराठी", font=("Arial", 14))

translate_button.pack(fill="x", padx=10, pady=5)


# ============================================================
# TRANSLATE INTERFACE
# ============================================================


def translate_interface():

    global current_language

    if current_language == "English":
        current_language = "Marathi"

    else:
        current_language = "English"

    language = LANGUAGES[current_language]

    root.title(language["title"])

    clear_button.config(text=language["clear"])

    backspace_button.config(text=language["backspace"])

    simplify_button.config(text=language["simplify"])

    plot_button.config(text=language["plot"])

    convert_button.config(text=language["convert"])

    unit_frame.config(text=language["unit_converter"])

    translate_button.config(text=language["translate"])

    current_display = display.get()

    if current_language == "Marathi":

        current_display = current_display.translate(ENGLISH_TO_MARATHI)

    else:

        current_display = current_display.translate(MARATHI_TO_ENGLISH)

    display.delete(0, tk.END)
    display.insert(0, current_display)

    # Change number button labels.
    for button, value in number_buttons:

        if value.isdigit():

            if current_language == "Marathi":

                button.config(text=value.translate(ENGLISH_TO_MARATHI))

            else:

                button.config(text=value)


translate_button.config(command=translate_interface)


# ============================================================
# RESIZE BUTTON GRIDS
# ============================================================

for row in range(4):
    button_frame.rowconfigure(row, weight=1)

for column in range(4):
    button_frame.columnconfigure(column, weight=1)

for row in range(2):
    scientific_frame.rowconfigure(row, weight=1)

for column in range(4):
    scientific_frame.columnconfigure(column, weight=1)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
