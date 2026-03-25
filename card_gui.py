import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import random

# ---------------------------------------------------------
# STAT RANGES FOR EACH ROLE
# ---------------------------------------------------------
ROLE_STATS = {
    "tank":    {"hp": (12, 20), "atk": (3, 6)},
    "melee":   {"hp": (10, 14), "atk": (6, 10)},
    "ranged":  {"hp": (8, 12),  "atk": (7, 11)},
    "support": {"hp": (8, 12),  "atk": (1, 4)},
    "healer":  {"hp": (10, 14), "atk": (1, 3)},
}

# ---------------------------------------------------------
# Scale AND crop image to fully cover a frame (no borders)
# ---------------------------------------------------------
def scale_and_crop(img, frame_width, frame_height):
    img_ratio = img.width / img.height
    frame_ratio = frame_width / frame_height

    # Scale up until image fully covers the frame
    if img_ratio > frame_ratio:
        new_height = frame_height
        new_width = int(frame_height * img_ratio)
    else:
        new_width = frame_width
        new_height = int(frame_width / img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Center crop
    left = (new_width - frame_width) // 2
    top = (new_height - frame_height) // 2
    right = left + frame_width
    bottom = top + frame_height

    return img.crop((left, top, right, bottom))


# ---------------------------------------------------------
# Card Generator
# ---------------------------------------------------------
class CardGenerator:
    def __init__(self, sleeves_folder, font_path="arial.ttf"):
        self.sleeves_folder = sleeves_folder

        # Fonts
        self.font_title = ImageFont.truetype(font_path, 40)
        self.font_stats = ImageFont.truetype(font_path, 32)
        self.font_desc = ImageFont.truetype(font_path, 26)

        # Layout (your exact coordinates)
        self.ART_X = 17
        self.ART_Y = 85
        self.ART_W = 715
        self.ART_H = 644

        self.NAME_X = 126
        self.NAME_Y = 19

        self.HEALTH_X = 37
        self.HEALTH_Y = 747

        self.ATTACK_X = 346
        self.ATTACK_Y = 747

        self.DESC_X = 51
        self.DESC_Y = 814

    def wrap_text(self, text, width):
        return textwrap.fill(text, width=width)

    def load_sleeve(self, role):
        role = role.lower()
        filename = f"{role}_sleeve.png"
        full_path = os.path.join(self.sleeves_folder, filename)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Sleeve not found: {full_path}")

        return Image.open(full_path).convert("RGBA")

    def create_card(self, art_path, name, health, attack, role, description, output_path):
        # Load sleeve based on role
        card = self.load_sleeve(role)

        draw = ImageDraw.Draw(card)

        # -----------------------------
        # ART (scale + crop to frame)
        # -----------------------------
        art = Image.open(art_path).convert("RGBA")
        art = scale_and_crop(art, self.ART_W, self.ART_H)
        card.paste(art, (self.ART_X, self.ART_Y), art)

        # -----------------------------
        # NAME
        # -----------------------------
        draw.text((self.NAME_X, self.NAME_Y), name, font=self.font_title, fill="black")

        # -----------------------------
        # HEALTH
        # -----------------------------
        draw.text((self.HEALTH_X, self.HEALTH_Y), f"HP: {health}", font=self.font_stats, fill="black")

        # -----------------------------
        # ATTACK
        # -----------------------------
        draw.text((self.ATTACK_X, self.ATTACK_Y), f"ATK: {attack}", font=self.font_stats, fill="black")

        # -----------------------------
        # DESCRIPTION
        # -----------------------------
        wrapped = self.wrap_text(description, width=60)
        draw.text((self.DESC_X, self.DESC_Y), wrapped, font=self.font_desc, fill="black")

        # -----------------------------
        # SAVE
        # -----------------------------
        card.save(output_path)
        print(f"Card saved to {output_path}")


# ---------------------------------------------------------
# GUI
# ---------------------------------------------------------
class CardGUI:
    def __init__(self, root):
        self.root = root
        root.title("Card Generator")

        # Card generator instance
        self.gen = CardGenerator(
            sleeves_folder=r"C:\Users\Redux\Desktop\cartd_generator\sleeves"
        )

        # -----------------------------
        # ART PICKER
        # -----------------------------
        tk.Label(root, text="Art File:").grid(row=0, column=0, sticky="w")
        self.art_path_var = tk.StringVar()
        tk.Entry(root, textvariable=self.art_path_var, width=40).grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.pick_art).grid(row=0, column=2)

        # -----------------------------
        # NAME
        # -----------------------------
        tk.Label(root, text="Name:").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(root, textvariable=self.name_var, width=40).grid(row=1, column=1)

        # -----------------------------
        # HP
        # -----------------------------
        tk.Label(root, text="HP:").grid(row=2, column=0, sticky="w")
        self.hp_var = tk.StringVar()
        tk.Entry(root, textvariable=self.hp_var, width=10).grid(row=2, column=1, sticky="w")

        # -----------------------------
        # ATK
        # -----------------------------
        tk.Label(root, text="ATK:").grid(row=3, column=0, sticky="w")
        self.atk_var = tk.StringVar()
        tk.Entry(root, textvariable=self.atk_var, width=10).grid(row=3, column=1, sticky="w")

        # -----------------------------
        # ROLE DROPDOWN
        # -----------------------------
        tk.Label(root, text="Role:").grid(row=4, column=0, sticky="w")
        self.role_var = tk.StringVar(value="tank")

        role_box = ttk.Combobox(
            root,
            textvariable=self.role_var,
            values=["tank", "melee", "ranged", "support", "healer"],
            width=15
        )
        role_box.grid(row=4, column=1, sticky="w")

        # Auto-roll stats when role changes
        role_box.bind("<<ComboboxSelected>>", lambda e: self.roll_stats_for_role(self.role_var.get()))

        # -----------------------------
        # DESCRIPTION
        # -----------------------------
        tk.Label(root, text="Description:").grid(row=5, column=0, sticky="nw")
        self.desc_box = tk.Text(root, width=40, height=5)
        self.desc_box.grid(row=5, column=1)

        # -----------------------------
        # GENERATE BUTTON
        # -----------------------------
        tk.Button(root, text="Generate Card", command=self.generate).grid(row=6, column=1, pady=10)

        # -----------------------------
        # STATUS
        # -----------------------------
        self.status_var = tk.StringVar()
        tk.Label(root, textvariable=self.status_var, fg="green").grid(row=7, column=1)

    # -----------------------------------------
    # Pick art file
    # -----------------------------------------
    def pick_art(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")]
        )
        if path:
            self.art_path_var.set(path)

    # -----------------------------------------
    # Auto-roll stats based on role
    # -----------------------------------------
    def roll_stats_for_role(self, role):
        stats = ROLE_STATS[role]
        hp_min, hp_max = stats["hp"]
        atk_min, atk_max = stats["atk"]

        rolled_hp = random.randint(hp_min, hp_max)
        rolled_atk = random.randint(atk_min, atk_max)

        self.hp_var.set(str(rolled_hp))
        self.atk_var.set(str(rolled_atk))

    # -----------------------------------------
    # Generate card
    # -----------------------------------------
    def generate(self):
        art = self.art_path_var.get()
        name = self.name_var.get()
        hp = int(self.hp_var.get())
        atk = int(self.atk_var.get())
        role = self.role_var.get()
        desc = self.desc_box.get("1.0", tk.END).strip()

        output_path = os.path.join(
            r"C:\Users\Redux\Desktop\cartd_generator",
            f"{name}_card.png"
        )

        try:
            self.gen.create_card(
                art_path=art,
                name=name,
                health=hp,
                attack=atk,
                role=role,
                description=desc,
                output_path=output_path
            )
            self.status_var.set(f"Saved: {output_path}")
        except Exception as e:
            self.status_var.set(f"Error: {e}")


# -----------------------------------------
# Run GUI
# -----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    gui = CardGUI(root)
    root.mainloop()
