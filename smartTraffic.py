from pyEngine.ColorLabeler import ColorLabeler
from config import *
import argparse
import imutils
import cv2


def greenLight(roadSide, image, x, y, total):

    if (roadSide == 'b'):
        text = str(5 + round((bottomRoad["value"] / total) * cycleTime))
    elif (roadSide == 't'):
        text = str(5 + round((topRoad["value"] / total) * cycleTime))
    elif (roadSide == 'l'):
        text = str(5 + round((leftRoad["value"] / total) * cycleTime))
    elif (roadSide == 'r'):
        text = str(5 + round((rightRoad["value"] / total) * cycleTime))

    cv2.putText(image, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (45, 234, 112), 2)
    cv2.imshow("Image", image)


def redLight(roadSide, image, x, y, total):

    if (roadSide == 'b'):
        text = str(
            cycleTime + 5 - (round(bottomRoad["value"] / total * cycleTime)))
    elif (roadSide == 't'):
        text = str(cycleTime + 5 -
                   (round(topRoad["value"] / total * cycleTime)))
    elif (roadSide == 'l'):
        text = str(cycleTime + 5 -
                   (round(leftRoad["value"] / total * cycleTime)))
    elif (roadSide == 'r'):
        text = str(cycleTime + 5 -
                   (round(rightRoad["value"] / total * cycleTime)))

    cv2.putText(image, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (59, 41, 239), 2)
    cv2.imshow("Image", image)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cl = ColorLabeler()


for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)

    color = cl.label(lab, c)

    if (color == 'road'):
        continue

    if (cX > rightRoad["x1"] and cX < rightRoad["x2"]):
        if (cY > rightRoad["y1"] and cY < rightRoad["y2"]):
            if (color == 'Mobil'):
                rightRoad["Vehicle"]["Car"] += 1
            elif (color == 'Truk'):
                rightRoad["Vehicle"]["Truck"] += 1
            elif (color == 'Motor'):
                rightRoad["Vehicle"]["Motorcycle"] += 1
            totalVehicle += 1

    if (cX > topRoad["x1"] and cX < topRoad["x2"]):
        if (cY > topRoad["y1"] and cY < topRoad["y2"]):
            if (color == 'Mobil'):
                topRoad["Vehicle"]["Car"] += 1
            elif (color == 'Truk'):
                topRoad["Vehicle"]["Truck"] += 1
            elif (color == 'Motor'):
                topRoad["Vehicle"]["Motorcycle"] += 1
            totalVehicle += 1

    if (cX > leftRoad["x1"] and cX < leftRoad["x2"]):
        if (cY > leftRoad["y1"] and cY < leftRoad["y2"]):
            if (color == 'Mobil'):
                leftRoad["Vehicle"]["Car"] += 1
            elif (color == 'Truk'):
                leftRoad["Vehicle"]["Truck"] += 1
            elif (color == 'Motor'):
                leftRoad["Vehicle"]["Motorcycle"] += 1
            totalVehicle += 1

    if (cX > bottomRoad["x1"] and cX < bottomRoad["x2"]):
        if (cY > bottomRoad["y1"] and cY < bottomRoad["y2"]):
            if (color == 'Mobil'):
                bottomRoad["Vehicle"]["Car"] += 1
            elif (color == 'Truk'):
                bottomRoad["Vehicle"]["Truck"] += 1
            elif (color == 'Motor'):
                bottomRoad["Vehicle"]["Motorcycle"] += 1
            totalVehicle += 1

    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    text = "{}".format(color)
    cv2.putText(image, text, (cX - 9, cY + 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Image", image)

rightRoad["value"] = (rightRoad["Vehicle"]["Motorcycle"] * motorcycleValue) + (rightRoad["Vehicle"]["Car"] *
                                                                               carValue) + (rightRoad["Vehicle"]["Truck"] * truckValue)

leftRoad["value"] = (leftRoad["Vehicle"]["Motorcycle"] * motorcycleValue) + (leftRoad["Vehicle"]["Car"] *
                                                                             carValue) + (leftRoad["Vehicle"]["Truck"] * truckValue)

topRoad["value"] = (topRoad["Vehicle"]["Motorcycle"] * motorcycleValue) + (topRoad["Vehicle"]["Car"] *
                                                                           carValue) + (topRoad["Vehicle"]["Truck"] * truckValue)

bottomRoad["value"] = (bottomRoad["Vehicle"]["Motorcycle"] * motorcycleValue) + (bottomRoad["Vehicle"]["Car"] *
                                                                                 carValue) + (bottomRoad["Vehicle"]["Truck"] * truckValue)

total = rightRoad["value"] + leftRoad["value"] + \
    topRoad["value"] + bottomRoad["value"]

greenLight("b", image, 335, 495, total)
greenLight("l", image, 328, 345, total)
greenLight("t", image, 430, 342, total)
greenLight("r", image, 475, 445, total)

redLight("b", image, 380, 495, total)
redLight("l", image, 328, 390, total)
redLight("t", image, 475, 342, total)
redLight("r", image, 475, 485, total)

print(totalVehicle)

print("rCar " + str(rightRoad["Vehicle"]["Car"]))
print("rTruck " + str(rightRoad["Vehicle"]["Truck"]))
print("rMotorcycle " + str(rightRoad["Vehicle"]["Motorcycle"]))
print("rValue " + str(rightRoad["value"]))
print("")

print("tCar " + str(topRoad["Vehicle"]["Car"]))
print("tTruck " + str(topRoad["Vehicle"]["Truck"]))
print("tMotorcycle " + str(topRoad["Vehicle"]["Motorcycle"]))
print("tValue " + str(topRoad["value"]))
print("")

print("lCar " + str(leftRoad["Vehicle"]["Car"]))
print("lTruck " + str(leftRoad["Vehicle"]["Truck"]))
print("lMotorcycle " + str(leftRoad["Vehicle"]["Motorcycle"]))
print("lValue " + str(leftRoad["value"]))
print("")

print("bCar " + str(bottomRoad["Vehicle"]["Car"]))
print("bTruck " + str(bottomRoad["Vehicle"]["Truck"]))
print("bMotorcycle " + str(bottomRoad["Vehicle"]["Motorcycle"]))
print("bValue " + str(bottomRoad["value"]))

cv2.waitKey(0)
