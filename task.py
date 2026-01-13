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


def start_task(task_id):
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task["id"] == task_id:
            task_found = True
            if task["status"] != "todo":
                print(f"Error: Task {task_id} is already '{task['status']}'. Only tasks in 'todo' status can be started.")
                return
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            break
    
    if not task_found:
        print(f"Error: Task with ID {task_id} not found")
        return
    
    save_tasks(tasks)
    print(f"Task {task_id} started successfully")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(new_tasks) == len(tasks):
        print(f"Error: Task with ID {task_id} not found")
        return
    
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted successfully")


def list_tasks():
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found")
        return
    
    grouped_tasks = {
        "todo": [],
        "in-progress": [],
        "done": []
    }
    
    for task in tasks:
        status = task.get("status", "todo")
        if status in grouped_tasks:
            grouped_tasks[status].append(task)
    
    status_labels = {
        "todo": "📋 To Do",
        "in-progress": "🚧 In Progress",
        "done": "✅ Done"
    }
    
    for status in ["todo", "in-progress", "done"]:
        tasks_in_status = grouped_tasks[status]
        if tasks_in_status:
            print(f"\n{status_labels[status]}")
            print("-" * 50)
            for task in tasks_in_status:
                print(f"  [{task['id']}] {task['description']}")
    
    print(f"\nTotal tasks: {len(tasks)}")


def main():
    parser = argparse.ArgumentParser(description="Task CLI - Simple todo list manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument("-s", "--status", help="New task status (todo, in-progress, done)")

    start_parser = subparsers.add_parser("start", help="Mark a todo task as in-progress")
    start_parser.add_argument("id", type=int, help="Task ID to start")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")
    
    list_parser = subparsers.add_parser("list", help="List all tasks grouped by status")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description, args.status)
    elif args.command == "start":
        start_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
