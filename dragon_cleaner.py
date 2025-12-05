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

    def create_gui(self):
        # Section A: Target Folder
        path_frame = tk.LabelFrame(self.root, text="1. Target Folder", padx=10, pady=10)
        path_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(path_frame, textvariable=self.path_var).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(path_frame, text="Browse...", command=self.browse_folder).pack(side="right")

        # Section B: File Manager
        file_frame = tk.LabelFrame(self.root, text="2. Files to Delete", padx=10, pady=10)
        file_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Input Area (Where you type the file name)
        input_frame = tk.Frame(file_frame)
        input_frame.pack(fill="x", pady=5)
        
        tk.Label(input_frame, text="File Name:").pack(side="left")
        
        self.new_file_var = tk.StringVar()
        self.file_entry = tk.Entry(input_frame, textvariable=self.new_file_var)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=5)
        # Allow pressing 'Enter' key to add file
        self.file_entry.bind('<Return>', lambda event: self.add_file()) 

        add_btn = tk.Button(input_frame, text="Add to List", command=self.add_file, bg="#e1ffe1")
        add_btn.pack(side="left")

        # List Area (The white box showing added files)
        self.listbox = tk.Listbox(file_frame, height=8)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        remove_btn = tk.Button(file_frame, text="Remove Selected", command=self.remove_file, bg="#ffe1e1")
        remove_btn.pack(anchor="e")

        # Section C: Execution Button
        action_frame = tk.Frame(self.root, pady=20)
        action_frame.pack(fill="x")

        delete_btn = tk.Button(action_frame, text="EXECUTE CLEANUP", 
                               command=self.perform_cleanup, 
                               bg="#ffcccc", fg="red", font=("Arial", 11, "bold"), height=2)
        delete_btn.pack(fill="x", padx=20)

        # Status Bar (Text at the bottom)
        self.status_var = tk.StringVar(value="Ready.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side="bottom", fill="x")

    # --- FIX WAS HERE: 'def browse_folder' needed to move left ---
    def browse_folder(self):
        # Opens Windows folder selector
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def add_file(self):
        # Takes text from box -> Adds to list
        filename = self.new_file_var.get().strip()
        if filename:
            self.files_to_delete.add(filename)
            self.refresh_listbox()
            self.new_file_var.set("") # Clear the box
        else:
            messagebox.showwarning("Warning", "Please type a file name first.")

    def remove_file(self):
        # Deletes selected item from list
        selection = self.listbox.curselection()
        if selection:
            file_to_remove = self.listbox.get(selection[0])
            self.files_to_delete.remove(file_to_remove)
            self.refresh_listbox()

    def refresh_listbox(self):
        # Updates the screen to match our data
        self.listbox.delete(0, tk.END)
        for filename in sorted(self.files_to_delete):
            self.listbox.insert(tk.END, filename)

    def perform_cleanup(self):
        target_dir = self.path_var.get()
        
        # Safety Check 1: Does folder exist?
        if not os.path.exists(target_dir):
            messagebox.showerror("Error", f"Folder not found:\n{target_dir}")
            return

        # Safety Check 2: Is list empty?
        if not self.files_to_delete:
            messagebox.showwarning("Warning", "The list is empty!")
            return

        # Safety Check 3: Ask User
        confirm = messagebox.askyesno("Confirm", f"Delete {len(self.files_to_delete)} files?")
        if not confirm:
            return

        deleted_count = 0
        skipped_count = 0

        # Loop through every file in our list
        for filename in self.files_to_delete:
            full_path = os.path.join(target_dir, filename)

            if os.path.exists(full_path):
                try:
                    send2trash(full_path) # <--- The actual delete command
                    deleted_count += 1
                except Exception as e:
                    print(f"Error: {e}")
            else:
                skipped_count += 1

        self.status_var.set(f"Done. Deleted: {deleted_count} | Skipped: {skipped_count}")
        messagebox.showinfo("Report", f"Deleted: {deleted_count}\nSkipped: {skipped_count}")

# ---------------------------------------------------------
# START THE APP
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DragonCleanerApp(root)
    root.mainloop()