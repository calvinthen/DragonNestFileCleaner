import tkinter as tk 
from tkinter import messagebox, filedialog
import os
from send2trash import send2trash
import json  # <--- NEW: Tool to save data

class DragonCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dragon Nest File Cleaner")
        self.root.geometry("600x550") 
        
        # Default settings (used if no save file is found)
        self.default_path = r"C:\DragonNest\Reborn"
        self.path_var = tk.StringVar(value=self.default_path)
        self.files_to_delete = set() 
        self.config_file = "cleaner_settings.json" # Name of the save file

        # 1. Try to load saved settings BEFORE building the GUI
        self.load_settings()

        # 2. Build the GUI
        self.create_gui()

    def create_gui(self):
        # Section A: Target Folder
        path_frame = tk.LabelFrame(self.root, text="1. Target Folder", padx=10, pady=10)
        path_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(path_frame, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(path_frame, text="Browse...", command=self.browse_folder).pack(side="right")

        # Section B: File Manager
        file_frame = tk.LabelFrame(self.root, text="2. Files to Delete", padx=10, pady=10)
        file_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Input Area
        input_frame = tk.Frame(file_frame)
        input_frame.pack(fill="x", pady=5)
        
        tk.Label(input_frame, text="File Name:").pack(side="left")
        
        self.new_file_var = tk.StringVar()
        self.file_entry = tk.Entry(input_frame, textvariable=self.new_file_var)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.file_entry.bind('<Return>', lambda event: self.add_file()) 

        add_btn = tk.Button(input_frame, text="Add to List", command=self.add_file, bg="#e1ffe1")
        add_btn.pack(side="left")

        # List Area
        self.listbox = tk.Listbox(file_frame, height=8)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        remove_btn = tk.Button(file_frame, text="Remove Selected", command=self.remove_file, bg="#ffe1e1")
        remove_btn.pack(anchor="e")

        # Populate listbox (in case we loaded data from the save file)
        self.refresh_listbox()

        # Section C: Execution Button
        action_frame = tk.Frame(self.root, pady=20)
        action_frame.pack(fill="x")

        delete_btn = tk.Button(action_frame, text="EXECUTE CLEANUP", 
                               command=self.perform_cleanup, 
                               bg="#ffcccc", fg="red", font=("Arial", 11, "bold"), height=2)
        delete_btn.pack(fill="x", padx=20)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side="bottom", fill="x")

    # --- NEW: SAVE & LOAD FUNCTIONS ---
    def save_settings(self):
        """Saves current path and file list to a JSON file."""
        data = {
            "path": self.path_var.get(),
            "files": list(self.files_to_delete) # Convert set to list for JSON
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        """Loads path and file list from JSON file if it exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    # Restore Path
                    if "path" in data:
                        self.path_var.set(data["path"])
                    # Restore Files
                    if "files" in data:
                        self.files_to_delete = set(data["files"])
            except Exception as e:
                print(f"Error loading settings: {e}")

    # --- UPDATED LOGIC FUNCTIONS (Now they trigger Save) ---

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
            self.save_settings() # <--- Save immediately

    def add_file(self):
        filename = self.new_file_var.get().strip()
        if filename:
            self.files_to_delete.add(filename)
            self.refresh_listbox()
            self.new_file_var.set("")
            self.save_settings() # <--- Save immediately
        else:
            messagebox.showwarning("Warning", "Please type a file name first.")

    def remove_file(self):
        selection = self.listbox.curselection()
        if selection:
            file_to_remove = self.listbox.get(selection[0])
            self.files_to_delete.remove(file_to_remove)
            self.refresh_listbox()
            self.save_settings() # <--- Save immediately

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for filename in sorted(self.files_to_delete):
            self.listbox.insert(tk.END, filename)

    def perform_cleanup(self):
        target_dir = self.path_var.get()
        
        if not os.path.exists(target_dir):
            messagebox.showerror("Error", f"Folder not found:\n{target_dir}")
            return

        if not self.files_to_delete:
            messagebox.showwarning("Warning", "The list is empty!")
            return

        confirm = messagebox.askyesno("Confirm", f"Delete {len(self.files_to_delete)} files?")
        if not confirm:
            return

        deleted_count = 0
        skipped_count = 0

        for filename in self.files_to_delete:
            full_path = os.path.join(target_dir, filename)

            if os.path.exists(full_path):
                try:
                    send2trash(full_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error: {e}")
            else:
                skipped_count += 1

        self.status_var.set(f"Done. Deleted: {deleted_count} | Skipped: {skipped_count}")
        messagebox.showinfo("Report", f"Deleted: {deleted_count}\nSkipped: {skipped_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DragonCleanerApp(root)
    root.mainloop()