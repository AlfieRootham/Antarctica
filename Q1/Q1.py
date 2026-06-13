import customtkinter as ctk

#print(ctk.__version__)

def execute_search():
    return

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

# Search button
search_button = ctk.CTkButton(
    search_frame,
    text="🔍",
    width=55,
    height=45,
    corner_radius=22,
    fg_color="white",
    text_color="black",
    hover_color="#e5e5e5",
    command=execute_search
)
search_button.grid(row=0, column=1)

app.mainloop()