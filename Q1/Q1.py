import customtkinter as ctk
from tkinter import filedialog

#print(ctk.__version__)

def execute_search():
    return

def browse_file_location():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Choose where to save the Excel file"
    )

    if file_path:
        file_location_entry.delete(0, "end")
        file_location_entry.insert(0, file_path)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("GitHub Repository Exporter")
app.geometry("800x500")
app.configure(fg_color="black")

# Title
title_label = ctk.CTkLabel(
    app,
    text="GitHub User Search Engine",
    font=("Arial", 32, "bold"),
    text_color="white"
)
title_label.pack(pady=(60, 0))

# Main centered container
search_frame = ctk.CTkFrame(app, fg_color="black")
search_frame.place(relx=0.5, rely=0.5, anchor="center")

# Search bar
search_entry = ctk.CTkEntry(
    search_frame,
    width=420,
    height=45,
    corner_radius=22,
    fg_color="white",
    text_color="black",
    placeholder_text="Search GitHub username...",
    placeholder_text_color="gray"
)
search_entry.grid(row=0, column=0, padx=(0, 10))

file_location_entry = ctk.CTkEntry(
    search_frame,
    width=420,
    height=45,
    corner_radius=22,
    fg_color="white",
    text_color="black",
    placeholder_text="Where would you like this saved?"
)
file_location_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 25))

browse_button = ctk.CTkButton(
    search_frame,
    text="📁",
    width=50,
    height=20,
    corner_radius=0,
    fg_color="white",
    text_color="black",
    hover_color="#e5e5e5",
    command=browse_file_location
)
browse_button.grid(row=1, column=1, pady=(0, 25))


# Search button
search_button = ctk.CTkButton(
    search_frame,
    text="Create Excel File",
    width=55,
    height=45,
    corner_radius=22,
    fg_color="white",
    text_color="black",
    hover_color="#e5e5e5",
    command=execute_search
)
search_button.grid(row=2, column=0)

app.mainloop()