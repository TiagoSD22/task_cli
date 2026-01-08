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

def update_task(task_id, description=None, status=None):
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task["id"] == task_id:
            task_found = True
            if description:
                task["description"] = description
            if status:
                if status not in ["todo", "in-progress", "done"]:
                    print(f"Error: Invalid status '{status}'. Valid statuses: todo, in-progress, done")
                    return
                task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            break
    
    if not task_found:
        print(f"Error: Task with ID {task_id} not found")
        return
    
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully")

def main():
    parser = argparse.ArgumentParser(description="Task CLI - Simple todo list manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument("-s", "--status", help="New task status (todo, in-progress, done)")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description, args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
