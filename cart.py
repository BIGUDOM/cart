# cart.py
import os
import json
import smtplib
import traceback
from datetime import datetime
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tabulate import tabulate
from colorama import Fore, Style, init
import time
import sys
import random
import hashlib

init(autoreset=True)

# ===== CONFIG =====
CONFIG_FILE = "config.json"
ACCOUNTS_FOLDER = "accounts"
ORDERS_FOLDER = "orders"
os.makedirs(ACCOUNTS_FOLDER, exist_ok=True)
os.makedirs(ORDERS_FOLDER, exist_ok=True)

# ===== COLORS =====
CYAN = Fore.CYAN
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
MAGENTA = Fore.MAGENTA
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL
BLUE = Fore.BLUE

def section_footer(color):
    print(f"{color}{'─'*50} END {Style.RESET_ALL}\n")

    
def section_header(title, color):
    print(f"{color}{'─'*10} {title} {'─'*10}{RESET}")

def load_cart_from_disk(username):
    cart = []
    total = 0.0
    try:
        with open(f"{username}_cart.txt", "r") as f:
            for line in f:
                item, qty, price = line.strip().split(",", 2)
                cart.append((item, int(qty), float(price)))
                total += int(qty) * float(price)
    except FileNotFoundError:
        pass
    return cart, total
# ======== ITEMS ========

# ===== SHOP ITEMS =====
CATEGORIES = {
    "Electronics": {"Phone": 600, "Laptop": 500, "Headphones": 50, "Monitor": 200, "Tablet": 250, "Smartwatch": 120, "Camera": 300},
    "Clothing": {"T-Shirt": 20, "Jeans": 40, "Sneakers": 60, "Jacket": 80, "Cap": 15},
    "Groceries": {"Rice (5kg)": 30, "Oil (1L)": 10, "Milk (1L)": 5, "Bread": 3, "Eggs (Dozen)": 4," Chicken (1kg)": 8, "Vegetables (1kg)": 6," Fruits (1kg)": 7},
    "Books": {"Novel": 15, "Biography": 20, "Science": 25, "History": 18, "Comics": 12},
    "Toys": {"Action Figure": 25, "Puzzle": 15, "Board Game": 30, "Doll": 20, "RC Car": 40},
    "Home Appliances": {"Toaster": 35, "Microwave": 80, "Blender": 50, "Vacuum Cleaner": 100, "Air Fryer": 90}
}

# ======== HELPERS ========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading(text="Loading"):
    for i in range(3):
        sys.stdout.write(f"\r{text}{'.'*(i+1)}")
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write("\r" + " "*20 + "\r")

def pause():
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def print_banner():
    banner = r"""
██████╗ ██╗ ██████╗ ██╗   ██╗██████╗  ██████╗ ███╗   ███╗
██╔══██╗██║██╔═══██╗██║   ██║██╔══██╗██╔═══██╗████╗ ████║
██████╔╝██║██║   ██║██║   ██║██████╔╝██║   ██║██╔████╔██║
██╔═══╝ ██║██║   ██║██║   ██║██╔═══╝ ██║   ██║██║╚██╔╝██║
██║     ██║╚██████╔╝╚██████╔╝██║     ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝ ╚═╝     ╚═╝
    """
    color = random.choice([CYAN, GREEN, YELLOW, MAGENTA, RED])
    print(f"{color}{banner}{RESET}")

def load_config():
    # If config file doesn't exist, create template
    if not os.path.exists(CONFIG_FILE):
        template = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "codis1723@gmail.com",      # your email
            "sender_password": "hkdzlilwcqbbvmjo"    # your app password
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(template, f, indent=4)
        print(f"{YELLOW}⚠️ config.json created. Fill in your Gmail and app password!{RESET}")

    # Load config safely
    with open(CONFIG_FILE, "r") as f:
        try:
            cfg = json.load(f)
        except json.JSONDecodeError:
            cfg = {}

    # Make keys safe and provide defaults
    fixed_cfg = {
        "smtp_server": cfg.get("smtp_server") or cfg.get("SMTP_SERVER") or "smtp.gmail.com",
        "smtp_port": cfg.get("smtp_port") or cfg.get("SMTP_PORT") or 587,
        "sender_email": cfg.get("sender_email") or cfg.get("SENDER_EMAIL") or "codis1723@gmail.com",
        "sender_password": cfg.get("sender_password") or cfg.get("SENDER_PASSWORD") or "hkdzlilwcqbbvmjo"
    }

    if not fixed_cfg["sender_email"] or not fixed_cfg["sender_password"]:
        print(f"{RED}❌ sender_email or sender_password missing in config.json!{RESET}")

    return fixed_cfg


# ======== EMAIL ========
def send_email(recipient, subject, body, attachments=None):
    try:
        cfg = load_config()
        if not cfg["sender_email"] or not cfg["sender_password"]:
            print(f"{RED}Email not configured.{RESET}")
            return
        msg = MIMEMultipart()
        msg["From"] = cfg["sender_email"]
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        if attachments:
            for path in attachments:
                with open(path,"rb") as f:
                    part=MIMEApplication(f.read(), Name=os.path.basename(path))
                    part["Content-Disposition"]=f'attachment; filename="{os.path.basename(path)}"'
                    msg.attach(part)
        with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
            server.starttls()
            server.login(cfg["sender_email"], cfg["sender_password"])
            server.send_message(msg)
        print(f"{GREEN}Email sent to {recipient}{RESET}")
    except Exception as e:
        print(f"{RED}Email failed: {e}{RESET}")
        traceback.print_exc()

# ======== ACCOUNTS ========
def get_user_folder(username):
    return os.path.join(ACCOUNTS_FOLDER, username)

def get_account_file(username):
    return os.path.join(get_user_folder(username), "account.txt")

def get_cart_file(username):
    return os.path.join(get_user_folder(username), "cart.txt")

def save_cart(username, cart):
    os.makedirs(get_user_folder(username), exist_ok=True)
    with open(get_cart_file(username),"w") as f:
        for item, qty, price in cart:
            f.write("Cart Item:\n")
            f.write("=" * 40 + "\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write(f"Item: {item}\n")
            f.write(f"Quantity: {qty}\n")
            f.write(f"Price: {price}\n")
            f.write("=" * 40 + "\n")

def load_cart(username):
    clear_screen()
    print_banner() 
    cart=[]
    total=0
    fpath=get_cart_file(username)
    if os.path.exists(fpath):
        with open(fpath) as f:
            for line in f:
                item, qty, price=line.strip().split(",")
                qty=int(qty); price=float(price)
                cart.append((item, qty, price))
                total+=qty*price
    return cart, total

def get_user_email(username):
    acc=get_account_file(username)
    if not os.path.exists(acc): return None
    with open(acc) as f:
        for line in f:
            if line.lower().startswith("email:"):
                return line.split(":",1)[1].strip()
    return None

def register():
    clear_screen()
    print_banner()
    print(f"{BOLD}--- Register ---{RESET}")
    name = input("Name: ").strip()
    username = name[:6].lower()+str(random.randint(100, 999))
    print(f"Your username: {username}")
    if os.path.exists(get_user_folder(username)):
        print(f"{RED}Username exists!{RESET}")
        pause(); return None
    email = input("Email: ").strip()
    password = getpass("Password: ").strip()
    if len(password) < 7:
        print(f"{RED}Password too short!{RESET}")
        pause(); return password
    os.makedirs(get_user_folder(username), exist_ok=True)
    with open(get_account_file(username),"w") as f:
        f.write("# Account Info\n")
        f.write(f"# Keep this file safe!\n")
        f.write(f"# Username is auto-generated and cannot be changed.\n\n")
        f.write("=" * 40 + "\n")
        f.write(f"This account was created on {datetime.now().isoformat()}\n")
        f.write(f"Name: {name}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Email: {email}\n")
        # f.write(f"Password:{password}\n")
        f.write(f"Password: {hashlib.sha256(password.encode()).hexdigest()}\n")
        f.write("=" * 40 + "\n")
        f.write("# End of file\n")

    
    
    print(f"{GREEN}✅ Registered successfully!{RESET}")
    send_email(email, "Welcome to Bigudom Store", f"Hello {name},\nYour username is {username}.\n Do well to keep your password safe!")
    pause()
    return username, email

def forget_password(username, email):
    user_folder = get_user_folder(username)
    info_file = os.path.join(user_folder, "account.txt")
    if not os.path.exists(info_file):
        print(f"{RED}⚠️ No such account. Please create one.{RESET}")
        pause()
        return
    with open(info_file, "r") as f:
        lines = f.readlines()
    password_line = [line for line in lines if line.lower().startswith("password:")]
    if not password_line:
        print(f"{RED}⚠️ Password not found in account file.{RESET}")
        pause()
        return
    password_hash = password_line[0].split(":", 1)[1].strip()
    body = f"Hello {username},\nYour password hash is: {password_hash}\nPlease keep it safe."
    send_email(email, "Password Recovery", body)


def change_password(username):
    clear_screen()
    print_banner() 
    section_header("🔑 Change Password", BLUE)

    current_password = getpass("Current Password: ").strip()
    new_password = getpass("New Password: ").strip()
    confirm_password = getpass("Confirm New Password: ").strip()

    if new_password != confirm_password:
        print(f"{RED}⚠️ New passwords do not match.{RESET}")
        section_footer(BLUE)
        pause()
        return

    if len(new_password) < 7:
        print(f"{RED}⚠️ New password too short!{RESET}")
        section_footer(BLUE)
        pause()
        return

    acc_file = get_account_file(username)
    if not os.path.exists(acc_file):
        print(f"{RED}⚠️ No such account.{RESET}")
        section_footer(BLUE)
        pause()
        return

    lines = []
    with open(acc_file) as f:
        lines = f.readlines()

    stored_pass_line = [line for line in lines if line.lower().startswith("password:")]
    if not stored_pass_line:
        print(f"{RED}⚠️ Password not found in account file.{RESET}")
        section_footer(BLUE)
        pause()
        return

    stored_pass_hash = stored_pass_line[0].split(":", 1)[1].strip()
    if stored_pass_hash != hashlib.sha256(current_password.encode()).hexdigest():
        print(f"{RED}⚠️ Current password incorrect.{RESET}")
        section_footer(BLUE)
        pause()
        return

    with open(acc_file, "w") as f:
        for line in lines:
            if line.lower().startswith("password:"):
                f.write(f"Password: {hashlib.sha256(new_password.encode()).hexdigest()}\n")
            else:
                f.write(line)

    print(f"{GREEN}✅ Password changed successfully!{RESET}")
    section_footer(BLUE)
    pause()

# ======= LOGIN =======

def login_account():
    clear_screen()
    print_banner() 
    section_header("🔑 Login", BLUE)

    username = input("👤 Username: ").strip()
    password = getpass("🔑 Password: ").strip()

    user_folder = os.path.join(ACCOUNTS_FOLDER, username)
    info_file = os.path.join(user_folder, "account.txt")

    if not os.path.exists(info_file):
        print(f"{RED}⚠️ No such account. Please create one.{RESET}")
        section_footer(BLUE)
        pause()
        return None,None


    loading("Authenticating")

    if not os.path.exists(get_account_file(username)): print(f"{RED}No account found.{RESET}"); pause(); return None
    lines=[l.strip() for l in open(get_account_file(username))]
    email=[l for l in lines if l.lower().startswith("email:")][0].split(":",1)[1].strip()
    stored_pass=[l for l in lines if l.lower().startswith("password:")][0].split(":",1)[1].strip()
    if stored_pass==hashlib.sha256(password.encode()).hexdigest():
        print(f"{GREEN}✅ Login successful!{RESET}"); pause(); cart,total=load_cart(username); return username,email,cart,total
    else: 
        change_password(username)
        print(f"{RED}❌ Wrong password.{RESET}"); pause(); return None


# ======= DeLETE ACCOUNT =======
def delete_account(username):
    clear_screen()
    print_banner() 
    section_header("❌ Delete Account", RED)
    confirm = input(f"Type DELETE to confirm deleting account {username}: ").strip()
    if confirm != "DELETE":
        print(f"{YELLOW}⚠️ Deletion cancelled.{RESET}")
        section_footer(RED)
        pause()
        return
    user_folder = get_user_folder(username)
    if os.path.exists(user_folder):
        for root, dirs, files in os.walk(user_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(user_folder)
        print(f"{GREEN}✅ Account {username} deleted.{RESET}")
    else:
        print(f"{RED}⚠️ No such account.{RESET}")
    section_footer(RED)
    pause()


# ======== Change Email ========
def change_email(username):
    clear_screen()
    print_banner() 
    section_header("✉️ Change Email", MAGENTA)
    new_email = input("New Email: ").strip()
    if "@" not in new_email or "." not in new_email:
        print(f"{RED}⚠️ Invalid email format.{RESET}")
        section_footer(MAGENTA)
        pause()
        return
    acc_file = get_account_file(username)
    if not os.path.exists(acc_file):
        print(f"{RED}⚠️ No such account.{RESET}")
        section_footer(MAGENTA)
        pause()
        return
    lines = []
    with open(acc_file) as f:
        lines = f.readlines()
    with open(acc_file, "w") as f:
        for line in lines:
            if line.lower().startswith("email:"):
                f.write(f"Email: {new_email}\n")
            else:
                f.write(line)
    print(f"{GREEN}✅ Email updated to {new_email}.{RESET}")
    section_footer(MAGENTA)
    pause()


# ======= logout =======
def logout():
    clear_screen()
    print_banner() 
    section_header("🚪 Logout", YELLOW)
    current_user = None
    current_email = None
    cart = []
    total = 0.0
    if not current_user:
        print(f"{RED}⚠️ No user logged in.{RESET}")
        section_footer(YELLOW)
        pause()
        return None, None, [], 0.0
    else:
        print(f"{YELLOW}Logging out {current_user}...{RESET}")
        time.sleep(1)
        current_user = None
        current_email = None
        cart = []
        total = 0.0
        
    print(f"{GREEN}✅ Logged out successfully.{RESET}")
    pause()

# ======== SHOPPING ========
def shop_cart(username, cart, total):
    while True:
        clear_screen()
        print_banner() 
        print(f"{BOLD}{CYAN}--- Categories ---{RESET}")
        for i, cat in enumerate(CATEGORIES,1): print(f"{i}. {cat}")
        print("s. Search | 0. Back")
        choice=input("Choose: ").strip().lower()
        if choice=="0": return cart, total
        elif choice=="s":
            query=input("Search: ").strip().lower()
            results=[]
            for cat, items in CATEGORIES.items():
                for item, price in items.items():
                    if query in item.lower(): results.append((cat,item,price))
            if not results: print(f"{RED}No match.{RESET}"); pause(); continue
            table=[(i+1,c,it,f"${pr}") for i,(c,it,pr) in enumerate(results)]
            print(tabulate(table, headers=["#","Category","Item","Price"], tablefmt="fancy_grid"))
            sel=input("Select #: ").strip()
            if sel.isdigit() and 1<=int(sel)<=len(results):
                _, item, price=results[int(sel)-1]
                qty=int(input("Qty: "))
                cart.append((item, qty, price)); total+=qty*price
                print(f"{GREEN}{item} x{qty} added.{RESET}"); pause()
        elif choice.isdigit() and 1<=int(choice)<=len(CATEGORIES):
            cat=list(CATEGORIES.keys())[int(choice)-1]
            items=list(CATEGORIES[cat].items())
            for i,(it,pr) in enumerate(items,1): print(f"{i}. {it} ${pr}")
            sel=input("Select #: ").strip()
            if sel.isdigit() and 1<=int(sel)<=len(items):
                item, price=items[int(sel)-1]; qty=int(input("Qty: "))
                cart.append((item, qty, price)); total+=qty*price
                print(f"{GREEN}{item} x{qty} added.{RESET}"); pause()
        save_cart(username, cart)

def get_ads():
    ads = [
        ("Big Sale!", "Get 20% off on all electronics this weekend!"),
        ("New Arrivals", "Check out the latest fashion trends in our clothing section."),
        ("Fresh Groceries", "Order fresh groceries and get them delivered to your doorstep."),
        ("Book Lovers", "Buy 2 get 1 free on all books this month!"),
        ("Toy Wonderland", "Up to 30% off on selected toys for kids."),
        ("Home Essentials", "Upgrade your home with our latest appliances at discounted prices."),
        ("Fitness Fanatics", "Get fit with our exclusive range of sports equipment."),
        ("Gadget Galore", "Latest gadgets available now. Limited stock!"),
        ("Back to School", "Special discounts on school supplies and backpacks."),
        ("Holiday Specials", "Exclusive holiday deals on all items in store."),
    ]
    return random.choice(ads)

# ======== ADMIN: SEND ADS ========
def send_ads():
    clear_screen()
    print_banner() 
    section_header("📢 Send Promotional Ads", CYAN)
    cfg = load_config()
    if not cfg["sender_email"] or not cfg["sender_password"]:
        print(f"{RED}Email not configured.{RESET}")
        section_footer(CYAN)
        pause()
        return
    subject, body = get_ads()
    body += "\nVisit our store for more exciting offers!"
    count = 0
    for user in os.listdir(ACCOUNTS_FOLDER):
        email = get_user_email(user)
        if email:
            send_email(email, random.choice(subject), body)
            count += 1
            time.sleep(1)  # To avoid spamming
    print(f"{GREEN}✅ Sent ads to {count} users.{RESET}")
    section_footer(CYAN)
    pause()

# ======== RECEIPTS ========
def save_receipt_txt(username, cart, total):
    folder=os.path.join(ORDERS_FOLDER, username); os.makedirs(folder, exist_ok=True)
    fname=f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    fpath=os.path.join(folder,fname)
    with open(fpath,"w") as f:
        f.write(f"Bigudom Store Receipt\nUser: {username}\nDate: {datetime.now()}\n\n")
        f.write("=" * 30 + "\n")
        for item, qty, price in cart: f.write(f"{item} x{qty} = ${price*qty}\n")
        f.write(f"\nTOTAL: ${total}\n")
        f.write("=" * 30 + "\n")
        f.write("Thank you for shopping with us!\n" + GREEN)
    return fpath

def save_receipt_pdf(username, cart, total):
    folder=os.path.join(ORDERS_FOLDER, username); os.makedirs(folder, exist_ok=True)
    fname=f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    fpath=os.path.join(folder,fname)
    c=canvas.Canvas(fpath, pagesize=letter)
    width,height=letter
    c.setFont("Helvetica-Bold",16); c.drawString(200,height-50,"Bigudom Store Receipt")
    c.setFont("Helvetica",12); c.drawString(50,height-80,f"User: {username}")
    c.drawString(50,height-100,f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y=height-140
    for item, qty, price in cart: c.drawString(50,y,f"{item} x{qty} = ${price*qty}"); y-=20
    c.setFont("Helvetica-Bold",14); c.drawString(50,y-20,f"TOTAL: ${total}"); c.save()
    return fpath

# ======== CHECKOUT ========
def checkout(username, email, cart, total):
    clear_screen()
    print_banner() 
    if not cart: print(f"{RED}Cart empty.{RESET}"); pause(); return
    clear_screen(); print(f"{BOLD}{MAGENTA}--- Checkout ---{RESET}")
    table=[(i+1,it,qty,f"${pr*qty}") for i,(it,qty,pr) in enumerate(cart)]
    print(tabulate(table, headers=["#","Item","Qty","Subtotal"], tablefmt="fancy_grid"))
    print(f"{YELLOW}TOTAL: ${total}{RESET}")
    if input("Confirm? (y/n): ").strip().lower()!="y": print(f"{YELLOW}Cancelled.{RESET}"); pause(); return
    loading("Processing")
    txt=save_receipt_txt(username, cart, total)
    pdf=save_receipt_pdf(username, cart, total)
    if email:
        body=f"Hello {username},\nThank you for shopping!\nTotal: ${total}\nSee attached receipt."
        send_email(email, "Bigudom Store Receipt", body,[txt,pdf])
    print(f"{GREEN}Checkout complete! Receipts saved.{RESET}")
    save_cart(username, [])
    pause()

# ======== MAIN MENU ========

def colored_option(number, text, emoji):
    color = random.choice([CYAN, GREEN, YELLOW, MAGENTA, RED])
    return f"{color}{BOLD}{number}. {text} {emoji}{RESET}"

def main():
    current_user=None; current_email=None; cart=[]; total=0
    while True:
        loading("Refreshing Store")
        clear_screen()
        print_banner() # multi-colored menu
        print(colored_option("1", "Create Account", "🆕"))
        print(colored_option("2", "Login", "🔑"))
        print(colored_option("3", "Shop", "🛒"))
        print(colored_option("4", "View Cart", "📜"))
        print(colored_option("5", "Checkout", "💳"))
        print(colored_option("6", "Purchase History", "📖"))
        print(colored_option("7", "Forget Password", "❓"))
        print(colored_option("8", "Test Email (send to logged in user)", "✉️"))
        print(colored_option("9", "Delete Account", "🗑️"))
        print(colored_option("10", "Change Email", "✉️"))
        print(colored_option("0", "Exit", "🚪"))
        footer_color = random.choice([CYAN, GREEN, YELLOW, MAGENTA, RED])
        print(f"\n{footer_color}© 2025 Bigudom Store. All rights reserved.{RESET}")

        choice = input("Choose: ").strip()
        if choice == "0":
            print(f"{GREEN}Bye!{RESET}")
            break
        elif choice == "1":
            res = register()
            send_ads()  # Send ads after registration
            if res:
                current_user, current_email = res
                cart, total = load_cart(current_user)
        elif choice == "2":
            res = login_account()
            send_ads()  # Send ads after login
            if res and isinstance(res, tuple) and len(res) == 4:
                current_user, current_email, cart, total = res
            else:
                # login failed: nothing changes
                current_user, current_email, cart, total = None, None, [], 0.0
        elif choice == "3":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                cart, total = shop_cart(current_user, cart, total)
        elif choice == "4":
            if not cart:
                print(f"{RED}Cart empty.{RESET}")
                pause()
            else:
                table = [(i+1, it, qty, f"${pr*qty}") for i, (it, qty, pr) in enumerate(cart)]
                print(tabulate(table, headers=["#","Item","Qty","Subtotal"], tablefmt="fancy_grid"))
                print(f"{YELLOW}TOTAL: ${total}{RESET}")
                pause()
        elif choice == "5":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                checkout(current_user, current_email, cart, total)
                cart = []
                total = 0
                save_cart(current_user, cart)
        elif choice == "6":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                folder = os.path.join(ORDERS_FOLDER, current_user)
                if not os.path.exists(folder):
                    print(f"{YELLOW}No purchase history.{RESET}")
                    pause()
                else:
                    files = os.listdir(folder)
                    files = [f for f in files if f.endswith(".txt")]
                    files.sort()
                    if not files:
                        print(f"{YELLOW}No purchase history.{RESET}")
                        pause()
                    else:
                        print(f"{BOLD}{CYAN}--- Purchase History ---{RESET}")
                        for f in files:
                            print(f"- {f}")
                        pause()
        elif choice == "7":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                email = get_user_email(current_user)
                if not email:
                    print(f"{RED}No email on file.{RESET}")
                    pause()
                else:
                    body = f"Hello {current_user},\nYour password is in your account.txt file. Please keep it safe."
                    send_email(email, "Password Recovery", body)
                    change_password(current_user)
                    pause()
        elif choice == "9":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                delete_account(current_user)
        elif choice == "8":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                email = get_user_email(current_user)
                if not email:
                    print(f"{RED}No email on file.{RESET}")
                    pause()
                else:
                    body = f"Hello {current_user},\nThis is a test email from Bigudom Store."
                    send_email(email, "Test Email from Bigudom Store", body)
                    send_ads()  # Send ads to logged in users
                    section_footer(CYAN)
                    pause()
        elif choice == "10":
            if not current_user:
                print(f"{RED}Login first.{RESET}")
                pause()
            else:
                change_email(current_user)
        else:
            print(f"{RED}Login First.{RESET}")
            pause()

if __name__=="__main__": main()