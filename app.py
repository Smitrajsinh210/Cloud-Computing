import os
import streamlit as st
import json
from datetime import datetime
import time

# Directory to store notes
NOTES_DIR = "notes"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Shared links JSON file
SHARED_LINKS_FILE = "shared_links.json"
if not os.path.exists(SHARED_LINKS_FILE):
    with open(SHARED_LINKS_FILE, "w") as file:
        json.dump({}, file)

# Function to save a note
def save_note(note_content, note_title):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{note_title}_{timestamp}.txt"
    file_path = os.path.join(NOTES_DIR, filename)
    with open(file_path, "w") as file:
        file.write(note_content)
    return filename

# Function to load all notes
def load_notes():
    notes = []
    for filename in os.listdir(NOTES_DIR):
        file_path = os.path.join(NOTES_DIR, filename)
        with open(file_path, "r") as file:
            content = file.read()
            notes.append({"filename": filename, "content": content})
    return notes

# Function to delete a note
def delete_note(filename):
    file_path = os.path.join(NOTES_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

# Function to get a shared note
def get_shared_note(link_id):
    with open(SHARED_LINKS_FILE, "r") as file:
        shared_links = json.load(file)
    filename = shared_links.get(link_id)
    if filename:
        file_path = os.path.join(NOTES_DIR, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
    return None

# Streamlit UI
st.title("☁️ Cloud Notes Sharing App")
st.subheader("Write, save, and share your notes easily.")

# Check if viewing a shared note
query_params = st.experimental_get_query_params()
if "view" in query_params:
    link_id = query_params["view"][0]
    shared_note = get_shared_note(link_id)
    if shared_note:
        st.success("Shared Note:")
        st.write(shared_note)
    else:
        st.error("This note does not exist or the link is invalid.")
    st.stop()

# Add a new note
st.write("### Add a New Note")
note_title = st.text_input("Note Title")
note_content = st.text_area("Write your note here...", height=100)
if st.button("Save Note"):
    if note_title.strip() and note_content.strip():
        filename = save_note(note_content.strip(), note_title.strip())
        st.success(f"Note `{note_title}` saved!")
        time.sleep(1)  # Add a small delay before refreshing
        st.experimental_set_query_params(reload="true")
    else:
        st.error("Both title and content are required.")

# Display saved notes
st.write("### Your Saved Notes")
notes = load_notes()

if notes:
    for note in notes:
        with st.expander(f"🗒️ {note['filename']}"):
            st.write(note["content"])
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"❌ Delete `{note['filename']}`", key=f"del_{note['filename']}"):
                    delete_note(note["filename"])
                    st.success(f"Deleted `{note['filename']}`!")
                    time.sleep(1)  # Add a small delay before refreshing
                    st.experimental_set_query_params(reload="true")
           
else:
    st.info("No notes found. Add a new note above.")

# Footer
st.markdown("---")
st.write("🔒 **Notes are securely stored on this cloud app.**")



