import tkinter as tk
from tkinter import filedialog, ttk
from cartd_generator import CardGenerator  # your existing file
import os

# -----------------------------------------
# GUI Window
# -----------------------------------------
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
        self.hp_var = tk.StringVar(value="10")
        tk.Entry(root, textvariable=self.hp_var, width=10).grid(row=2, column=1, sticky="w")

        # -----------------------------
        # ATK
        # -----------------------------
        tk.Label(root, text="ATK:").grid(row=3, column=0, sticky="w")
        self.atk_var = tk.StringVar(value="5")
        tk.Entry(root, textvariable=self.atk_var, width=10).grid(row=3, column=1, sticky="w")

        # -----------------------------
        # ROLE DROPDOWN
        # -----------------------------
        tk.Label(root, text="Role:").grid(row=4, column=0, sticky="w")
        self.role_var = tk.StringVar(value="tank")
        ttk.Combobox(
            root,
            textvariable=self.role_var,
            values=["tank", "melee", "ranged", "support", "healer"],
            width=15
        ).grid(row=4, column=1, sticky="w")

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
