# app.py
from lightning.app import LightningApp, LightningFlow, LightningWork
from lightning.app.runners import MultiProcessRuntime


class TrainComponent(LightningWork):
    def run(self, x):
        print(f"train a model on {x}")


class AnalyzeComponent(LightningWork):
    def run(self, x):
        print(f"analyze model on {x}")


class WorkflowOrchestrator(LightningFlow):
    def __init__(self) -> None:
        super().__init__()
        self.train = TrainComponent()
        self.analyze = AnalyzeComponent()

    def run(self):
        self.train.run("GPU machine 1")
        self.analyze.run("CPU machine 2")


app = LightningApp(WorkflowOrchestrator())
MultiProcessRuntime(app).dispatch()
