from models import Note , Tag, NoteTag
from database import engine , SessionLocal , Base

Base.metadata.create_all(bind=engine)



def main_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Manage Notes")
        print("2. Manage Tags")
        print("3. Tag Operations")
        print("4. Search / Reports")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            manage_notes()
        elif choice == "2":
            manage_tags()
        elif choice == "3":
            tag_operations()
        elif choice == "4":
            search_reports()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

# ! Notes managment function

def add_notes(title,content):
    db = SessionLocal()
    try:
        new_note = Note(title = title,content = content)

        db.add(new_note)

        db.commit()
        db.refresh(new_note)
        print(f"Note is created with title : {title}")

    except Exception as e:
        db.rollback()
        print("Error : ",e)

    finally:
        db.close()

def show_all_notes():
    db = SessionLocal()
    try:
        data = db.query(Note).all()
        print("All notes")
        for note in data:
            print(f"title : {note.title} ")

    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()

def update_note_by_id(id,title,content):
    db = SessionLocal()
    try:
        data = db.query(Note).filter(Note.id == id).first()

        data.title = title
        data.content = content

        db.commit()
        db.refresh(data)
        print("Record Updated")
    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()

def delete_note(id):
    db = SessionLocal()
    try:
        data = db.query(Note).filter(Note.id == id).first()
        db.delete(data)
        db.commit()
        print("User deleted")
    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()



def manage_notes():
    while True:
        print("\n--- MANAGE NOTES ---")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Update Note")
        print("4. Delete Note")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Enter title: ")
            content = input("Enter content: ")
            if title and content:
                add_notes(title,content)
            else:
                print("Missing information")

        elif choice == "2":
            show_all_notes()  # fetch and display notes

        elif choice == "3":
            note_id = input("Enter note ID: ")
            new_title = input("Enter new title: ")
            new_content = input("Enter new content: ")
            update_note_by_id(note_id,new_title,new_content)  # update note

        elif choice == "4":
            note_id = input("Enter note ID: ")
            delete_note(note_id)  # delete note

        elif choice == "5":
            break
        else:
            print("Invalid choice!")


#! Manage Tag
def add_tags(name):
    db = SessionLocal()
    try:
        new_tag = Tag(name=name)

        db.add(new_tag)

        db.commit()
        db.refresh(new_tag)
        print(f"Note is created with title : {name}")

    except Exception as e:
        db.rollback()
        print("Error : ",e)

    finally:
        db.close()

def show_all_tags():
    db = SessionLocal()
    try:
        data = db.query(Tag).all()
        print("All Tag")
        for tag in data:
            print(f"title : {tag.name} ")

    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()

def delete_tag_by_id(id):
    db = SessionLocal()
    try:
        data = db.query(Tag).filter(Tag.id == id).first()
        db.delete(data)
        db.commit()

        print("Tag Deleted")
    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()


def manage_tags():
    while True:
        print("\n--- MANAGE TAGS ---")
        print("1. Add Tag")
        print("2. View Tags")
        print("3. Delete Tag")
        print("4. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter tag name: ")
            add_tags(name)  # insert tag

        elif choice == "2":
            show_all_tags()  # view tags

        elif choice == "3":
            tag_id = input("Enter tag ID: ")
            delete_tag_by_id(tag_id)  # delete tag

        elif choice == "4":
            break
        else:
            print("Invalid choice!")


def add_tag_to_note(note_id,tag_id):
    db = SessionLocal()
    try:
        note = db.get(Note, note_id)
        tag = db.get(Tag, tag_id)

        if not note:
            print("Note not found")
            return
        
        if not tag:
            print("Tag not found")
            return
        
        existing = db.query(NoteTag).filter_by(note_id = note_id,tag_id = tag_id).first()

        if existing:
            print("Tag is already linked to this note")
            return
        
        link = NoteTag(note_id= note_id , tag_id = tag_id)
        db.add(link)
        db.commit()
        db.refresh(link)

        print("Tag added to note")

    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()

def remove_tag_from_note(note_id,tag_id):
    db = SessionLocal()
    try:
        note = db.get(Note, note_id)
        tag = db.get(Tag, tag_id)

        if not note:
            print("Note not found")
            return
        
        if not tag:
            print("Tag not found")
            return
        
        existing = db.query(NoteTag).filter_by(note_id = note_id,tag_id = tag_id).first()

        if not existing:
            print("Tag is not linked to this note")
            return
        
        # link = NoteTag(note_id= note_id , tag_id = tag_id)
        db.delete(existing)
        db.commit()
        # db.refresh(link)

        print("Tag removed from the note")

    except Exception as e:
        db.rollback()
        print("Error ",e)
    finally:
        db.close()


def view_tags_of_note(note_id):
    db = SessionLocal()
    note = db.get(Note, note_id)
    if not note:
        print("Note not found!")
        return

    tags = db.query(Tag).join(NoteTag).filter(
        NoteTag.note_id == note_id
    ).all()

    if not tags:
        print("No tags found.")
        return

    print("\nTags:")
    for tag in tags:
        print(f"{tag.id} - {tag.name}")


def view_notes_by_tag(tag_id):
    db = SessionLocal()
    tag = db.get(Tag, tag_id)
    if not tag:
        print("Tag not found!")
        return

    notes = db.query(Note).join(NoteTag).filter(
        NoteTag.tag_id == tag_id
    ).all()

    if not notes:
        print("No notes found.")
        return

    print("\nNotes:")
    for note in notes:
        print(f"{note.id} - {note.title}")

def tag_operations():
    while True:
        print("\n--- TAG OPERATIONS ---")
        print("1. Add Tag to Note")
        print("2. Remove Tag from Note")
        print("3. View Tags of a Note")
        print("4. View Notes by Tag")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            note_id = input("Enter note ID: ")
            tag_id = input("Enter tag ID: ")
            add_tag_to_note(note_id,tag_id)  # validate + insert into NoteTag

        elif choice == "2":
            note_id = input("Enter note ID: ")
            tag_id = input("Enter tag ID: ")
            remove_tag_from_note(note_id,tag_id)  # delete from NoteTag

        elif choice == "3":
            note_id = input("Enter note ID: ")
            view_tags_of_note(note_id)  # fetch tags for note

        elif choice == "4":
            tag_id = input("Enter tag ID: ")
            view_notes_by_tag(tag_id)  # fetch notes for tag

        elif choice == "5":
            break
        else:
            print("Invalid choice!")


def search_reports():
    while True:
        print("\n--- SEARCH / REPORTS ---")
        print("1. Search Notes by Keyword")
        print("2. Count Notes per Tag")
        print("3. Most Used Tag")
        print("4. Notes Without Tags")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            keyword = input("Enter keyword: ")
            pass  # LIKE query

        elif choice == "2":
            pass  # GROUP BY + COUNT

        elif choice == "3":
            pass  # ORDER BY DESC LIMIT 1

        elif choice == "4":
            pass  # LEFT JOIN / subquery

        elif choice == "5":
            break
        else:
            print("Invalid choice!")






if __name__ == "__main__":
    main_menu()

