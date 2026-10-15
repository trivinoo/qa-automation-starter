# Game QA Automation Lab (Industry Practice Project)

A hands-on, lightweight video game test automation project replicating how major game studios (Unreal, Unity, AltTester, Airtest Poco) automate game testing across PC, mobile, and consoles.

---

## 🎮 Why Games Require Different Automation

Unlike websites or mobile apps where you inspect HTML DOM trees or mobile UI accessibility tags, **games render continuously at 60+ FPS inside a 3D/2D graphics engine**.

Traditional black-box tools cannot "see" inside the game canvas. Modern game studios solve this using **embedded test hooks / RPC drivers** that expose the internal `GameObject` hierarchy and components to external test frameworks.

This project implements that exact pattern:
- **`mini_game_engine/`**: A simulated 2D Game Engine featuring a game loop, delta time, GameObject hierarchy, and components (`Transform`, `HealthComponent`, `InventoryComponent`, `WeaponComponent`, `Collider2D`).
- **`automation_sdk/`**: An automation client (`GameDriver`, `GameElement`) modeled after **AltTester (AltUnity)** and **Airtest Poco**.
- **`test_suites/`**: Practical automated tests covering Smoke/BVT, combat distance physics, inventory caps, and autonomous exploratory playtest bots.
- **`curriculum/`**: A complete **3-Month Learning Roadmap** with weekly milestones and challenges to build your gaming QA portfolio.

---

## 🚀 Quick Start: Running the Lab Tests

Zero external setup required (uses Python standard library):

```powershell
python game_qa_automation_lab\run_lab_tests.py
```

### What gets executed:
1. **Smoke & BVT (Build Verification Tests):** Validates engine initialization, scene transition, and baseline player stats.
2. **Combat & Physics Distance Mechanics:** Asserts that attacks fail when out of range, navigation closes distance, and lethal damage sets `is_alive = False`.
3. **Economy & Inventory Boundaries:** Verifies item inventory slot limits and rejects overflow race conditions.
4. **Autonomous Playtest Bot (TestBot):** Spawns an automated bot that calculates vector angles, navigates toward targets, and eliminates them autonomously.

---

## 📚 3-Month Study Guide

Check [`curriculum/3_month_learning_roadmap.md`](curriculum/3_month_learning_roadmap.md) for the structured 12-week progression plan!
