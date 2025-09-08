# ================= Store Inventory =================
available_parts = [
    ("Computer", "BigUdom Tech", 2500,
     [
        (1,"HP Laptops"),
        (2,"Macbooks"),
        (3,"Lenovo"),
        (4,"DELL"),
        (5,"Asus"),
        (6,"Acer"),
     ]
    ),
    ("Monitors", "FaziImports", 2000,
     [
        (1,"CRT Monitor"),
        (2,"LCD Monitor"),
        (3,"LED Monitor"),
        (4,"OLED Monitor"),
        (5,"Plasma Monitor"),
        (6,"TouchScreen Monitor"),
        (7,"Curved Monitor"),
     ]
    ),
    ("Keyboards", "KeyWorlds", 1000,
        [
            (1,"Standard Keys"),
            (2,"Ergonomic Keys"),
            (3,"Wireless Keys"),
            (4,"Gaming Keys"),
            (5,"Mechanical Keys"),
            (6,"Foldable Keyboard"),
        ]
    ),
    ("Mouse", "Bigudom Tech", 500,
        [
            (1,"Trackball"),
            (2,"Optical"),
            (3,"Wireless"),
            (4,"Gaming"),
            (5,"Laser"),
            (6,"Mechanical"),
            (7,"3D Mice"),
            (8,"Vertical Mouse"),
        ]
    ),
    ("HDMI Cable","JayWires", 300,
        [
            (1,"Type A"),
            (2,"Type B"),
            (3,"Type C"),
            (4,"Type D"),
            (5,"Type E"),
        ]
    ),
    ("Phones", "Spectrum Phones", 700,
        [
            (1,"Iphone"),
            (2,"Samsung"),
            (3,"Redmi"),
            (4,"Oppo"),
            (5,"Infinix"),
            (6,"Itel"),
            (7,"Tecno"),
            (8,"OnePlus"),
        ]
    ),
    ("Printers","OfficePro", 1500,
        [
            (1,"Inkjet Printer"),
            (2,"Laser Printer"),
            (3,"3D Printer"),
            (4,"Dot Matrix Printer"),
            (5,"Thermal Printer"),
        ]
    ),
    ("Tablets","SmartWorld", 1200,
        [
            (1,"iPad"),
            (2,"Samsung Galaxy Tab"),
            (3,"Amazon Fire"),
            (4,"Lenovo Tab"),
            (5,"Microsoft Surface"),
        ]
    ),
    ("Smartwatches","WristTech", 800,
        [
            (1,"Apple Watch"),
            (2,"Samsung Galaxy Watch"),
            (3,"Fitbit"),
            (4,"Huawei Watch"),
            (5,"Amazfit"),
        ]
    ),
    ("Speakers","SoundHub", 900,
        [
            (1,"Bluetooth Speaker"),
            (2,"Smart Speaker"),
            (3,"Home Theater Speaker"),
            (4,"Portable Mini Speaker"),
            (5,"Soundbar"),
        ]
    ),
]

price_tags = {
    "Computer": {
        "HP Laptops": 2100,
        "Macbooks": 2500,
        "Lenovo": 1900,
        "DELL": 1800,
        "Asus": 2000,
        "Acer": 1700,
    },
    "Monitors": {
        "CRT Monitor": 1200,
        "LCD Monitor": 1400,
        "LED Monitor": 1600,
        "OLED Monitor": 1500,
        "Plasma Monitor": 1800,
        "TouchScreen Monitor": 2000,
        "Curved Monitor": 2200,
    },
    "Keyboards": {
        "Standard Keys": 600,
        "Ergonomic Keys": 700,
        "Wireless Keys": 850,
        "Gaming Keys": 1000,
        "Mechanical Keys": 1200,
        "Foldable Keyboard": 900,
    },
    "Mouse": {
        "Trackball": 200,
        "Optical": 250,
        "Wireless": 400,
        "Gaming": 500,
        "Laser": 500,
        "Mechanical": 300,
        "3D Mice": 450,
        "Vertical Mouse": 350,
    },
    "HDMI Cable": {
        "Type A": 200,
        "Type B": 100,
        "Type C": 200,
        "Type D": 150,
        "Type E": 250,
    },
    "Phones": {
        "Iphone": 2200,
        "Samsung": 3000,
        "Redmi": 1000,
        "Oppo": 500,
        "Infinix": 400,
        "Itel": 200,
        "Tecno": 350,
        "OnePlus": 2800,
    },
    "Printers": {
        "Inkjet Printer": 1200,
        "Laser Printer": 2500,
        "3D Printer": 5000,
        "Dot Matrix Printer": 1000,
        "Thermal Printer": 800,
    },
    "Tablets": {
        "iPad": 3000,
        "Samsung Galaxy Tab": 2500,
        "Amazon Fire": 1500,
        "Lenovo Tab": 1800,
        "Microsoft Surface": 4000,
    },
    "Smartwatches": {
        "Apple Watch": 2000,
        "Samsung Galaxy Watch": 1800,
        "Fitbit": 1000,
        "Huawei Watch": 1200,
        "Amazfit": 900,
    },
    "Speakers": {
        "Bluetooth Speaker": 700,
        "Smart Speaker": 1200,
        "Home Theater Speaker": 3500,
        "Portable Mini Speaker": 600,
        "Soundbar": 2000,
    },
}

# ================= ANSI Colors =================
BLACK = '\u001b[30m'
RED = '\u001b[31m'
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
BLUE = '\u001b[34m'
MAGENTA = '\u001b[35m'
CYAN = '\u001b[36m'
WHITE = '\u001b[37m'
RESET = '\u001b[0m'

BOLD = '\u001b[1m'
UNDERLINE = '\u001b[4m'
REVERSE = '\u001b[7m'


def colour_print(text: str, effect: str) -> None:
    """Print text in ANSI color style"""
    print(f"{effect}{text}{RESET}")


def get_integers(prompt: str) -> int:
    """Keep asking until user inputs a number"""
    while True:
        temp = input(prompt)
        if temp.isnumeric():
            return int(temp)
        else:
            colour_print("Please enter a valid number!", RED)


# ================= Main Store Logic =================
def display_items():
    cart = []
    total_cost = 0

    while True:
        colour_print("\nAvailable Categories:", CYAN)
        for index, (category, store, base_price, items) in enumerate(available_parts):
            print(f"{index+1}. {category} (Base Price: {base_price}, Vendor: {store})")

        colour_print("\nEnter category number to explore, or 0 to checkout.", YELLOW)
        choice = get_integers("> ")

        if choice == 0:
            break

        if 1 <= choice <= len(available_parts):
            category, store, base_price, items = available_parts[choice - 1]

            colour_print(f"\nExplore {category} options:", MAGENTA)
            for i, (num, item) in enumerate(items):
                item_price = price_tags[category][item]
                print(f"{i+1}. {item} - ₦{item_price}")

            sub_choice = get_integers("Select item number (0 to go back): ")
            if sub_choice == 0:
                continue

            if 1 <= sub_choice <= len(items):
                selected_item = items[sub_choice - 1][1]
                item_price = price_tags[category][selected_item]

                if selected_item in [c[0] for c in cart]:
                    colour_print(f"Removing {selected_item} from cart.", RED)
                    cart = [c for c in cart if c[0] != selected_item]
                    total_cost -= item_price
                else:
                    colour_print(f"Adding {selected_item} to cart.", GREEN)
                    cart.append((selected_item, item_price))
                    total_cost += item_price

                colour_print(f"Current Cart: {cart}", CYAN)
                colour_print(f"Total: ₦{total_cost}\n", YELLOW)

    # Final checkout
    colour_print("\n==== Checkout Summary ====", BOLD)
    if cart:
        for item, price in cart:
            print(f"- {item}: ₦{price}")
        colour_print(f"\nTOTAL COST: ₦{total_cost}", GREEN)
    else:
        colour_print("Your cart is empty!", RED)


# ================= Run Program =================

colour_print("Welcome to BigUdom Tech Store!", GREEN)
display_items()
