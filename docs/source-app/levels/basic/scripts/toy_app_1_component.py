# app.py
from lightning.app import LightningApp, LightningFlow, LightningWork


class Component(LightningWork):
    def run(self, x):
        print(x)


class WorkflowOrchestrator(LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.component = Component()

    def run(self):
        self.component.run("i love Lightning")


app = LightningApp(WorkflowOrchestrator())
