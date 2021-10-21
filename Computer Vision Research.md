# Computer Vision Research

There are three primary object detection methods considered during deep learning-based object detection. 

- Faster R-CNNs [(Ren et al., 2015)](https://arxiv.org/pdf/1506.01497.pdf)
- You Only Look Once (YOLO) [(Redmon et al., 2015)](https://arxiv.org/pdf/1506.02640.pdf)
- Single Shot Detectors (SSDs) [(Liu et al., 2015)](https://arxiv.org/pdf/1512.02325.pdf)

Although R-CCNs are more popular, it's difficult to train and implement. It is also quite slow with a throughput at 7 FPS. 

YOLO is much faster with a performance up to 40-90 FPS on a Titan X GPU, worse on the TX2, however accuracy is an issue. 

SSDs, originally developed by Google, are a balance between the two with a 22-45 FPS throughput. 

Deploying an SSD-MobileNet V2 [(Howard et al., 2017)](https://arxiv.org/pdf/1704.04861.pdf) model on a 91 class COCO dataset* seemed to perform the best with sub-60 FPS speeds. To do so, we must first install [jetson-inference](https://github.com/dusty-nv/jetson-inference), a realtime DNN vision library for NVIDIA Jetson Nano/TX1/TX2/Xavier NX/AGX Xavier. 

```bash
$ cd ~
$ sudo apt-get update
$ git clone -- recursive https://github.com/dusty-nv/jetson-inference
$ cd jetson-inference
$ mkdir build && cd build
$ cmake ../
# Only select SSD-Mobilenet-v2, disregard the prompt asking you to install Pytorch.
$ make -j$(nproc)
$ sudo make install
$ sudo ldconfig
```

This should create two files `jetson_inference_python.so` and `jetson_utils_python.so` inside `/usr/lib/python3.6/dist-packages/jetson/`. 

Check installation:

```bash
$ python3
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import jetson.inference
>>> import jetson.utils
>>> 
# No NoModuleFound error indicates successful installation
```

> You can try running a test example using the `MobileNetSSDModule.py` file.

---

*`~/jetson-inference/data/networks/SSD-Mobilenet-v2/ssd_coco_labels.txt` contains the 91 class labels. Furthermore, the object detection model is in the same directory, it's the `.uff` file.   

Sources: 

- [github.com/dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference)
- [Object detection with deep learning and OpenCV](https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/)