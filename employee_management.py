#!/usr/bin/env python3
"""
Employee Management System
Handles employee database and task assignments
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class EmployeeManager:
    def __init__(self, db_path="employees.db"):
        self.db_path = db_path
        self.init_database()
        self.populate_employees()
    
    def init_database(self):
        """Initialize employee database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_employees(self):
        """Add all employees to database"""
        employees_data = [
            ("YASEEN", "MANAGEMENT"),
            ("ABHISHEK", "GAME"),
            ("SHREESURYAMAN", "GAME"),
            ("SURAJ", "ROBOTICS"),
            ("ABHISHEK P", "ROBOTICS"),
            ("AKASH", "AI/ML"),
            ("KARAN", "AI/ML"),
            ("NIHAL", "BLOCKCHAIN"),
            ("VISHAL", "GAME"),
            ("VINAYAK", "TESTER"),
            ("VIJAY", "AI/ML"),
            ("KARTHIKEYA", "AI/ML"),
            ("TEJASWI", "ROBOTICS"),
            ("SHIVAM", "BLOCKCHAIN"),
            ("VAIBHAV", "AI VIDEO"),
            ("NIPUN", "AI/ML"),
            ("RUTUJA", "BIOTECHNOLOGY"),
            ("GAUDHAMI READY", "SOCIAL MEDIA"),
            ("MOKSH", "GAME"),
            ("SHANTANU", "BLOCKCHAIN"),
            ("SHASHANK G", "AI/ML"),
            ("BHAVESH", "AI/ML"),
            ("VEDANG", "GAME"),
            ("RAJ", "AI/ML"),
            ("NISARG", "AI/ML"),
            ("SACHIN", "GAME"),
            ("ADITYA KHUTALE", "AI/ML"),
            ("YASHIKA", "AI/ML"),
            ("SUSHRUT", "BIOTECHNOLOGY"),
            ("KANAV", "AI VIDEO"),
            ("RISHABH YADAV", "AI/ML"),
            ("ASHMIT", "AI/ML"),
            ("SHAHSANK M", "AI/ML"),
            ("ANMOL", "AI/ML"),
            ("NILESH", "AI/ML"),
            ("SEEYA", "AI/ML"),
            ("SANKALP", "AI/ML"),
            ("SEJAL", "AI/ML"),
            ("CHANDRESH", "AI/ML"),
            ("NOOPUR", "AI/ML"),
            ("PARTH", "AI/ML"),
            ("NIKHIL", "AI/ML"),
            ("YASH", "AI/ML"),
            ("USMAN", "ROBOTICS"),
            ("SOHAM", "AI/ML"),
            ("HETH", "ROBOTICS"),
            ("SIDDHESH", "AI/ML"),
            ("RANJEET", "AI/ML"),
            ("SIDDHESH T", "AI/ML"),
            ("HRUJUL", "AI/ML"),
            ("VIJAY D", "AI/ML"),
            ("SOHAM K", "AI/ML"),
            ("SIDDHESH N", "AI/ML"),
            ("SHIVAM PAL", "AI/ML"),
            ("ISHAN", "AI/ML")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if employees already exist
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO employees (name, department) VALUES (?, ?)",
                employees_data
            )
            conn.commit()
        
        conn.close()
    
    def get_all_employees(self) -> List[Dict]:
        """Get all employees"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, department, status, created_at 
            FROM employees 
            ORDER BY department, name
        """)
        
        employees = []
        for row in cursor.fetchall():
            employees.append({
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "status": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        return employees
    
    def get_employees_by_department(self, department: str) -> List[Dict]:
        """Get employees by department"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, department, status 
            FROM employees 
            WHERE department = ? AND status = 'active'
            ORDER BY name
        """, (department,))
        
        employees = []
        for row in cursor.fetchall():
            employees.append({
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "status": row[3]
            })
        
        conn.close()
        return employees
    
    def assign_task(self, employee_id: int, title: str, description: str = "", priority: str = "medium", due_date: str = "") -> bool:
        """Assign task to employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO tasks (employee_id, title, description, priority, due_date)
                VALUES (?, ?, ?, ?, ?)
            """, (employee_id, title, description, priority, due_date))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error assigning task: {e}")
            conn.close()
            return False
    
    def get_employee_tasks(self, employee_id: int) -> List[Dict]:
        """Get tasks for specific employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.id, t.title, t.description, t.priority, t.status, t.assigned_at, t.due_date,
                   e.name, e.department
            FROM tasks t
            JOIN employees e ON t.employee_id = e.id
            WHERE t.employee_id = ?
            ORDER BY t.assigned_at DESC
        """, (employee_id,))
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                "task_id": row[0],
                "title": row[1],
                "description": row[2],
                "priority": row[3],
                "status": row[4],
                "assigned_at": row[5],
                "due_date": row[6],
                "employee_name": row[7],
                "department": row[8]
            })
        
        conn.close()
        return tasks
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.id, t.title, t.description, t.priority, t.status, t.assigned_at, t.due_date,
                   e.name, e.department
            FROM tasks t
            JOIN employees e ON t.employee_id = e.id
            ORDER BY t.assigned_at DESC
        """)
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                "task_id": row[0],
                "title": row[1],
                "description": row[2],
                "priority": row[3],
                "status": row[4],
                "assigned_at": row[5],
                "due_date": row[6],
                "employee_name": row[7],
                "department": row[8]
            })
        
        conn.close()
        return tasks
    
    def update_task_status(self, task_id: int, status: str) -> bool:
        """Update task status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE tasks SET status = ? WHERE id = ?
            """, (status, task_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            conn.close()
            return False
    
    def get_department_stats(self) -> Dict:
        """Get department statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT department, COUNT(*) as count
            FROM employees
            WHERE status = 'active'
            GROUP BY department
            ORDER BY count DESC
        """)
        
        dept_stats = {}
        for row in cursor.fetchall():
            dept_stats[row[0]] = row[1]
        
        conn.close()
        return dept_stats

# Global instance
employee_manager = EmployeeManager()

if __name__ == "__main__":
    # Test the system
    print("Employee Management System initialized")
    employees = employee_manager.get_all_employees()
    print(f"Total employees: {len(employees)}")
    
    dept_stats = employee_manager.get_department_stats()
    print("Department statistics:")
    for dept, count in dept_stats.items():
        print(f"  {dept}: {count} employees")