import customtkinter as ctk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import webbrowser
from google import genai
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
from chatbot import gemini


#print(ctk.__version__)
#load the path to the . env fils so that the api key can be found
env_path = Path(__file__).resolve().parent.parent / ".env"

#print("Current working directory:", Path.cwd())
#print("Env path:", env_path)
#print("Env exists:", env_path.exists())
#print("raw values:", dotenv_values(env_path))



load_dotenv(env_path)
api = os.getenv("GEMINI_API_KEY")
#print(api)
'''
client = genai.Client(api_key=api)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)
'''

'''
Button functions 
'''
def execute_search():
    global last_created_file

    user = search_entry.get()
    file_path = file_location_entry.get()

    if not user or not file_path:
        return

    user_repositories = scrape_github(user)
    get_excel(user_repositories, file_path)

    #create link under the search button 
    last_created_file = file_path

    file_link_label.configure(
        text=f"Open created file: {os.path.basename(file_path)}",
        text_color="#4da6ff",
        cursor="hand2"
    )


#file search to add this to an existing excel file
def browse_file_location():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Choose where to save the Excel file"
    )

    if file_path:
        file_location_entry.delete(0, "end")
        file_location_entry.insert(0, file_path)

#create in page link to file
last_created_file = None

def open_created_file(event=None):
    if last_created_file and os.path.exists(last_created_file):
        webbrowser.open(last_created_file)

def send_message():
    user_message = chat_input.get()

    if not user_message.strip():
        return

    chat_display.insert("end", f"You: {user_message}\n")
    chat_input.delete(0, "end")

    bot_reply = gemini(user_message)

    chat_display.insert("end", f"Gemini: {bot_reply}\n\n")
'''
Create GUI
'''
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("GitHub Repository Exporter")
app.geometry("800x500")
app.configure(fg_color="black")

#two frames so that the chatbot an dsearch both appear on the screen
main_container = ctk.CTkFrame(app)
main_container.pack(fill="both", expand=True, padx=20, pady=20)

left_frame = ctk.CTkFrame(main_container)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 17.5))

chat_frame = ctk.CTkFrame(main_container, width=300)
chat_frame.pack(side="right", fill="y", padx=(10, 0))
chat_frame.pack_propagate(False)


# Title
title_label = ctk.CTkLabel(
    left_frame,
    text="GitHub User Search Engine",
    font=("Calibri", 32, "bold"),
    text_color="white"
)
title_label.pack(pady=(60, 0))

# Main centered container
search_frame = ctk.CTkFrame(left_frame, fg_color="#383838")
search_frame.place(relx=0.5, rely=0.5, anchor="center")

# Search bar
search_entry = ctk.CTkEntry(
    search_frame,
    width=350,
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
    width=350,
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


file_link_label = ctk.CTkLabel(
    search_frame,
    text="",
    font=("Segoe UI", 13, "underline"),
    text_color="#4da6ff"
)
file_link_label.grid(row=3, column=0, columnspan=2, pady=(15, 0))

file_link_label.bind("<Button-1>", open_created_file)

#chat bot
chat_display = ctk.CTkTextbox(chat_frame, width=500, height=300)
chat_display.pack(pady=10)

chat_input = ctk.CTkEntry(chat_frame, width=400, placeholder_text="Ask the chatbot...")
chat_input.pack(pady=5)

send_button = ctk.CTkButton(chat_frame, text="Send", command=send_message)
send_button.pack(pady=5)
'''
code functions
'''


def scrape_github(username):
    '''
    scrapes a users github repositories pagea to get a dictionary that contains repository names (made dictiobnary as readme links no. of stars and other attributes could be added)
    returns a list of dictionarys where each dictioary contains repository atitributes 
    

    HTML for github repo:


    '''

    url = f"https://github.com/{username}?tab=repositories"

    response = requests.get(url) #gets the page from the website
    response.raise_for_status() # checks the request works, gets error code if not eg 404, 400 etc, 200 is good
    #would fail here if the user didnt exist

    
    soup = BeautifulSoup(response.text, "html.parser") # turns the html data into something we can search on 

    repositories = []

    repo_links = soup.select('a[itemprop="name codeRepository"]') #this is what comes before the repo nam eeach time in the html code 
    # loop through each time that we find a repository name 

    for repo_link in repo_links:
        repo_name = repo_link.text.strip()
        relative_url = repo_link.get("href") #gets the unique part of the url

        repo_url = f"https://github.com{relative_url}" #re build the url with the standard start 
        readme_url = f"{repo_url}#readme"

        #dictionary 
        repositories.append({
            "Repository Name": repo_name,
            "Repository URL": repo_url,
            "README URL": readme_url
        })

    return repositories

#print(scrape_github("AlfieRootham"))

def get_excel(repositories, file_path):
    '''
    using the scrape github function 
    turns the list into a data frame with pandas and then writes this to an excel file
    to be called under the execute search function
    '''

    df = pd.DataFrame(repositories)
    df.to_excel(file_path, index=False)




app.mainloop()