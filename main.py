import json
import argparse
from datetime import datetime
from pathlib import Path

# File to store projects
DB_FILE = Path("projects.json")

# Load projects
def load_projects():
    if DB_FILE.exists():
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

# Save projects
def save_projects(projects):
    with open(DB_FILE, "w") as f:
        json.dump(projects, f, indent=4)

# Add a project
def add_project(name, tech, notes):
    projects = load_projects()
    project = {
        "name": name,
        "tech": tech.split(","),
        "notes": notes,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    projects.append(project)
    save_projects(projects)
    print(f"✅ Project '{name}' added!")

# List all projects
def list_projects():
    projects = load_projects()
    if not projects:
        print("No projects logged yet.")
        return
    for i, project in enumerate(projects, 1):
        print(f"\n{i}. {project['name']}")
        print(f"   Tech: {', '.join(project['tech'])}")
        print(f"   Notes: {project['notes']}")
        print(f"   Added: {project['date_added']}")

# CLI Commands
def main():
    parser = argparse.ArgumentParser(description="Personal Project Logger")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("name", help="Project name")
    add_parser.add_argument("--tech", default="", help="Technologies used (comma-separated)")
    add_parser.add_argument("--notes", default="", help="Notes/what you learned")

    # List command
    subparsers.add_parser("list", help="List all projects")

    args = parser.parse_args()

    if args.command == "add":
        add_project(args.name, args.tech, args.notes)
    elif args.command == "list":
        list_projects()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
