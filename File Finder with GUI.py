import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

class FileFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Finder")
        self.root.geometry("500x300")
        
        # Label for instructions
        self.label = tk.Label(root, text="Enter file or directory name to search:", font=("Arial", 12))
        self.label.pack(pady=10)
        
        # Entry field for the file or directory name
        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack(pady=5)
        
        # Button to browse the directory
        self.browse_button = tk.Button(root, text="Browse Starting Directory", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        # Label to display the selected directory
        self.directory_label = tk.Label(root, text="No directory selected", fg="gray", font=("Arial", 10))
        self.directory_label.pack(pady=5)
        
        # Button to start the search
        self.search_button = tk.Button(root, text="Search", command=self.start_search)
        self.search_button.pack(pady=10)
        
        # Text area to display search results
        self.result_area = tk.Text(root, height=6, width=60, state="disabled")
        self.result_area.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
        self.progress.pack(pady=5)
        
        self.searching = False
        self.directory_path = ""
    
    # Function to browse and select the directory to start search
    def browse_directory(self):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.directory_label.config(text=f"Directory: {self.directory_path}", fg="black")
    
    # Function to start the search process
    def start_search(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a file or directory name to search.")
            return
        if not self.directory_path:
            messagebox.showwarning("Directory Error", "Please select a starting directory.")
            return
        
        self.result_area.config(state="normal")
        self.result_area.delete("1.0", tk.END)
        self.result_area.insert(tk.END, "Searching...\n")
        self.result_area.config(state="disabled")
        
        # Start search in a separate thread to keep the UI responsive
        search_thread = Thread(target=self.search, args=(search_term,))
        search_thread.start()
    
    # Function to search for the file or directory in the specified path
    def search(self, search_term):
        self.search_button.config(state="disabled")
        self.progress.start()
        found_paths = []
        
        # Walk through directory and subdirectories
        for root, dirs, files in os.walk(self.directory_path):
            if search_term in dirs or search_term in files:
                found_paths.append(os.path.join(root, search_term))
            
            if not self.searching:
                break
        
        # Update results in the text area
        self.progress.stop()
        self.search_button.config(state="normal")
        
        self.result_area.config(state="normal")
        self.result_area.delete("1.0", tk.END)
        
        if found_paths:
            self.result_area.insert(tk.END, f"Found {len(found_paths)} matches:\n")
            for path in found_paths:
                self.result_area.insert(tk.END, path + "\n")
        else:
            self.result_area.insert(tk.END, "No matches found.")
        
        self.result_area.config(state="disabled")

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = FileFinderApp(root)
    root.mainloop()


#Libraries Used:

#os: To traverse the file system and find directories/files.
#tkinter: To create the graphical user interface.
#threading: To run the search operation on a separate thread, allowing the UI to remain responsive.
#ttk: Provides the progress bar for a modern look.
