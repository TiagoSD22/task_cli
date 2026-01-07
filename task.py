import json
import argparse
from pathlib import Path
from datetime import datetime

TASKS_FILE = Path("tasks.json")

def load_tasks():
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    tasks = load_tasks()
    task_id = max([task["id"] for task in tasks], default=0) + 1
    
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def main():
    parser = argparse.ArgumentParser(description="Task CLI - Simple todo list manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_task(args.description)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
