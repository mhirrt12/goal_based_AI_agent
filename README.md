Here's the **ready-to-copy** content for your `README.md` file:


# 🏥 Hospital Bed Management Agent

A **goal‑based AI agent** that simulates intelligent bed allocation in a hospital.  
Patients are admitted based on medical priority (critical > serious > normal), automatically upgraded to ICU when beds free up, and visually animated in a Tkinter GUI.



## ✨ Features

- ✅ **Priority waiting queue** – uses a heap to always serve the most urgent patient first.
- ✅ **Automatic ICU upgrade** – critical patients in general beds move to ICU as soon as a bed is available.
- ✅ **Smooth animations** – patient boxes move between ICU, General, and Waiting areas without overlapping.
- ✅ **Discharge handling** – frees beds and reallocates waiting patients automatically.
- ✅ **Duplicate name prevention** – alerts if a patient name already exists.
- ✅ **Real‑time status display** – shows available beds and current allocations.
- ✅ **Clean, professional UI** – light blue/white background with black text.



## 🧠 Why This Is a Goal‑Based AI Agent

The system continuously:

- **Perceives** – knows how many ICU/general beds are free, which patients are where, and who is waiting.
- **Has a goal** – *“Place every patient in the most appropriate bed according to priority, and ensure critical patients eventually get ICU beds.”*
- **Acts deliberately** – after every admission or discharge, it runs a reassignment process that:
  1. Upgrades critical patients from general to ICU if possible.
  2. Allocates waiting patients to freed beds in priority order.
- **Improves the state** – moves patients only when it brings the system closer to the goal.

This is exactly the definition of a **goal‑based agent** in AI (Russell & Norvig) – it makes decisions based on how its actions will affect future goal satisfaction.

## 📁 Project Structure


HospitalBedAgentProject/
│
├── agents/
│   ├── __init__.py
│   ├── patient.py          # Patient class with priority
│   └── hospital_agent.py   # Core logic (allocation, queue, upgrades)
│
└── ui/
    └── main_ui.py          # Tkinter GUI with animation



## 🚀 Installation & Running

### Prerequisites
- Python 3.6 or higher (Tkinter is included in the standard library)

### Steps
1. **Clone or download** this repository.
2. **Navigate** to the project folder:
   ```bash
   cd HospitalBedAgentProject
   ```
3. **Run the application**:
   ```bash
   python -m ui.main_ui
   ```


## 🎮 How to Use

### Admit a Patient
1. Enter the patient’s name.
2. Select the condition: **Critical**, **Serious**, or **Normal**.
3. Click **Admit**.
   - The system will place the patient in an ICU bed (if critical and free), a general bed (if available), or add them to the waiting queue (if no beds).
   - A colored box appears and animates to the correct location.

### Discharge a Patient
1. Enter the patient’s name.
2. Click **Discharge**.
   - The patient is removed from the bed or waiting queue.
   - The freed bed triggers reassignment: upgrades first, then allocates waiting patients.
   - Boxes animate to their new positions.

### Monitor Status
- The left panel shows **available beds** and a **text list** of all allocated and waiting patients.
- The right canvas provides a **visual overview**:  
  - 🔴 Red = Critical  
  - 🟠 Orange = Serious  
  - 🔵 Blue = Normal  


## ⚙️ How It Works Internally

1. **Patient arrival** – `admit_patient()` tries to allocate a bed using `_try_allocate()`. If none free, the patient is pushed into a **priority heap** (critical first).
2. **Discharge** – `discharge_patient()` removes the patient and frees a bed.
3. **Reassessment** – After any change, `reassign_beds()` is called:
   - **Upgrade** – critical patients in general beds move to ICU if an ICU bed is free.
   - **Allocate** – waiting patients are popped from the heap and assigned to freed beds until no more beds or no suitable patients remain.
4. **Animation** – The canvas computes target positions for all patient boxes and moves them gradually for a smooth effect.

All data structures are kept consistent, and the heap ensures O(log n) priority operations.


## 🛠️ Technologies Used

- **Python 3** – core language.
- **Tkinter** – GUI (standard library).
- **Heapq** – priority queue implementation.
- **Object‑oriented design** – clean separation of agent logic and UI.



## 📈 Possible Future Enhancements

- Add patient age or other factors to priority.
- Logging and history of admissions/discharges.
- Multiple wards or departments.
- Predictive analytics for bed demand (using ML).
- Network version for multi‑user access.



## 📄 License

This project is open source and available under the [MIT License](LICENSE).


## 🙏 Acknowledgements

Inspired by real‑world hospital bed management challenges and the goal‑based agent model from artificial intelligence.  
Built with ❤️ for learning and simulation.


