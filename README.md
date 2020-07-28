# Python-SmartTraffic 
©KevinYobeth
## Description
A simple python script that scans the traffic and return the best green light duration for the selected scene. You can custom create the scene using the sceneGenerator.psd or using the clean plate given. Use the color red (#eb4343, 235, 67, 67) for car, blue (#50a3e9, 80, 163, 223) for motorcycle and green (#69e850, 105, 232, 80)

## Requirements
- Computer Vision 2 (pip install opencv-python)
- Scipy (pip install scipy)
- Imutils (pip install imutils)

To run the script, use the code
```python
py smartTraffic.py --i [sceneName].jpg
```

## Screenshot
![Screenshot of Working App](/screenshot/1.png)

## How this works
The technology behind this is computer vision. We use computer vision (cv) to scan the scene and recognize the vehicle defined as a colored shape. The color red for car, green for truck and blue for motorcycle. By splitting it into 4 sections, we can get the total vehicle from the left, top, right and the bottom side of the road. We than calculate the value of each section by multiplying motorcycle with a value of 1, car with a value of 3 and truck, 4. For each section, we divide the value of it with the total value of all section and multiplying it with the cycle time (default 120 s)
