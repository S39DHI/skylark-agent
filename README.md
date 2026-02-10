# Skylark Drone Operations Coordinator Agent

A conversational AI system for managing drone operations, pilot assignments, and mission scheduling using a simple chat interface and a live Google Sheets backend.

The system allows operations managers to issue natural-language commands such as:

- “Who is available?”
- “Put Arjun on leave”
- “Assign someone to PRJ001”
- “Check conflicts”

All updates are reflected instantly in a shared Google Sheet, acting as a real-time operational database.

---

## Overview

This project is designed as a lightweight operational assistant for drone teams.  
It combines:

- A chat-based user interface
- A backend decision agent
- Live Google Sheets as the data source

The goal is to make mission coordination faster, simpler, and more intuitive without requiring complex enterprise systems.

---

## System Architecture

The system follows a **three-layer architecture**:

┌──────────────────────────────────────────────────────────┐
│                        USER                              │
│               Operations Coordinator                     │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                     FRONTEND                             │
│               Web Chat Interface                         │
│                                                          │
│  - Chat input                                            │
│  - Live pilot table                                      │
│  - Live drone table                                      │
│  - Live mission table                                    │
│                                                          │
│  Technologies: HTML, CSS, JavaScript                    │
└─────────────────────────┬────────────────────────────────┘
                          │ HTTP Requests
                          ▼
┌──────────────────────────────────────────────────────────┐
│                     BACKEND API                          │
│                     FastAPI (app.py)                     │
│                                                          │
│  Endpoints:                                              │
│   • /chat                                                │
│   • /pilots                                              │
│   • /drones                                              │
│   • /missions                                            │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                   DECISION AGENT                         │
│                      (agent.py)                          │
│                                                          │
│  Responsibilities:                                       │
│   • Interpret commands                                   │
│   • Match pilots to missions                             │
│   • Update pilot/drone status                            │
│   • Detect conflicts                                     │
│   • Handle urgent reassignments                          │
└─────────────────────────┬────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                GOOGLE SHEETS CONNECTOR                   │
│                     (sheets.py)                          │
│                                                          │
│  Functions:                                              │
│   • load_pilots()                                        │
│   • load_drones()                                        │
│   • load_missions()                                      │
│   • update_pilot_status()                                │
│   • update_drone_status()                                │
└─────────────────────────┬────────────────────────────────┘
                          │ Google Sheets API
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    GOOGLE SHEETS DB                      │
│                                                          │
│  Spreadsheet: Skylark Drone Database                    │
│                                                          │
│  Worksheets:                                             │
│   • Pilot_Roster                                         │
│   • Drone_Fleet                                          │
│   • Missions                                             │
└──────────────────────────────────────────────────────────┘



---

## Architecture Components

### 1. Frontend (User Interface)

**Technology:**  
- HTML
- CSS
- JavaScript

**Responsibilities:**
- Provide a chat interface for commands
- Display live operational tables:
  - Pilots
  - Drones
  - Missions
- Send commands to the backend
- Refresh data after each action

---

### 2. Backend (FastAPI Server)

**Technology:**  
- Python
- FastAPI
- Uvicorn

**Responsibilities:**
- Receive user commands
- Pass commands to the decision agent
- Read and update Google Sheets
- Return responses to the frontend

**Main API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Load web interface |
| `/chat` | POST | Process user command |
| `/pilots` | GET | Return pilot data |
| `/drones` | GET | Return drone data |
| `/missions` | GET | Return mission data |

---

### 3. Decision Agent (Core Logic)

**File:** `agent.py`

**Responsibilities:**
- Interpret user commands
- Match pilots to missions
- Update pilot or drone status
- Detect conflicts
- Suggest or perform reassignments

The agent uses rule-based logic to ensure predictable and reliable operational decisions.

---

### 4. Data Layer (Google Sheets)

Google Sheets is used as a **live operational database**.

It contains three worksheets:

1. **Pilot_Roster**  
   Pilot details, skills, location, and status

2. **Drone_Fleet**  
   Drone models, capabilities, and availability

3. **Missions**  
   Project requirements, location, and needed skills

**Advantages:**
- Real-time updates
- Easy to view and edit
- No database setup required

---

## Data Flow (Command Lifecycle)

1. User enters a command in the chat.
2. Frontend sends the command to `/chat`.
3. Backend forwards it to the decision agent.
4. Agent reads data from Google Sheets.
5. Agent performs logic (assignment, update, or check).
6. Google Sheet is updated.
7. Response is sent back to the user.
8. Tables refresh automatically.

---

## Technology Stack

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- FastAPI

**Data Layer**
- Google Sheets
- gspread

**AI Layer (optional)**
- Gemini API for intent understanding

---

## Project Structure

skylark-agent/
│
├── app.py # FastAPI server
├── act.py # Decision logic
├── Sheets.py # Google Sheets integration
├── requirements.txt
├── Proclfile
├── templates/
│ └── index.html # Frontend UI
└── README.md
