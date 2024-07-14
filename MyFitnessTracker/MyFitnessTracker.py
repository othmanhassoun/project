import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# Dummy data for demonstration
activities = []
goals = []

# Helper functions
def validate_entry(entry):
    return entry.strip() != ''

# Main Application Class
class MyFitnessTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyFitnessTracker")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_frame()
        tk.Label(self, text="Welcome to MyFitnessTracker", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Get Started", command=self.show_dashboard).pack(pady=10)
        tk.Button(self, text="About", command=self.show_about_screen).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=10)

    def show_dashboard(self):
        self.clear_frame()
        tk.Label(self, text="MyFitnessTracker Dashboard", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Log Activity", command=self.show_log_activity_screen).pack(pady=10)
        tk.Button(self, text="View Goals", command=self.show_view_goals_screen).pack(pady=10)
        tk.Button(self, text="View Progress", command=self.show_view_progress_screen).pack(pady=10)
        tk.Button(self, text="Generate Report", command=self.show_generate_report_screen).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=10)

    def show_log_activity_screen(self):
        self.clear_frame()
        tk.Label(self, text="Log Your Activity", font=("Arial", 24)).pack(pady=20)
        
        tk.Label(self, text="Activity Type").pack(pady=5)
        activity_type = ttk.Combobox(self, values=["Running", "Cycling", "Swimming", "Other"])
        activity_type.pack(pady=5)
        
        tk.Label(self, text="Duration (minutes)").pack(pady=5)
        duration = tk.Entry(self)
        duration.pack(pady=5)
        
        tk.Label(self, text="Calories Burned").pack(pady=5)
        calories = tk.Entry(self)
        calories.pack(pady=5)
        
        def submit_activity():
            if not validate_entry(activity_type.get()) or not validate_entry(duration.get()) or not validate_entry(calories.get()):
                messagebox.showerror("Invalid Entry", "Please fill in all fields.")
                return
            activities.append({
                "type": activity_type.get(),
                "duration": int(duration.get()),
                "calories": int(calories.get()),
                "date": datetime.date.today()
            })
            messagebox.showinfo("Success", "Activity logged successfully.")
            self.show_dashboard()
        
        tk.Button(self, text="Submit", command=submit_activity).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.show_dashboard).pack(pady=10)

    def show_view_goals_screen(self):
        self.clear_frame()
        tk.Label(self, text="Your Fitness Goals", font=("Arial", 24)).pack(pady=20)

        for goal in goals:
            tk.Label(self, text=f"Goal: {goal['description']} - Status: {'Completed' if goal['completed'] else 'Incomplete'}").pack(pady=5)
        
        tk.Button(self, text="Add New Goal", command=self.add_goal).pack(pady=10)
        tk.Button(self, text="Edit Goal", command=self.edit_goal).pack(pady=10)
        tk.Button(self, text="Delete Goal", command=self.delete_goal).pack(pady=10)
        tk.Button(self, text="Back", command=self.show_dashboard).pack(pady=10)
    
    def add_goal(self):
        goal_description = simpledialog.askstring("New Goal", "Enter your goal:")
        if goal_description:
            goals.append({"description": goal_description, "completed": False})
            messagebox.showinfo("Success", "Goal added successfully.")
            self.show_view_goals_screen()
    
    def edit_goal(self):
        goal_description = simpledialog.askstring("Edit Goal", "Enter the goal description to edit:")
        for goal in goals:
            if goal["description"] == goal_description:
                new_description = simpledialog.askstring("Edit Goal", "Enter the new description:")
                if new_description:
                    goal["description"] = new_description
                    messagebox.showinfo("Success", "Goal edited successfully.")
                    self.show_view_goals_screen()
                    return
        messagebox.showerror("Error", "Goal not found.")

    def delete_goal(self):
        goal_description = simpledialog.askstring("Delete Goal", "Enter the goal description to delete:")
        for goal in goals:
            if goal["description"] == goal_description:
                goals.remove(goal)
                messagebox.showinfo("Success", "Goal deleted successfully.")
                self.show_view_goals_screen()
                return
        messagebox.showerror("Error", "Goal not found.")

    def show_view_progress_screen(self):
        self.clear_frame()
        tk.Label(self, text="Your Progress", font=("Arial", 24)).pack(pady=20)
        
        if not activities:
            tk.Label(self, text="No activities logged yet.").pack(pady=10)
        else:
            figure = plt.Figure(figsize=(6,5), dpi=100)
            ax = figure.add_subplot(111)
            dates = [activity['date'] for activity in activities]
            calories = [activity['calories'] for activity in activities]
            ax.plot(dates, calories, marker='o')
            chart = FigureCanvasTkAgg(figure, self)
            chart.get_tk_widget().pack(pady=10)
        
        tk.Button(self, text="Back", command=self.show_dashboard).pack(pady=10)

    def show_generate_report_screen(self):
        self.clear_frame()
        tk.Label(self, text="Generate Fitness Report", font=("Arial", 24)).pack(pady=20)
        
        tk.Label(self, text="Select Date Range").pack(pady=5)
        tk.Label(self, text="Start Date").pack(pady=5)
        start_date = tk.Entry(self)
        start_date.pack(pady=5)
        
        tk.Label(self, text="End Date").pack(pady=5)
        end_date = tk.Entry(self)
        end_date.pack(pady=5)
        
        def generate_report():
            start = start_date.get()
            end = end_date.get()
            if not validate_entry(start) or not validate_entry(end):
                messagebox.showerror("Invalid Entry", "Please fill in all fields.")
                return
            try:
                start_date_parsed = datetime.datetime.strptime(start, '%Y-%m-%d').date()
                end_date_parsed = datetime.datetime.strptime(end, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter valid dates in YYYY-MM-DD format.")
                return
            report_activities = [activity for activity in activities if start_date_parsed <= activity['date'] <= end_date_parsed]
            report_text = "\n".join([f"{activity['date']}: {activity['type']} - {activity['duration']} minutes, {activity['calories']} calories" for activity in report_activities])
            messagebox.showinfo("Fitness Report", report_text)
        
        tk.Button(self, text="Generate", command=generate_report).pack(pady=10)
        tk.Button(self, text="Cancel", command=self.show_dashboard).pack(pady=10)

    def show_about_screen(self):
        self.clear_frame()
        tk.Label(self, text="About MyFitnessTracker", font=("Arial", 24)).pack(pady=20)
        tk.Label(self, text="MyFitnessTracker is a tool to help you track your fitness activities, set goals, and monitor progress.").pack(pady=10)
        tk.Button(self, text="Back", command=self.show_dashboard).pack(pady=10)
    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MyFitnessTrackerApp()
    app.mainloop()
