# 🚦 ATCC & ANPR Smart Traffic Management System

### Infosys Springboard Internship Project – Vidzai Digital

---

## 📌 Project Overview

The **Smart Traffic Management System** is an AI-powered solution that combines **Automatic Number Plate Recognition (ANPR)** and **Automatic Traffic Classification and Control (ATCC)** using **Deep Learning and Computer Vision**.

This project aims to automate traffic monitoring, vehicle detection, and traffic signal control in **real-time** using live camera feeds — improving road safety, reducing congestion, and enabling **smart city integration**.

---

## 🎯 Objectives

- Detect and recognize vehicle number plates in real-time.
- Classify vehicles (car, truck, bus, motorbike, etc.) from live camera footage.
- Dynamically adjust traffic signals based on traffic density.
- Integrate ANPR and ATCC modules for unified smart city traffic management.

---

## 🧩 Project Modules

### 1️⃣ ANPR (Automatic Number Plate Recognition)
- Detects number plates from live camera or video feed.  
- Uses **OpenCV + EasyOCR** for plate detection and character recognition.  
- Saves or displays recognized plate numbers in real-time.

### 2️⃣ ATCC (Automatic Traffic Classification and Control)
- Classifies vehicles using **YOLOv8 Deep Learning model**.  
- Counts vehicles and analyzes traffic density.  
- Suggests or automates traffic signal control dynamically.

### 3️⃣ Controller Integration
- Integrates ANPR + ATCC modules for unified operation.  
- Controls camera input, performs detection, and displays results together.

---

## ⚙️ Tech Stack

| Category | Technologies Used |
|-----------|-------------------|
| **Frontend** | React.js, HTML, CSS, JavaScript |
| **Backend (ANPR)** | Python, FastAPI, EasyOCR, OpenCV |
| **Backend (ATCC)** | Python, Flask, YOLOv8, Torch, OpenCV |
| **Real-time Control** | Python Scripts (`controller.py`, `anpr_demo.py`, `vehicle_demo.py`) |
| **Tools / Libraries** | NumPy, Pillow, Ultralytics, CORS, Uvicorn |

