# 🖐️ Virtual Gesture Control 🎬⌨️  
Control YouTube & Spotify Give commands without touch– Just Use Your Hands!

A real-time computer vision project that allows users to **control YouTube videos** and **Spotify**using only **hand gestures**, leveraging your webcam.  
Built using **Python 3.10**, **OpenCV**, and **MediaPipe**.

---

## 📸 Demo Preview
![alt text](<Screenshot 2025-06-15 172403.png>)
![alt text](<Screenshot 2025-06-15 173453.png>)



> 🎥 Control volume with Zoom gestures, play/pause with taps, switch videos with thumbs up/down, and type using an on-screen keyboard — all with your hands!



---

## 🛠️ Technologies Used

| Library          | Purpose                                      |
|------------------|----------------------------------------------|
| `OpenCV`         | Real-time video capture & drawing            |
| `MediaPipe`      | Hand landmark tracking (by Google)           |
| `PyAutoGUI`      | Simulating keypresses and mouse events       |
| `TensorFlow`     | (Optional) for enhancing gesture classification |
✅ **Tested on Python 3.10.10**

---

## 🎯 Features

- 🎬 **YouTube Gesture Control**  
  - 👎 Thumbs Down → Previous Video  
  - 👍 Thumbs Up → Next Video  
  - 🤏 Zoom In/Out → Volume Up/Down  
  - 👉 Tap Gesture → Play / Pause  

- ⌨️ **Virtual Keyboard**  
  - Track index finger to press keys  
  - Detect fingertip hovering and simulate key input  
  - Draws responsive keyboard UI in real-time

- 🎥 **Live Camera Feed**  
  - Displays hand landmarks and gesture feedback  
  - Shows FPS and instructions on screen by using Time libraries (You can gesture_detection.py code for that!)

---

## 🧱 Project Structure
Virtual Gesture Control/
│
├── main.py                  # Entry script for keyboard + gesture controller
├── hand_tracking.py         # Hand tracking utility (via MediaPipe)
│
├── Utils/                   # Utility modules
│   ├── calibration.py       # Hand tracking calibration (if used)
│   ├── gesture_detection.py # Core gesture logic
│   ├── virtual_keyboard.py  # Keyboard layout and keypress detection
│   └── yt_gesture_control.py# YouTube control with hand gestures
│
├── .venv/                   # Virtual environment (excluded via .gitignore)
├── __pycache__/             # Compiled Python cache files (ignored)
│
├── requirements.txt         # Project dependencies
├── README.md                # Project overview and documentation
├── .gitignore               # Files/folders excluded from Git
├── LICENSE                  # License file
│
├── SS1.png                  # Screenshot 1 (project demo)
└── SS2.png                  # Screenshot 2 (project demo)


yaml
Copy
Edit

---

## 🧑‍💻 How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/virtual-gesture-control.git
cd virtual-gesture-control
2. Create Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv .venv
source .venv/Scripts/activate  # On Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Project
bash
Copy
Edit
python main.py
✅ Ensure your webcam is connected and working.

📝 Instructions
Make sure you're in a well-lit environment.

Keep your hand within the camera frame.

Try the following:

👈 Tap Gesture → Play / Pause

👍 Thumbs Up → Next

👎 Thumbs Down → Previous

🤏 Zoom In / Out → Volume Control

☝️ Point and hover over keys to type


📦 Dependencies
txt
Copy
Edit
opencv-python
mediapipe
pyautogui
tensorflow  # Optional
Add these to requirements.txt for easy setup.


💡 Future Enhancements
Add voice command fallback

Customizable keyboard layouts

Gesture training with ML models

Browser-independent video control (via Selenium or JS injection)


🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📜 License
This project is licensed under the MIT License.

🙌 Acknowledgements
MediaPipe by Google

OpenCV

PyAutoGUI

🚀 Built with ❤️ by [Your Name] – Let your hands do the talking!
yaml
Copy
Edit

---

### ✅ BONUS: `requirements.txt` (If you don’t have one yet)

```txt
opencv-python
mediapipe
pyautogui
tensorflow


