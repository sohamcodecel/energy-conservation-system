# ⚡ Electricity Energy Conservation System

### Smart IoT-Based Electricity Monitoring and Conservation System

An intelligent electricity conservation system designed to reduce unnecessary power consumption in classrooms and other indoor environments using **computer vision, IoT, and real-time energy monitoring**.

The system monitors room occupancy through a camera and tracks the electricity consumption of connected appliances. When no one is present in the room, it identifies unnecessary electricity usage and alerts users to switch off appliances, helping prevent energy wastage.

---

## 🎯 Problem Statement

Electricity is frequently wasted in classrooms, laboratories, offices, and other public spaces because lights, fans, and other electrical appliances remain switched on even when nobody is present.

Traditional electrical systems rely on people to manually switch off appliances, which often leads to unnecessary energy consumption.

Our project aims to address this problem through an automated monitoring and alert mechanism.

## 💡 Our Solution

We developed an IoT-based electricity monitoring system that combines camera-based human detection with electrical parameter monitoring.

The system:

* Uses a camera and Python-based computer vision to detect and count people in a room.
* Monitors the electrical parameters of connected appliances.
* Tracks voltage, current, power consumption, and energy usage.
* Displays electricity consumption information through a monitoring dashboard.
* Identifies situations where appliances are running in an unoccupied room.
* Sends notifications or alerts to encourage users to switch off unnecessary appliances.

## ✨ Key Features

* **Human Detection:** Camera-based monitoring to identify room occupancy.
* **Real-Time Monitoring:** Tracks electrical parameters of connected appliances.
* **Energy Measurement:** Monitors power consumption in Watts (W) and energy consumption in kilowatt-hours (kWh).
* **Smart Alerts:** Identifies electricity wastage when appliances remain switched on in an empty room.
* **IoT Integration:** Uses NodeMCU ESP8266 for wireless communication.
* **Monitoring Dashboard:** Provides a centralized interface for viewing energy consumption data.
* **Energy Conservation:** Helps reduce unnecessary electricity usage and promotes responsible energy consumption.

## 🛠️ Technologies Used

| Technology                 | Purpose                                     |
| -------------------------- | ------------------------------------------- |
| Python                     | Computer vision and human detection         |
| OpenCV                     | Camera-based occupancy monitoring           |
| C++ / Embedded Programming | Microcontroller programming                 |
| NodeMCU ESP8266            | Wi-Fi-based IoT communication               |
| HTML, CSS, JavaScript      | Dashboard interface                         |
| IoT                        | Communication between monitoring components |

## 🔌 Hardware Components

| Component         | Function                                  |
| ----------------- | ----------------------------------------- |
| NodeMCU ESP8266   | Wireless communication and IoT control    |
| L298 Motor Driver | Motor control for the prototype           |
| DC Motor          | Demonstration of appliance control        |
| Camera            | Human detection and occupancy monitoring  |
| Voltage Sensor    | Voltage measurement                       |
| Current Sensor    | Current measurement                       |
| Computer / Laptop | Python execution and monitoring dashboard |

## ⚙️ How It Works

The system operates through the following workflow:

**1. Room Occupancy Detection**

A camera continuously captures the room environment. Python-based computer vision processes the camera feed to identify and count people present in the room.

**2. Electrical Parameter Monitoring**

Sensors connected to electrical appliances collect information about:

* Voltage (V)
* Current (A)
* Power (W)
* Energy Consumption (kWh)

**3. Wireless Data Transmission**

The NodeMCU ESP8266 facilitates wireless communication between the hardware components and the monitoring system.

**4. Occupancy and Energy Analysis**

The system compares room occupancy with the operating status and power consumption of connected appliances.

**5. Electricity Wastage Detection**

If the room is detected as empty while electrical appliances are still consuming power, the system identifies a potential electricity wastage situation.

**6. Alert and Monitoring**

The monitoring dashboard displays relevant energy information, and an alert is generated to notify users about unnecessary electricity consumption.

## 🏗️ System Architecture

```text
             CAMERA
                |
                v
       Python + OpenCV
                |
                v
       Human Detection
                |
                |
                v
        Occupancy Status
                |
                |
                v
Electrical Sensors ------> NodeMCU ESP8266
                |                 |
                |                 |
                v                 v
       Energy Monitoring    Wi-Fi Communication
                |                 |
                +--------+--------+
                         |
                         v
                Monitoring Dashboard
                         |
                         v
               Electricity Wastage
                    Detection
                         |
                         v
                   Smart Alerts
```

## 📂 Project Structure

```text
Electricity-Energy-Conservation-System/
│
├── python/
│   ├── detection.py
│   └── requirements.txt
│
├── hardware/
│   ├── nodemcu_code/
│   └── circuit_diagram/
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── images/
│   └── project-demo.png
│
├── README.md
└── LICENSE
```

*Note: Adjust the folder structure according to your actual repository files.*

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Visual Studio Code or another code editor
* NodeMCU ESP8266
* Camera or webcam
* Required electrical sensors
* Stable Wi-Fi connection

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

**2. Navigate to the project directory**

```bash
cd Electricity-Energy-Conservation-System
```

**3. Install Python dependencies**

```bash
pip install opencv-python
```

Install any additional dependencies required by your implementation.

**4. Configure the hardware**

* Connect the camera to the computer.
* Connect the electrical monitoring sensors to the microcontroller.
* Configure the NodeMCU ESP8266 Wi-Fi connection.
* Upload the appropriate microcontroller program.

**5. Run the Python application**

```bash
python python/detection.py
```

*The commands and configuration may need adjustment depending on your final implementation.*

## 🌍 Applications

This system can be implemented in:

* Educational institutions and classrooms.
* College laboratories.
* Corporate offices.
* Libraries and reading rooms.
* Conference rooms.
* Commercial buildings.
* Smart buildings and infrastructure.

## 🔮 Future Improvements

We aim to improve the system through:

* Automatic switching of electrical appliances based on occupancy.
* Integration of machine learning for more accurate human detection.
* Cloud-based energy monitoring and data storage.
* Historical electricity consumption analysis.
* Predictive energy consumption analytics.
* Mobile application integration.
* Multi-room electricity monitoring.
* Automated electricity consumption reports.

## 🌱 Impact

The project focuses on making electricity consumption smarter, more efficient, and more sustainable.

By combining computer vision and IoT, the system can help reduce avoidable electricity wastage, encourage energy-conscious behaviour, and contribute towards the development of smart and sustainable infrastructure.

## 👨‍💻 Project Contributors

Developed as an engineering project focused on IoT, automation, and sustainable energy management.

---

**If you find this project interesting, consider giving this repository a ⭐!**
