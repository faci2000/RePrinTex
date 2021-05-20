from controllers.controller import Controller


class StatusBarController:
    def __init__(self, parent, statusbar) -> None:
        self.parent = parent
        self.statusbar = statusbar
        Controller().set_statusbar_controller(self)

    def task_starting(self):
        self.statusbar.set_status("Task in progress...")
