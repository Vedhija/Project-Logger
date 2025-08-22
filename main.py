import argparse
import json
from datetime import datetime
import os
import csv

DATA_FILE = "projects.json"

def load_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_projects(projects):
    with open(DATA_FILE, "w") as f:
        json.dump(projects, f, indent=4)

def add_project(name, tech, notes):
    projects = load_projects()
    project = {
        "name": name,
        "tech": [t.strip() for t in tech.split(",")],  # store as list
        "notes": notes,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    projects.append(project)
    save_projects(projects)
    print(f"✅ Project '{name}' added!")

def list_projects():
    projects = load_projects()
    if not projects:
        print("⚠️ No projects found.")
        return
    for idx, project in enumerate(projects, 1):
        print(f"\n{idx}. {project['name']}")
        print(f"   Tech: {', '.join(project['tech'])}")
        print(f"   Notes: {project['notes']}")
        print(f"   Added: {project['date_added']}")

def search_projects(name=None, tech=None):
    projects = load_projects()
    results = []

    for project in projects:
        if name and name.lower() in project["name"].lower():
            results.append(project)
        elif tech:
            if any(tech.lower() in t.lower() for t in project["tech"]):
                results.append(project)

    if results:
        print(f"🔍 Found {len(results)} project(s):")
        for i, project in enumerate(results, start=1):
            print(f"\n{i}. {project['name']}")
            print(f"   Tech: {', '.join(project['tech'])}")
            print(f"   Notes: {project['notes']}")
            print(f"   Added: {project['date_added']}")
    else:
        print("❌ No projects found matching your search.")

# 🔹 Update project
def update_project(name, tech=None, notes=None):
    projects = load_projects()
    updated = False

    for project in projects:
        if project["name"].lower() == name.lower():
            if tech:
                project["tech"] = [t.strip() for t in tech.split(",")]
            if notes:
                project["notes"] = notes
            updated = True
            break

    if updated:
        save_projects(projects)
        print(f"✅ Project '{name}' updated successfully!")
    else:
        print(f"❌ No project found with name '{name}'.")

def delete_project(name):
    projects = load_projects()
    new_projects = [p for p in projects if p["name"].lower() != name.lower()]

    if len(new_projects) == len(projects):
        print(f"❌ No project found with name '{name}'.")
    else:
        save_projects(new_projects)
        print(f"🗑️ Project '{name}' deleted successfully!")

def export_projects():
    projects = load_projects()
    if not projects:
        print("⚠️ No projects to export.")
        return

    with open("projects.md", "w", encoding="utf-8") as f:
        f.write("# 📂 Project Log\n\n")
        for idx, project in enumerate(projects, start=1):
            f.write(f"## {idx}. {project['name']}\n")
            f.write(f"- **Tech:** {', '.join(project['tech'])}\n")
            f.write(f"- **Notes:** {project['notes']}\n")
            f.write(f"- **Added:** {project['date_added']}\n\n")

    print("✅ Projects exported to projects.md")


def export_projects_csv():
    projects = load_projects()
    if not projects:
        print("⚠️ No projects to export.")
        return

    with open("projects.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Technologies", "Notes", "Date Added"])
        for project in projects:
            writer.writerow([
                project["name"],
                ", ".join(project["tech"]),
                project["notes"],
                project["date_added"]
            ])

    print("✅ Projects exported to projects.csv")

def main():
    parser = argparse.ArgumentParser(description="Project Logger CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add project
    add_parser = subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("--tech", required=True, help="Technologies used (comma separated)")
    add_parser.add_argument("--notes", required=True, help="Notes or insights")

    # List projects
    subparsers.add_parser("list", help="List all projects")
    # Export projects
    subparsers.add_parser("export", help="Export projects to Markdown file")
    # Export CSV
    subparsers.add_parser("export-csv", help="Export projects to CSV file")

    # Search projects
    search_parser = subparsers.add_parser("search", help="Search projects")
    search_parser.add_argument("--name", help="Search by project name")
    search_parser.add_argument("--tech", help="Search by technology")

    # 🔹 Update projects
    update_parser = subparsers.add_parser("update", help="Update an existing project")
    update_parser.add_argument("--name", required=True, help="Project name to update")
    update_parser.add_argument("--tech", help="Updated technologies (comma separated)")
    update_parser.add_argument("--notes", help="Updated notes")

    # Delete project
    delete_parser = subparsers.add_parser("delete", help="Delete a project")
    delete_parser.add_argument("--name", required=True, help="Project name to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_project(args.name, args.tech, args.notes)
    elif args.command == "list":
        list_projects()
    elif args.command == "search":
        search_projects(name=args.name, tech=args.tech)
    elif args.command == "update":
        update_project(name=args.name, tech=args.tech, notes=args.notes)
    elif args.command == "delete":
        delete_project(name=args.name)
    elif args.command == "export":
        export_projects()
    elif args.command == "export-csv":
        export_projects_csv()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
