📝 Keylogger (Windows — LAB Version)
For cybersecurity education & training only

The Keylogger (LAB Version) is a Python-based educational tool that records keystrokes on the system where it is manually executed. It is used only for demonstrating keylogging concepts in cybersecurity labs.

🚀 Features

Captures and logs keystrokes

Automatically saves logs to output.txt

Stops logging when the program is closed

Lightweight & simple — no stealth or autorun (ethical version)

🧠 How It Works (Logic Flow)
1. Run the keylogger script manually
2. The script monitors keyboard events
3. Each key pressed is recorded and saved in a text file
4. When the script is closed, logging ends automatically

📌 How to Run

Install Python and pynput library

pip install pynput


Open terminal in the project folder

Run the script:

python keylogger.py


Logs will be saved automatically in output.txt in the same folder

📁 Folder Structure
Keylogger_LAB/
 ├── keylogger.py
 ├── keystrokes_log.csv (generated after running)
 └── README.md

🧪 How to Test
Action	What happens
Run script	Logging starts
Type something in any window	Keys recorded
Close terminal / stop script	Logging stops
Open output.txt	All captured keys visible
⚠ Ethical Use Notice

This is a LAB-ONLY cybersecurity training tool.
You may use it ONLY on systems you own or have explicit permission to test.

Misuse for spying or unauthorized monitoring is illegal and strictly discouraged.

👨‍💻 Developer

Created by: Mersilin Princy M
Cybersecurity Intern — 2025
