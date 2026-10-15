# 3-Month Game QA Automation Learning Roadmap

This curriculum guides you from complete beginner to building production-ready test automation for game studios (PC, Mobile, and Consoles).

---

## 📅 Month 1: Fundamentals of Game Architecture & Instrumentation

### Week 1: Understanding the Game Loop & State Machines
- **Concept:** How games differ from websites. The concept of Delta Time (`dt`), Tick rates (30/60/120 FPS), and the Game Loop (`ProcessInput` -> `Update` -> `Render`).
- **Hands-on:** Study [`mini_game_engine/engine.py`](../mini_game_engine/engine.py). Run headless mode vs. tick updates.
- **Milestone Challenge:** Add a new `STAMINA` attribute to the player and drain it whenever movement commands are simulated.

### Week 2: GameObject Hierarchy & Component-Based Design
- **Concept:** Entity-Component-System (ECS) vs Object-Oriented GameObjects (Unity/Unreal style).
- **Hands-on:** Inspect how components (`Transform`, `Collider2D`, `HealthComponent`) attach to GameObjects.
- **Milestone Challenge:** Create a `ShieldComponent` that absorbs 50% damage before health is impacted.

### Week 3: In-Engine Automation Drivers & RPC Bridges
- **Concept:** How tools like **AltTester** and **Unreal Automation Driver** hook into games. Sockets, JSON-RPC, and serialization.
- **Hands-on:** Study [`automation_sdk/driver.py`](../automation_sdk/driver.py). Understand how `driver.find_object_by_name("Player")` queries the engine.
- **Milestone Challenge:** Implement a `driver.find_objects_by_tag("Enemy")` method that returns all living monsters in the scene.

### Week 4: Build Verification Tests (BVTs) & Smoke Testing
- **Concept:** What AAA studios run on every code check-in (CI/CD).
- **Hands-on:** Run [`test_suites/test_smoke_bvt.py`](../test_suites/test_smoke_bvt.py).
- **Milestone Challenge:** Write an automated smoke test verifying that all audio sound buses initialize without mute flags.

---

## 📅 Month 2: Core Gameplay Mechanics & Complex Automation Patterns

### Week 5: Combat, Collision & Physics Assertions
- **Concept:** Deterministic math assertions in games: weapon damage, hitboxes, distance checks, and death states.
- **Hands-on:** Run [`test_suites/test_combat_and_physics.py`](../test_suites/test_combat_and_physics.py).
- **Milestone Challenge:** Write a test verifying projectile falloff damage: weapons deal 100% damage within 5 units, but 50% damage beyond 10 units.

### Week 6: In-Game Economy & Inventory Boundary Testing
- **Concept:** Validating item stacks, currency transactions, slot caps, and preventing duplication (dupe) exploits.
- **Hands-on:** Run [`test_suites/test_economy_inventory.py`](../test_suites/test_economy_inventory.py).
- **Milestone Challenge:** Automate an edge-case test: attempt to sell an item while simultaneously dropping it, ensuring the inventory system rejects race conditions.

### Week 7: Black-Box Computer Vision & Optical Verification (Airtest/OpenCV)
- **Concept:** When games have no debug hooks (locked console builds), using OpenCV template matching, pixel color sampling, and perceptual hashing to verify rendering.
- **Hands-on:** Explore visual image matching concepts to locate HUD health bars on screen.
- **Milestone Challenge:** Capture simulated frames and assert that the health bar color shifts from green to red when HP drops below 25%.

### Week 8: Performance Profiling & Frame Rate Stress Testing
- **Concept:** Monitoring memory usage, tick execution times, garbage collection spikes, and detecting frame drops.
- **Hands-on:** Run [`test_suites/test_performance_stress.py`](../test_suites/test_performance_stress.py).
- **Milestone Challenge:** Simulate spawning 500 enemies in the scene and assert that engine tick time remains below 25ms.

---

## 📅 Month 3: Autonomous AI Bots & CI/CD Game Pipelines

### Week 9: Autonomous Playtesting & Soak Bots (TestBots)
- **Concept:** Modern studios deploy automated bots (Random Walk, NavMesh A*, or Behavior Trees) to wander maps for 12 hours hunting memory leaks, geometry holes, and physics glitches.
- **Hands-on:** Run [`test_suites/test_autonomous_bot.py`](../test_suites/test_autonomous_bot.py).
- **Milestone Challenge:** Program the test bot with a goal-oriented rule: seek out health potions when HP < 30%.

### Week 10: Game Localization QA (LQA) Automation
- **Concept:** Automated checking for truncated dialogue strings, missing font glyphs (`□`), and text expansion in EFIGS + CJK languages.
- **Hands-on:** Integrate the `static_string_auditor.py` and `pseudo_localizer.py` from the `game_qa_automation` module.
- **Milestone Challenge:** Write an automated test that audits UI dialogue boxes across 10 languages and logs any string that overflows the button boundary.

### Week 11: Real-World Engine Exploration (AltTester on Unity & Unreal Gauntlet)
- **Concept:** Downloading a free Unity starter kit (e.g., Unity Roll-a-ball or 2D Platformer) and attaching real AltTester SDK.
- **Milestone Challenge:** Write an AltTester Python test that completes Level 1 of a sample Unity game without human input.

### Week 12: CI/CD Pipeline & Portfolio Packaging
- **Concept:** Running game tests headlessly inside GitHub Actions on every pull request.
- **Hands-on:** Configure `.github/workflows/game_qa_pipeline.yml`.
- **Milestone Challenge:** Publish your GitHub repository with badge indicators showing passing game test runs. Add it to your resume as a Game Automation Portfolio project!
