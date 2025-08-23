import os
import json
from datetime import datetime
import questionary
from rich.console import Console
from rich.table import Table

console = Console()

# Always save/load projects.json from the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "projects.json"))
print(f"📂 Using projects.json at: {DATA_FILE}")


# -------------------- Core Functions --------------------
def load_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# def save_projects(projects):
#     with open(DATA_FILE, "w", encoding="utf-8") as f:
#         json.dump(projects, f, indent=4)
#     print(f"💾 Saved {len(projects)} project(s) to {DATA_FILE}")
def save_projects(projects):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=4)
    print(f"💾 Saved {len(projects)} project(s) to {DATA_FILE}")
    print(f"📂 Verify by opening this file manually: {DATA_FILE}")


def backup_projects():
    if os.path.exists(DATA_FILE):
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.rename(DATA_FILE, backup_name)
        print(f"🔒 Backup created: {backup_name}")

def add_project(name, tech, notes):
    projects = load_projects()
    project = {
        "name": name,
        "tech": [t.strip() for t in tech.split(",")],
        "notes": notes,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    projects.append(project)
    save_projects(projects)
    print(f"✅ Project '{name}' added!")

def list_projects():
    projects = load_projects()
    if not projects:
        console.print("[red]⚠️ No projects found![/red]")
        return

    table = Table(title="🚀 Your Projects")
    table.add_column("No.", justify="right", style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Tech", style="magenta")
    table.add_column("Notes", style="yellow")
    table.add_column("Added", style="blue")

    for i, project in enumerate(projects, start=1):
        table.add_row(str(i), project["name"], ", ".join(project["tech"]), project["notes"], project["date_added"])

    console.print(table)
    

def search_projects(name=None, tech=None):
    projects = load_projects()
    results = []
    for p in projects:
        if name and name.lower() in p["name"].lower():
            results.append(p)
        elif tech and any(tech.lower() in t.lower() for t in p["tech"]):
            results.append(p)

    if results:
        for p in results:
            console.print(f"[green]{p['name']}[/green] - {', '.join(p['tech'])} - {p['notes']}")
    else:
        console.print("[red]No matching projects found![/red]")

def update_project(name, tech=None, notes=None):
    projects = load_projects()
    for p in projects:
        if p["name"].lower() == name.lower():
            if tech:
                p["tech"] = [t.strip() for t in tech.split(",")]
            if notes:
                p["notes"] = notes
            save_projects(projects)
            print(f"✏️ Project '{name}' updated!")
            return
    print("⚠️ Project not found.")

def delete_project():
    projects = load_projects()
    if not projects:
        print("⚠️ No projects to delete.")
        return

    # Show multi-select checklist with project names
    names = questionary.checkbox(
        "Select project(s) to delete:",
        choices=[p["name"] for p in projects]
    ).ask()

    if not names:  # user pressed enter without selecting
        print("⚠️ No projects selected.")
        return

    before_count = len(projects)
    projects = [p for p in projects if p["name"] not in names]
    save_projects(projects)
    deleted_count = before_count - len(projects)
    print(f"🗑️ Deleted {deleted_count} project(s): {', '.join(names)}")


def export_projects():
    projects = load_projects()
    with open("projects.md", "w", encoding="utf-8") as f:
        f.write("# 📦 Exported Projects\n\n")
        for p in projects:
            f.write(f"- **{p['name']}** ({', '.join(p['tech'])}) → {p['notes']} [{p['date_added']}]\n")
    print("📄 Exported to projects.md")

def export_projects_csv():
    import csv
    projects = load_projects()
    with open("projects.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Tech", "Notes", "Date Added"])
        for p in projects:
            writer.writerow([p["name"], ", ".join(p["tech"]), p["notes"], p["date_added"]])
    print("📊 Exported to projects.csv")


# -------------------- Interactive Menu --------------------
def menu():
    while True:
        choice = questionary.select(
            "Choose an action:",
            choices=[
                "Add Project",
                "List Projects",
                "Search Projects",
                "Update Project",
                "Delete Project",
                "Export to Markdown",
                "Export to CSV",
                "Exit"
            ]
        ).ask()

        if choice == "Add Project":
            name = questionary.text("Project name:").ask()
            tech = questionary.text("Technologies (comma separated):").ask()
            notes = questionary.text("Notes:").ask()
            add_project(name, tech, notes)

        elif choice == "List Projects":
            list_projects()

        elif choice == "Search Projects":
            search_by = questionary.select("Search by:", choices=["Name", "Tech"]).ask()
            if search_by == "Name":
                name = questionary.text("Enter project name:").ask()
                search_projects(name=name)
            else:
                tech = questionary.text("Enter technology:").ask()
                search_projects(tech=tech)

        elif choice == "Update Project":
            name = questionary.text("Project name to update:").ask()
            tech = questionary.text("New technologies (leave blank to skip):").ask()
            notes = questionary.text("New notes (leave blank to skip):").ask()
            update_project(name, tech if tech else None, notes if notes else None)

        elif choice == "Delete Project":
            delete_project()



        elif choice == "Export to Markdown":
            export_projects()

        elif choice == "Export to CSV":
            export_projects_csv()

        elif choice == "Exit":
            print("👋 Goodbye!")
            break

# -------------------- Entry Point --------------------
if __name__ == "__main__":
    menu()


