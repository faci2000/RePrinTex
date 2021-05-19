class StatusBarController:
    def __init__(self, parent, statusbar) -> None:
        self.parent = parent
        self.statusbar = statusbar

    def task_starting(self):
        self.statusbar.set_status("Task in progress...")
