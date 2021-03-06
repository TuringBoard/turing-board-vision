# Computer Vision Research

There are three primary object detection methods considered during deep learning-based object detection. 

- Faster R-CNNs [(Ren et al., 2015)](https://arxiv.org/pdf/1506.01497.pdf)
- You Only Look Once (YOLO) [(Redmon et al., 2015)](https://arxiv.org/pdf/1506.02640.pdf)
- Single Shot Detectors (SSDs) [(Liu et al., 2015)](https://arxiv.org/pdf/1512.02325.pdf)

Although R-CCNs are more popular, it's difficult to train and implement. It is also quite slow with a throughput at 7 FPS. 

YOLO is much faster with a performance up to 40-90 FPS on a Titan X GPU, worse on the TX2, however accuracy is an issue. 

SSDs, originally developed by Google, are a balance between the two with a 22-45 FPS throughput. 

Deploying an SSD-MobileNet V2 [(Howard et al., 2017)](https://arxiv.org/pdf/1704.04861.pdf) model on a 91 class COCO dataset<sup>[1]</sup> seemed to perform the best with sub-60 FPS speeds. To do so, we must first install [jetson-inference](https://github.com/dusty-nv/jetson-inference), a realtime DNN vision library for NVIDIA Jetson Nano/TX1/TX2/Xavier NX/AGX Xavier. 

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
# Absence of NoModuleFound error indicates successful installation
```

> You can try running a test example using the `MobileNetSSDModule.py` file.

---

### Pathfinding for the Summon feature

> 10:05 PM, Sun Oct 24, 2021

Board generates a trapezoidal trajectory map infront of it with a progressive width equal to its own width plus some padding width, if object detected within the trajectory, avoid object. 

The path finding algorithm may draw inspiration from many existing projects. For example, the [Starship](https://www.starship.xyz/) autonomous delivery vehicle employs it's own flavor of autonomous driving on non-road paths. Here are some videos of some employees of this company talking about the software behind their product: 

- Time: 13:25 - 18:34 [Kristjan Korjus (Starship Technologies) KEYNOTE: Building Smart and Reliable Self-Driving Robots](https://youtu.be/u1awz4Auj-c?t=805)
- Time: 5:00 - 34:40 [Ahti Heinla, Starship: "Building self-driving delivery robots"](https://www.youtube.com/watch?v=aM9-bRGbmPQ?t=300)

> 8:30 PM, Wed Nov 3, 2021

Adding slides related to path finding from CSE 4360 - Robotics, Manfred Huber. See folder `/PathFindingSlides`.

---

##### Sources: 

- [github.com/dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference)
- [Object detection with deep learning and OpenCV](https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/)

---

<sup>[1]</sup> `~/jetson-inference/data/networks/SSD-Mobilenet-v2/ssd_coco_labels.txt` contains the 91 class labels. Furthermore, the object detection model is in the same directory, it's the `.uff` file.   
