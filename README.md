
# Smart Store
## A project, in the course 1DT305 - Applied IoT

Name: David Mozart Andraws<br/>
Email: <dm222is@student.lnu.se><br/>
University: [Linnaeus University](https://lnu.se/)<br/>
PowerPoint: [Smart-Store](https://1drv.ms/p/s!AsqxEF09_XshkM1n4i1At7rL_whUDQ?e=use26k)<br/>

<p float="left">
    <img src="https://pycom.io/wp-content/uploads/2018/08/pycomLogoGoInventGrey1920.png" alt="alt text" width="110px" height="auto">
    <img src="https://hitconsultant.net/wp-content/uploads/2018/09/CareCloud-Google.png" alt="alt text" width="110px" height="auto">
    <img src="https://www.connectedfinland.fi/wp-content/uploads/2017/10/Sigfox-Logo.png" alt="alt text" width="110px" height="auto">
    <img src="https://ubidots.com/_nuxt/img/logo_color.9c7e99e.png" alt="alt text" width="110x" height="auto">
</p>
 
---
## Overview
Smart Store is a project that aims towards smartifying department stores, by monitoring air conditions and customer behaviour, of course while respecting their integrity. The smart store device can be installed in a number of sections in the store and once installed, data about air conditions and customer movement activity will be transmitted to the sigfox network and further on to ubidots and google cloud for real-time visualisation.

Estimated time: 60h

---
**Table of Contents**
- [Smart Store](#smart-store)
  - [A project, in the course 1DT305 - Applied IoT](#a-project-in-the-course-1dt305---applied-iot)
  - [Overview](#overview)
  - [Objective](#objective)
  - [Material](#material)
    - [Hardware](#hardware)
    - [Software](#software)
  - [Computer setup](#computer-setup)
  - [Putting everything together](#putting-everything-together)
  - [Platform](#platform)
    - [Sigfox backend](#sigfox-backend)
    - [Google Cloud](#google-cloud)
    - [Ubidots](#ubidots)
  - [The Code](#the-code)
  - [Transmitting the data / connectivity](#transmitting-the-data--connectivity)
  - [Presenting the data](#presenting-the-data)
    - [Ubidots](#ubidots-1)
    - [Google Cloud - Data Studio](#google-cloud---data-studio)
  - [Finalizing the design](#finalizing-the-design)
    - [Final thoughts](#final-thoughts)
    - [Data studio (Live data)](#data-studio-live-data)
    - [Ubidots (Live data)](#ubidots-live-data)




---

## Objective


- [X] ***Why you chose the project***
I chose this specific project because it provides valueable information to a low cost. It also adds one more variable to consider when developing sales strategies.
I also chose to make something unique, that can't be found on a single tutorial online.   

- [X] ***What purpose does it serve***
It helps the store owner / manager to monitor air conditions in each section of the store. This information is useful both for customer well-being and air sensitive store section such as fruit and vegtable, dairy, furniture, clothing and painting sections.    
It also reports movement activities for x period of time, which can be helpful to learn and develop item promotion / sales techinques based on customer behaviour.
E.g. If section B is low on activity, that could mean that items in that section aren't exposed enough to the customer and by looking at how other sections, with more activity, are structured. One, of many possible measures, would be to mimic the structure in section B.

- [X] ***What insights you think it will give***
It will give an insight into how commercial and retail IOT systems are built. I will learn how to work with gathered data and use it for different purposes.

## Material

### Hardware
| Component                    | Task             | Price  | Link
| -----------------------------| ---------------- |--------|---
| LoPy4, exp-board & antenna   | To power sensors and communicate with the sigfox backend          | ~€60   | [here](https://pycom.io/product/lopy4-multipack)
| Breadboard      | To help us connect our sensors to the lopy4 | ~€7 | [here](https://www.kjell.com/se/produkter/el-verktyg/arduino/arduino-kit/luxorparts-basic-start-kit-for-arduino-p90632)
| BME680 Air Quality Sensor      | Monitor Air Conditions | ~€28 | [here](https://www.electrokit.com/produkt/bme680-monterad-pa-kort)
| HC-SR501 PIR Movement Detection      | To help us connect our sensors to the lopy4 | ~€5 | [here](https://www.electrokit.com/produkt/pir-rorelsedetektor-hc-sr501/)
| Resistor bundle with 1 Resistor 220 Ohms 1%      | To power our led when movement is detected (Mostly for debugging purposes, thus not really necessary) | ~€12 | [here](https://www.kjell.com/se/produkter/el-verktyg/elektronik/komponentsatser/playknowlogy-sortiment-med-resistorer-600-pack-p90646)


### Software
| IoT Thing | Link   |
| --------- | ----------- |
| Sigfox-backend Account   | [Here](https://support.sigfox.com/docs/backend-user-account-creation)          |
| Ubidots account      | [Here](https://industrial.ubidots.com/accounts/signup_industrial/)  |
| Google Cloud console      | [Here](https://console.cloud.google.com)  |
| Google Cloud functions    | [Here](https://cloud.google.com/functions)  |
| Google Cloud pubsub       | [Here](https://cloud.google.com/pubsub)  |
| Google Cloud bigquery     | [Here](https://cloud.google.com/bigquery)  |



## Computer setup

- [X] ***Chosen IDE***
    Atom

- [X] ***How the code is uploaded***
    From Atom with the PyMakr-plugin though a micro usb cable connected to the lopy4 expantion board

- [X] ***Steps that you needed to do for your computer. Installation of Node.js, extra drivers, etc.***
1. Update device firmware, more about that [here](https://docs.pycom.io/gettingstarted/installation/firmwaretool).
2. Create a project folder and open it with atom.
3. Upload some example code e.g. [RGB LED](https://docs.pycom.io/tutorials/basic/rgbled/) to test connectivity


## Putting everything together

- [X] ***Circuit diagram (can be hand drawn)***

![Circuit](https://i.imgur.com/BTJlePO.jpg)
**For high resolution, see [this](https://cdn.discordapp.com/attachments/670333245816045580/740637625995624589/IMG_20200805_202857.jpg)**

![Circruit_2](https://github.com/dmasb/Smart-Store/blob/master/circuit.png?raw=true)
Circuit created with https://www.circuit-diagram.org/


- [X] ****Electrical calculations***

N/A, see the Transmitting the data / connectivity section. Also, no sensor had an output larger than 3.3V, so no voltage devider was needed (lopy4 input pins only tolerate up to 3.3V as input).

**Possible improvements**
1. Keep wifi disabled - Saves 12mA
2. Remove the LED that the pir triggers - Saves ~20mA

This leaves:
1. Pir - 65mA
2. BME680 ~13mA (once/h, else ~0.15µA in sleep-mode)

So a 1200mAh battery would not be able to power this device more than ~2-3 weeks with the led removed and wifi disabled.


## Platform
The platform of choice is cloud-based, to keep it as serverless as possible.

### Sigfox backend
Used to receive data transmitted by the IOT device over their IOT network. Transmitted data looks like this:

![Img](https://i.imgur.com/XiO2tSU.png)

The uplink payload is sent and represented in hexadecimal format. It is also limited to 12 bytes for uplink, e.g your data to sigfox can at max be 12 bytes, and to 8 bytes for downlink, excluding header size in both cases. Sigfox allows for a maximum of 120 uplink messages o be transmitted per day and 4 downlink messages per day. [Read more](https://build.sigfox.com/technical-quickstart#uplink-downlink-messages).

More on how to connect your device to sigfox can be found [here](https://docs.pycom.io/tutorials/networks/sigfox/).
### Google Cloud
Used to get the payload (data) from sigfox, store it in a database and visiualize the data. The configuration is as following:
1. Create a Pub/Sub topic in the google cloud platform
2. Implement a callback function in sigfox to forward the data received by the device to google cloud platform.
3. Implement a callback function in google cloud platform to receive the sigfox data (this callback function will public the data to the Pub/Sub topic)
4. Create a callback function to decode the payload (data) and store it in bigquery

Refer to the following [tutorial](https://cloud.google.com/community/tutorials/sigfox-gw) for more detailed instructions

In a nutshell, the image below shows how everything is assembled together. (Ignore title in the first box and the title in the third box where it says Sens'it V3 Data Backend, the infrastructure can be used for any device, assuming the developer handles the decoding of the payload in the cloud function. the image is just to illustrate the infrastructure).
![pic](https://storage.googleapis.com/gcp-community/tutorials/sigfox-sensit/architecture.svg)

### Ubidots
Used to visualize the data in a few easy steps. This is how:
1. Create a ubidots account
2. Create an ubifunction in your ubidots account
3. Create a sigfox callback to ubidots in the sigfox-backend.
4. Request a downlink from ubidots (At this point, your device is created)
5. Create variables in ubidots
6. Create a dashboard in ubidots choosing the variables created in the previous steps.

Refer to the following [tutorial](https://help.ubidots.com/en/articles/924209-setup-your-sigfox-callback-to-talk-with-ubidots-cloud) for more detailed instructions


- [X] ***Explain and elaborate what made you choose this platform***

To quickly visualize my data, i chose to go with the **Sigfox**+**ubidots** configuration as it requires fewer steps and less time.

Once done, i began exploring other cloud platforms and chose to go with **Google Cloud** since it seemed to offer a large number of functionalies, including database solutions.


## The Code

This is how main.py looks like. The complete repository can be found in my github repository [here](https://github.com/dmasb/Smart-Store). (Exluded it for convenience)


```python

import time
import _thread
from lib.bme import BME
import struct
from lib.pir import PIR
from network import Sigfox
import socket

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink (Disabled downlink for now)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# PIR (Output to pin 13 (G5))
pir = PIR('G5')

"""
The run_pir() basically runs the sensor and keeps track of how
many time the sensor is triggered by incrementing a variable by 1.
This variable is set back to 0 each time the get_count_last_h() method is called.
This way, each time get_count_last_h() is called, it will return the number of
detections since last time this method was called.
"""
_thread.start_new_thread(pir.run_pir, ())

# BME680 (Output to Pin 9 and 10 (G16 and G17))
bme = BME(('P9', 'P10'))

while True:
    # Get the movement count since last time (Currently once / hour)
    count_last_hour = pir.get_count_last_h()

    # Get air condition values
    temp, humidity, pressure, air_quality = bme.get_values()

    # Print all
    print(temp, humidity, pressure, air_quality, count_last_hour)


    """
    Prepare the data by packing it before sending it to sigfox
    Payload format is: >bb BB HHHH HHHH HHHH where
    b = Temperature         (1 byte,  8 bits,  signed)       Range: -128 to 127
    B = Humidity            (1 byte,  8 bits,  unsigned)     Range: 0 to 255
    H = Pressure            (2 bytes, 16 bits, unsigned)     Range: 0 to 65,535
    H = Air Quality         (2 bytes, 16 bits, unsigned)     Range: 0 to 65,535
    H = Movement last hour  (2 bytes, 16 bits, unsigned)     Range: 0 to 65,535
    """
    package = struct.pack('>bBHBI',
                            int(temp),
                            int(humidity),
                            int(pressure),
                            int(air_quality),
                            int(count_last_hour))

    # Send the data to sigfox backend
    s.send(package)

    """
    Sleep for 60 minutes
    Pir is running on its own thread, and continues to do so while
    this thread sleeps.
    """
    time.sleep(3600)
```



## Transmitting the data / connectivity

How is the data transmitted to the internet? Describe the package format. All the different steps that are needed in getting the data to your end point. Explain both the code and choice of wireless protocols


- [X] ***How often is the data sent?***
* Once per hour

- [X] ***Which wireless protocols did you use (WiFi, LoRa, etc ...)?***
* Sigfox Radio Network

- [X] ***Which transport protocols were used (MQTT, webhook, etc ...)***
* Sigfox - Ubidots: HTTP
* Sigfox - Google Cloud: HTTP

- [X] ****Explain how much data is sent every day.***

The Device transmitts data to Sigfox-backend every hour, which is 24 times per 24h.
Each payload carries several sensor values and consists of a total of 8 bytes

The payload hexadecimal schema is: ***TTHHPPPPAAAAMMMM***, where each character represents 1 byte, see table below.

| Value           | Bytes            | Range        | Needed            |
|-----------------|------------------|--------------|-------------------|
| Temperature (T) | 1 byte, signed   | -128 to 127  | -40 to 85 (°C)    |
| Humidity (H)    | 1 byte, unsigned | 0 to 255     | 0 to 100  (% r.H.)|
| Pressure (H)    | 2 bytes, unsigned| 0 to 65,535  | 300 to 1100 (hPa) |
| Air Quality (A) | 2 bytes, unsigned| 0 to 65,535  | 0 to 500 (IAQ)    |
| Movement (M)    | 2 bytes, unsigned| 0 to 65,535  | 0 to 600 (detections / h MAX)  |

The size of each field is chosen with consultation from the component datasheet.

So in total, there are 8 bytes being trasmitted from the device every hour, excluding the datapacket header size. The effective payload size, exluding header size, each day is 8x24 = 192 bytes.

Example: The device sends the following data: 1b2803f1006300dc
Temperature: 0x1b = 27 in decimal
Humidity: 0x28 = 40 in decimal
Pressure: 0x03f1 = 1009 in decimal
Air Quality: 0x0063 = 99 in decimal
Movement: 0x00dc = 220 in decimal

It is also possible to further encode the data but shrinking it with a factor, but at the cost of losing resolution.

For uplink messages, sigfox has pre-defined payload lengths of 1, 4, 8 and 12 bytes. If the data being sent is 5 bytes, then 3 additional bytes of padding are added to the payload, to "fill the free space". This device has support for 5 additional bytes that could be used if upgraded with additional sensors in the future.

****Elaborate on the designb choices. That is how your choices affect the device range and battery consumption***
For these type of devices, that never sleeps, power consumption is high, as they actively listen for input. Therefore, I decided to just power it with a 5V micro-usb.

## Presenting the data

- [X] ***Provide visual examples on how the dashboard looks. Pictures needed.***
### Ubidots
![ubidots-dashboard](https://i.imgur.com/3EMUdJ3.png)

### Google Cloud - Data Studio
![glcloud-dashboard](https://i.imgur.com/uXGgQw7.png)

- [X] ***How often is data saved in the database***

The data transmitted by the device every hour is saved in a bigQuery table forever, e.g. no expiry date. This could be set up, if needed.

- [X] ****Explain your choice of database.***

I chose bigQuery as it is designed to scale and stream data analytics in real-time and because it is serverless. It is also fast and provides an option to share stored data to other applications, e.g. to the A.I platform or to grafana (via the BigQuery-plugin) to visualize the data.  
It is free of charge for the first 1TB of data processed each month. Stream-inserts (When our callback receives the data from sigfox-backend, decode it and insert it to bigquery) costs $0.01 per 200MB, which is very cheap.

This means that years/months/days old data can be reviewed and compared to current data or simply data from 2 date intervals can compared together.

- [X] ****Automation/triggers of the data***

**Sigfox**:
* Callback 1 (UPLINK) - Once sigfox-backend receives a message from the device, a callback function is triggered and forwards the data to ubidots.
* Callback 2 (BIDIR) - Once sigfox-backend receives a message from the device, a callback function is triggered and forwards the data to google cloud.

![sigfox-cb](https://i.imgur.com/0IOaFlf.png)
The service callbacks are triggered when downlink is activated (ack = true in the uplink message).

**Ubitdots**
* Receives and decode the payload and store the values in the created variables

![ubidots-cb](https://i.imgur.com/AYaLyFS.png)

**Google Cloud**
* Callback-data - Receives the data from the sigfox-backend callback and pushes the data to the Pub/Sub topic.
* pubsub-iot-decode - Is triggered when the Pub/Sub topic received new data and fetches it, decodes it and inserts the different values in a BigQuery table.

![gcloud-cb](https://i.imgur.com/1VYGARN.png)

## Finalizing the design

### Final thoughts
This couse was very educational, with a balanced mix of theory and experiential learning. The lectures were interactive and there were a decent number of workshops with skilled and helpful teaching assistants.

This project gave me a clearer insight into commercial systems are created. It also revealed some hidden aspects that has to be dealt with when developing such systems, e.g. minimize payload, minimize power consumption, maximize reliability & usability and following IOT-standards by using recommended transport protocols, such as MQTT etc..

While there is only one device presented in this project, the main idea is to have several devices monitoring a store section each. That is easily done by just connecting more devices to Sigfox-backend using existing callbacks.


- [X] ***Show final results of the project***
![final-product](https://i.imgur.com/3LCmxLW.jpg)
### Data studio (Live data)
<iframe width="100%" height="560" src="https://datastudio.google.com/embed/reporting/890679cc-8c9b-41a2-86bc-a259c4816f88/page/Bi5aB" frameborder="0" style="border:0" allowfullscreen></iframe>

[Link to Data Studio Dashboard](https://datastudio.google.com/reporting/890679cc-8c9b-41a2-86bc-a259c4816f88/page/Bi5aB)

### Ubidots (Live data)
<iframe width="100%" height="560" frameborder="0" src="https://industrial.ubidots.com/app/dashboards/public/dashboard/svFhUSFSp9YXCyCJRBzL9zPnMeI?embed=true"></iframe>
...

![sms](https://cdn.discordapp.com/attachments/670333245816045580/740982065625038858/Screenshot_20200806_191741_com.google.android.apps.messaging.jpg)

---
