# app.py
from lightning.app import CloudCompute, LightningApp, LightningWork


class YourComponent(LightningWork):
    def run(self):
        print("RUN ANY PYTHON CODE HERE")


# run on a cloud machine ("cpu", "gpu", ...)
compute = CloudCompute("gpu")
component = YourComponent(cloud_compute=compute)
app = LightningApp(component)
