import tkinter as tk 
from tkinter import messagebox, filedialog
import os
from send2trash import send2trash

class DragonCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dragon Nest File Cleaner")
        self.root.geometry("600x550") 
        
        self.default_path = r"C:\DragonNest\Reborn"
        self.path_var = tk.StringVar(value=self.default_path)

        self.files_to_delete = set() 

        self.create_gui()


