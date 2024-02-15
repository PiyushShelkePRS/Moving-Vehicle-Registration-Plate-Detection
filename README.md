# Moving Vehicle Registration Plate Detection

This project aims to detect and recognize license plates on moving vehicles using computer vision techniques.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

The ability to detect and recognize license plates on moving vehicles has numerous applications including traffic monitoring, law enforcement, toll collection, and parking management. 
This project utilizes computer vision algorithms to identify license plates from video streams captured by cameras installed on roads, highways, or any surveillance system.

## Installation

Here are the steps to use the project:

1. Run the Python server:
   Execute the following command in your terminal/PyCharm/VScode to start the Python server:
   python server.py
   This command will start a server that will handle communication between the camera and the client.
2. Run the camera script:
   Launch the camera script using the following command:
   python camera.py
   This script will access the camera feed and stream it to the server.
3. Access the link provided by the server:
   After running both server.py and camera.py, the server will provide a link. Copy and paste this link into your web browser. This link will typically be in the format of http://localhost:<port_number>.
   It will allow you to view the live camera feed from the camera.py script.
5. View the live camera feed:
   Once you've accessed the link provided by the server, you should see the live camera feed
   being streamed from the camera. This feed may include moving vehicles with their license
   plates.
6. Perform license plate detection :
   IProject includes license plate detection, you may need to interact with the camera feed to initiate the detection process. Follow any prompts or instructions provided by the interface to perform license plate detection on the live video stream.
7. Interact with the detected license plates:
Depending on the functionality of your project, you may be able to interact with the detected license plates in various ways. This could include retrieving information about the vehicles, storing license plate data in a database, or triggering alerts for specific events.

These steps outline the basic process for using the project. Depending on the specific implementation and features of your project, there may be additional steps or variations to consider.
   





