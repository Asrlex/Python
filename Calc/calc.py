import tkinter as tk
from tkinter import messagebox, colorchooser
import numpy as np
import configparser
import sqlite3
from colors import get_colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tooltip import ToolTip
import datetime
import traceback

class CalculatorApp:
    """
    A simple calculator application using Tkinter.
    """
    BASIC_BUTTONS = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]
    TRIG_BUTTONS = [
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'exp', 
        'sinh', 'cosh', 'tanh', 'sqrt',
        'asinh', 'acosh', 'atanh', 'pow',
        'ln', 'log2', 'log10', ','
    ]
    TRIG_BUTTON_TOOLTIPS = {
        'sin': 'Sine function',
        'cos': 'Cosine function',
        'tan': 'Tangent function',
        'log': 'Logarithm function',
        'asin': 'Inverse sine function',
        'acos': 'Inverse cosine function',
        'atan': 'Inverse tangent function',
        'exp': 'Exponential function',
        'sinh': 'Hyperbolic sine function',
        'cosh': 'Hyperbolic cosine function',
        'tanh': 'Hyperbolic tangent function',
        'sqrt': 'Square root function',
        'asinh': 'Inverse hyperbolic sine function',
        'acosh': 'Inverse hyperbolic cosine function',
        'atanh': 'Inverse hyperbolic tangent function',
        'pow': 'Power function (base, exponent)'
    }
    UNIT_CONVERSION_BUTTONS = [
        'mm', 'cm', 'm', 'km',
        'in', 'ft', 'yd', 'mi',
        'mg', 'g', 'kg', 'ton',
        'oz', 'lb'
    ]
    ADVANCED_BUTTONS = [
        '7', '8', '9', '/', 'x**2', 'x**3', 'x**y',
        '4', '5', '6', '*', '1/x', 'e**x', '10**x',
        '1', '2', '3', '-', 'ln', 'log2', 'log10',
        '0', '.', '=', '+', '!', '(', ')'
    ]
    MODES = ['Basic', 'Trig', 'Units', 'Advanced']
    DEFAULT_DISPLAY_FONT = 'Courier New'

    def __init__(self, root):
        # Set root window properties
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)

        # Initialize instance variables
        self.font = 'Roboto'
        self.display_font = self.DEFAULT_DISPLAY_FONT
        self.calc_font_size = 12
        self.display_font_size = 16
        self.console_font_size = 10
        self.theme = 'Dark'
        self.colors = get_colors(self.theme)

        self.root.configure(bg=self.colors['background'])

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        # Create menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Settings menu
        settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences", command=self.open_settings)
        settings_menu.add_command(label="Clear History", command=self.clear_history)

        # Initialize database
        self.init_db()

        # Load settings
        self.load_settings()

        # Apply color theme
        self.colors = get_colors(self.theme)

        # Create display and buttons
        self.expression = ""
        self.create_display()
        self.create_history_console()
        self.load_history()
        self.button_area = tk.Frame(root, bg=self.colors['background'])
        self.button_area.grid(row=2, column=0, rowspan=3, columnspan=3, padx=20, pady=20, sticky='nsew')
        self.button_area_mode = ""
        self.create_aux_buttons()
        self.create_button_area()
        self.create_plot_canvas()

        self.function_map = {
            '=': self.evaluate_expression,
            'sin': self.apply_function,
            'cos': self.apply_function,
            'tan': self.apply_function,
            'asin': self.apply_function,
            'acos': self.apply_function,
            'atan': self.apply_function,
            'sinh': self.apply_function,
            'cosh': self.apply_function,
            'tanh': self.apply_function,
            'asinh': self.apply_function,
            'acosh': self.apply_function,
            'atanh': self.apply_function,
            'log': self.apply_function,
            'exp': self.apply_function,
            'sqrt': self.apply_function,
            'pow': self.apply_function,
            'mm': self.handle_unit_conversion,
            'cm': self.handle_unit_conversion,
            'm': self.handle_unit_conversion,
            'km': self.handle_unit_conversion,
            'mg': self.handle_unit_conversion,
            'g': self.handle_unit_conversion,
            'kg': self.handle_unit_conversion,
            'ton': self.handle_unit_conversion,
            'in': self.handle_unit_conversion,
            'ft': self.handle_unit_conversion,
            'yd': self.handle_unit_conversion,
            'mi': self.handle_unit_conversion,
            'oz': self.handle_unit_conversion,
            'lb': self.handle_unit_conversion,
            'ton': self.handle_unit_conversion,
            'x**2': self.apply_function,
            'x**3': self.apply_function,
            'x**y': self.apply_function,
            '1/x': self.apply_function,
            'e**x': self.apply_function,
            '10**x': self.apply_function,
            'ln': self.apply_function,
            'log2': self.apply_function,
            'log10': self.apply_function,
            '!': self.apply_function,
            '(': self.apply_function,
            ')': self.apply_function,
            ',': self.apply_function
        }

    # Initialization methods
    def init_db(self):
        self.conn = sqlite3.connect('history.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                expression TEXT,
                result TEXT
            )
        ''')
        self.conn.commit()

    def load_settings(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.settings = self.config['DEFAULT']

        # Apply settings
        self.font = self.settings.get('font', 'Times New Roman')
        self.display_font = self.settings.get('display_font', self.DEFAULT_DISPLAY_FONT)
        self.calc_font_size = self.settings.get('calc_font_size', 12)
        self.display_font_size = self.settings.get('display_font_size', 18)
        self.console_font_size = self.settings.get('console_font_size', 12)
        self.theme = self.settings.get('color_theme', 'Dark')

        # Apply color theme
        self.colors = get_colors(self.theme)

    def save_settings(self):
        self.settings['font'] = self.font_var.get()
        self.settings['display_font'] = self.display_font_var.get()
        self.settings['calc_font_size'] = str(self.font_size_var.get())
        self.settings['display_font_size'] = str(self.display_font_size_var.get())
        self.settings['console_font_size'] = str(self.console_font_size_var.get())
        self.settings['color_theme'] = self.color_theme_var.get()

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

        messagebox.showinfo("Settings", "Settings saved successfully!")

    # UI creation methods
    def create_display(self):
        self.display = tk.Text(
            self.root, 
            font=(self.display_font, self.display_font_size), 
            bd=10, 
            insertwidth=2, 
            borderwidth=4,
            relief='flat',
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            state='disabled',
            width=25,
            height=1.5,
            highlightbackground="gray",
            highlightthickness=1
        )
        self.display.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky='nsew')

    def create_history_console(self):
        self.history_console = tk.Text(
            self.root,
            font=(self.font, self.console_font_size),
            bd=10,
            insertwidth=2,
            borderwidth=4,
            relief='flat',
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            state='disabled',
            width=30,
            highlightbackground="gray",
            highlightthickness=1
        )
        self.history_console.grid(row=0, column=3, rowspan=4, padx=20, pady=20, sticky='ns')
        self.history_console.bind("<Button-1>", self.on_history_click)
        self.history_console.bind("<Motion>", self.on_history_hover)
        self.history_console.tag_configure("timestamp", foreground="gray")
        self.history_console.tag_configure("expression", foreground="lightblue")

    def create_aux_buttons(self):
        aux_buttons_area = tk.Frame(self.root, bg=self.colors['background'])
        aux_buttons_area.grid(row=1, column=0, columnspan=3, padx=20, pady=0, sticky='nsew')

        # Clear button
        tk.Button(
            aux_buttons_area, 
            text='Clear', 
            **self.button_style(), 
            command=self.clear
        ).grid(row=1, column=0, padx=5, pady=5)

        # Mode dropdown
        self.mode_var = tk.StringVar(value="Basic")
        mode_dropdown = tk.OptionMenu(
            aux_buttons_area, 
            self.mode_var, 
            *self.MODES, 
            command=self.change_mode
        )
        mode_dropdown.config(
            font=(self.font, self.calc_font_size),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground='#6A6A6A',
            activeforeground=self.colors['button_fg'],
            relief='raised'
        )
        mode_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Plot button (only visible in Advanced mode)
        self.plot_button = tk.Button(
            aux_buttons_area, 
            text="Plot", 
            **self.button_style(),
            command=self.draw_plot
        )
        self.plot_button.grid(row=1, column=2, padx=5, pady=5)
        self.plot_button.grid_remove()

    def create_button_area(self, mode="Basic"):
        self.clear_button_area()
        self.button_area_mode = mode

        # Make display editable in Advanced mode
        if mode == "Advanced":
            self.display.config(state='normal')
            self.display.bind("<KeyRelease>", self.update_expression)
        else:
            self.display.config(state='disabled')
            self.display.unbind("<KeyRelease>")

        # Buttons
        buttons = []
        if mode == "Basic":
            buttons = self.BASIC_BUTTONS
        elif mode == "Trig":
            buttons = self.TRIG_BUTTONS
        elif mode == "Units":
            buttons = self.UNIT_CONVERSION_BUTTONS
        elif mode == "Advanced":
            buttons = self.ADVANCED_BUTTONS
        else:
            buttons = self.BASIC_BUTTONS
        
        row = 1
        col = 0
        max_cols = 4
        if mode == "Advanced":
            max_cols = 7
        elif mode == "Trig":
            max_cols = 5
        for button in buttons:
            action = lambda x=button: self.click_event(x)
            btn = tk.Button(
                self.button_area,
                text=button,
                **self.button_style(),
                command=action
            )
            self.add_button(btn, row, col)
            self.add_hover_effect(btn)
            col += 1
            if col == max_cols:
                col = 0
                row += 1

        # Add key bindings for basic buttons
        if mode == "Basic":
            for button in self.BASIC_BUTTONS:
                self.root.bind(f"<KeyPress-{button}>", lambda event, b=button: self.click_event(b))

    def create_plot_canvas(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.plot_canvas.get_tk_widget().grid(row=0, column=4, rowspan=5, padx=20, pady=20, sticky='ns')

    # Event handling methods
    def on_history_click(self, event):
        index = self.history_console.index(f"@{event.x},{event.y}")
        line = self.history_console.get(f"{index} linestart", f"{index} lineend")
        if "=" in line:
            result = line.split("=")[-1].strip()
            self.expression = result
            self.display.config(state='normal')
            self.display.delete(1.0, tk.END)
            self.display.insert(tk.END, self.expression)
            self.display.config(state='disabled')

    def on_history_hover(self, event):
        index = self.history_console.index(f"@{event.x},{event.y}")
        line = self.history_console.get(f"{index} linestart", f"{index} lineend")
        if "=" in line:
            self.history_console.config(cursor="hand2")
        else:
            self.history_console.config(cursor="")

    def change_mode(self, mode):
        self.create_button_area(mode)
        if mode == "Advanced":
            self.plot_button.grid()
        else:
            self.plot_button.grid_remove()

    def clear_button_area(self):
        for widget in self.button_area.winfo_children():
            widget.destroy()

    def update_expression(self, event):
        self.expression = self.display.get("1.0", tk.END).strip()

    def click_event(self, key):
        if self.expression == "Error":
            self.expression = ""

        try:
            if key in self.function_map:
                self.function_map[key](key)
            else:
                self.expression += str(key)
        except Exception:
            self.expression = "Error"
            traceback.print_exc()
            self.history_console.config(state='normal')
            self.history_console.insert(tk.END, f"{self.expression}\n", "expression")
            self.history_console.config(state='disabled')

        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, self.expression)
        self.display.config(state='disabled')

    def add_button(self, button, row, col):
        button.grid(row=row, column=col, padx=5, pady=5)
        if button['text'] in self.TRIG_BUTTON_TOOLTIPS:
            ToolTip(button, self.TRIG_BUTTON_TOOLTIPS[button['text']])

    def add_hover_effect(self, button):
        def on_enter(e):
            button['bg'] = '#6A6A6A'
        def on_leave(e):
            button['bg'] = self.colors['button_bg']
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def button_style(self):
        return {
            'padx': 10, 
            'pady': 10, 
            'font': (self.font, self.calc_font_size),
            'width': 3,
            'height': 1,
            'bd': 2,
            'bg': self.colors['button_bg'],
            'fg': self.colors['button_fg'],
            'activebackground': '#6A6A6A',
            'activeforeground': self.colors['button_fg'],
            'relief': 'raised'
        }

    # Mathematical operations
    def evaluate_expression(self, key):
        result = str(eval(self.expression))
        self.add_to_history(self.expression, result)
        self.expression = result

    def apply_function(self, key):
        if key in ['log', 'exp', 'sqrt', 'pow', 'x**2', 'x**3', 'x**y', '1/x', 'e**x', '10**x', 'ln', 'log2', 'log10', '!', '(', ')', ',']:
            self.expression += key
        else:
            result = str(getattr(np, key)(eval(self.expression)))
            self.add_to_history(f"{key}({self.expression})", result)
            self.expression = result

    # Unit conversions
    def handle_unit_conversion(self, key):
        if self.expression == "":
            self.expression = ""
        elif self.expression[-3:] == " to":
            self.expression += f" {key}"
            value, unit = self.expression.split(" ")[0:2]
            result = self.convert_units(value, unit, key)
            self.add_to_history(self.expression, result)
            self.expression = result
        else:
            if self.expression[-1].isdigit():
                self.expression += f" {key} to"
            else:
                self.expression = ""

    def convert_units(self, value, from_unit, to_unit):
        switcher = {
            'mm': {
                'cm': lambda x: x / 10,
                'm': lambda x: x / 1000,
                'km': lambda x: x / 1000000,
                'in': lambda x: x / 25.4,
                'ft': lambda x: x / 304.8,
                'yd': lambda x: x / 914.4,
                'mi': lambda x: x / 1609344
            },
            'cm': {
                'mm': lambda x: x * 10,
                'm': lambda x: x / 100,
                'km': lambda x: x / 100000,
                'in': lambda x: x / 2.54,
                'ft': lambda x: x / 30.48,
                'yd': lambda x: x / 91.44,
                'mi': lambda x: x / 160934.4
            },
            'm': {
                'mm': lambda x: x * 1000,
                'cm': lambda x: x * 100,
                'km': lambda x: x / 1000,
                'in': lambda x: x * 39.37,
                'ft': lambda x: x * 3.281,
                'yd': lambda x: x * 1.094,
                'mi': lambda x: x / 1609.344
            },
            'km': {
                'mm': lambda x: x * 1000000,
                'cm': lambda x: x * 100000,
                'm': lambda x: x * 1000,
                'in': lambda x: x * 39370.079,
                'ft': lambda x: x * 3280.84,
                'yd': lambda x: x * 1093.613,
                'mi': lambda x: x / 1.609
            },
            'in': {
                'mm': lambda x: x * 25.4,
                'cm': lambda x: x * 2.54,
                'm': lambda x: x / 39.37,
                'km': lambda x: x / 39370.079,
                'ft': lambda x: x / 12,
                'yd': lambda x: x / 36,
                'mi': lambda x: x / 63360
            },
            'ft': {
                'mm': lambda x: x * 304.8,
                'cm': lambda x: x * 30.48,
                'm': lambda x: x / 3.281,
                'km': lambda x: x / 3280.84,
                'in': lambda x: x * 12,
                'yd': lambda x: x / 3,
                'mi': lambda x: x / 5280
            },
            'yd': {
                'mm': lambda x: x * 914.4,
                'cm': lambda x: x * 91.44,
                'm': lambda x: x / 1.094,
                'km': lambda x: x / 1093.613,
                'in': lambda x: x * 36,
                'ft': lambda x: x * 3,
                'mi': lambda x: x / 1760
            },
            'mi': {
                'mm': lambda x: x * 1609344,
                'cm': lambda x: x * 160934.4,
                'm': lambda x: x * 1609.344,
                'km': lambda x: x * 1.609,
                'in': lambda x: x * 63360,
                'ft': lambda x: x * 5280,
                'yd': lambda x: x * 1760
            },
            'mg': {
                'g': lambda x: x / 1000,
                'kg': lambda x: x / 1000000,
                'ton': lambda x: x / 1000000000,
                'oz': lambda x: x / 28349.523,
                'lb': lambda x: x / 453592.37,
            },
            'g': {
                'mg': lambda x: x * 1000,
                'kg': lambda x: x / 1000,
                'ton': lambda x: x / 1000000,
                'oz': lambda x: x / 28.35,
                'lb': lambda x: x / 453.592
            },
            'kg': {
                'mg': lambda x: x * 1000000,
                'g': lambda x: x * 1000,
                'ton': lambda x: x / 1000,
                'oz': lambda x: x * 35.274,
                'lb': lambda x: x * 2.205
            },
            'ton': {
                'mg': lambda x: x * 1000000000,
                'g': lambda x: x * 1000000,
                'kg': lambda x: x * 1000,
                'oz': lambda x: x * 35273.962,
                'lb': lambda x: x * 2204.623
            },
            'oz': {
                'mg': lambda x: x * 28349.523,
                'g': lambda x: x * 28.35,
                'kg': lambda x: x / 35.274,
                'ton': lambda x: x / 35273.962,
                'lb': lambda x: x / 16
            },
            'lb': {
                'mg': lambda x: x * 453592.37,
                'g': lambda x: x * 453.592,
                'kg': lambda x: x / 2.205,
                'ton': lambda x: x / 2204.623,
                'oz': lambda x: x * 16
            }
        }

        return str(switcher[from_unit][to_unit](float(value)))

    # History management
    def add_to_history(self, expression, result):
        self.history_console.config(state='normal')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_console.insert('1.0', "-"*20 + "\n", "timestamp")
        self.history_console.insert('1.0', f"{expression} = {result}\n", "expression")
        self.history_console.insert('1.0', f"{timestamp}\n", "timestamp")
        self.history_console.config(state='disabled')
        self.save_history(expression, result, timestamp)

    def save_history(self, expression, result, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO history (timestamp, expression, result)
            VALUES (?, ?, ?)
        ''', (timestamp, expression, result))
        self.conn.commit()

    def load_history(self):
        self.history_console.config(state='normal')
        self.cursor.execute('SELECT timestamp, expression, result FROM history ORDER BY timestamp asc')
        rows = self.cursor.fetchall()
        for row in rows:
            timestamp, expression, result = row
            self.history_console.insert('1.0', "-"*20 + "\n", "timestamp")
            self.history_console.insert('1.0', f"{expression} = {result}\n", "expression")
            self.history_console.insert('1.0', f"{timestamp}\n", "timestamp")
        self.history_console.config(state='disabled')

    def clear_history(self):
        self.cursor.execute('DELETE FROM history')
        self.conn.commit()
        self.history_console.config(state='normal')
        self.history_console.delete(1.0, tk.END)
        self.history_console.config(state='disabled')
        messagebox.showinfo("Clear History", "History cleared successfully!")

    # Settings management
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        tk.Label(settings_window, text="Font settings", font=(self.font, 16)
            ).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(settings_window, text="Font:", font=(self.font, self.calc_font_size)
            ).grid(row=1, column=0, padx=10, pady=2, sticky='e')
        self.font_var = tk.StringVar(value=self.settings.get('font', self.font))
        tk.Entry(settings_window, textvariable=self.font_var, font=(self.font, self.calc_font_size)
            ).grid(row=1, column=1, padx=10, pady=2, sticky='w')

        tk.Label(settings_window, text="Display Font:", font=(self.font, self.calc_font_size)
            ).grid(row=2, column=0, padx=10, pady=2, sticky='e')
        self.display_font_var = tk.StringVar(value=self.settings.get('display_font', self.display_font))
        tk.Entry(settings_window, textvariable=self.display_font_var, font=(self.font, self.calc_font_size)
            ).grid(row=2, column=1, padx=10, pady=2, sticky='w')

        tk.Label(settings_window, text="Calc font Size:", font=(self.font, self.calc_font_size)
            ).grid(row=3, column=0, padx=10, pady=2, sticky='e')
        self.font_size_var = tk.IntVar(value=self.settings.get('calc_font_size', self.calc_font_size))
        tk.Entry(settings_window, textvariable=self.font_size_var, font=(self.font, self.calc_font_size)
            ).grid(row=3, column=1, padx=10, pady=2, sticky='w')

        tk.Label(settings_window, text="Display Font Size:", font=(self.font, self.calc_font_size)
            ).grid(row=4, column=0, padx=10, pady=2, sticky='e')
        self.display_font_size_var = tk.IntVar(value=self.settings.get('display_font_size', self.display_font_size))
        tk.Entry(settings_window, textvariable=self.display_font_size_var, font=(self.font, self.calc_font_size)
            ).grid(row=4, column=1, padx=10, pady=2, sticky='w')

        tk.Label(settings_window, text="Console Font Size:", font=(self.font, self.calc_font_size)
            ).grid(row=5, column=0, padx=10, pady=2, sticky='e')
        self.console_font_size_var = tk.IntVar(value=self.settings.get('console_font_size', self.console_font_size))
        tk.Entry(settings_window, textvariable=self.console_font_size_var, font=(self.font, self.calc_font_size)
            ).grid(row=5, column=1, padx=10, pady=2, sticky='w')

        tk.Label(settings_window, text="Color settings", font=(self.font, 16)
            ).grid(row=6, column=0, columnspan=2, pady=10)

        tk.Label(settings_window, text="Color Theme:", font=(self.font, self.calc_font_size)
            ).grid(row=7, column=0, padx=10, pady=2, sticky='e')
        self.color_theme_var = tk.StringVar(value=self.settings.get('color_theme', self.theme))
        tk.Entry(settings_window, textvariable=self.color_theme_var, font=(self.font, self.calc_font_size)
            ).grid(row=7, column=1, padx=10, pady=2, sticky='w')

        tk.Button(settings_window, text="Save", command=self.save_settings).grid(row=8, column=0, columnspan=2, pady=20)

    # Plotting
    def draw_plot(self):
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(self.expression)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            self.plot_canvas.draw()
            self.add_to_history("Plotted", self.expression)
        except Exception as e:
            messagebox.showerror("Plot Error", f"Error plotting the function: {e}")

    # Miscellaneous
    def clear(self):
        self.expression = ""
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        self.display.config(state='disabled')

    def show_about(self):
        messagebox.showinfo("About", "This is a simple calculator application using Tkinter.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()