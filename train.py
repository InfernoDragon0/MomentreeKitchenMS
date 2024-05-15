from ultralytics import YOLO
from roboflow import Roboflow


if __name__ == '__main__':
    rf = Roboflow(api_key="apikey")

    project = rf.workspace("ms-xprmw").project("momentree-kitchen")
    version = project.version(3)
    dataset = version.download("yolov8")
    # Load a model
    model = YOLO('yolov8m.pt')  # load a pretrained model (recommended for training)

    # Use the model
    results = model.train(
        data=f'{dataset.location}/data.yaml', 
        epochs=30,
        hsv_h=0,
        hsv_s=0,
        hsv_v=0,
        fliplr=0,
        erasing=0)  # train the model
    results = model.export(format='onnx')  # export the model to ONNX format
