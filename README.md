# Gestalyze

![Gestalyze Logo](gestalyze-logo-text.svg)

**Gesture-based Smart Home Interface using Sign Language and Hand Pose Recognition**

🔧 Built with [FastAPI](https://fastapi.tiangolo.com), [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker), [React](https://react.dev), [MQTT](https://mqtt.org) and [Home Assistant](https://www.home-assistant.io).

🔍 Empowering accessibility through open-source gesture control.

---

## 📦 Overview

Gestalyze is an open-source project that enables real-time hand gesture recognition for controlling smart home devices. By combining computer vision and machine learning techniques, the system interprets static hand poses — including alphabet signs from sign language — and sends commands to home automation platforms like [Home Assistant](https://www.home-assistant.io).

The system is modular, lightweight, and designed for low-power environments using technologies such as [MQTT](https://mqtt.org), [MediaPipe Hands](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker), and [React](https://react.dev). Users can extend, train custom models, and integrate new gesture mappings for full control over their smart environment.

---

## 🎯 Key Features

- ✋ Real-time hand detection and finger tracking with [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker).
- 🔠 ASL static alphabet recognition using trainable ML classifiers.
- 💡 Smart home integration via [MQTT](https://mqtt.org) and [Home Assistant](https://www.home-assistant.io) plugins.
- ⚡ Low-latency WebSocket communication between frontend and backend.
- 📷 Frontend web app built in [React](https://react.dev) + WebRTC.
- 🌍 Multilingual interface with i18n support.
- 🧠 Supports custom and pre-trained gesture models.
- 📊 Visualization tools for metrics, training and evaluation.
- 🧪 Designed for reproducible research and experimentation.

---

## 🧱 System Architecture

This repository is currently structured as a monorepo to simplify development, deployment, and cross-component coordination. As the project matures, it is expected that individual components — such as the frontend, backend, and Home Assistant integrations — may be separated into distinct repositories to improve modularity and scalability.

---

## 🗃️ Project Structure

```
gestalyze/
├── backend/               # Gestalyze backend server
│   ├── inference/         # ML model inference and processing
│   ├── mqtt/              # MQTT client and message handling
│   └── ssl/               # SSL certificates and configuration
├── config/                # Project-wide configuration files (e.g., MQTT)
├── datasets/              # Public and custom gesture datasets
├── docs/                  # Assets and documentation support files
├── frontend/              # React web app for video capture and UI
├── homeassistant/         # Plugins and custom components for Home Assistant
│   ├── custom_components/ # Custom Home Assistant integration
│   └── gestalyze_plugin/  # Home Assistant plugin for gestalyze
├── models/                # Serialized ML models (.joblib)
├── training/              # Training scripts and model experiments
├── website/               # Public website (gestalyze.com)
└── Makefile               # Project task automation
```

---

## 🚀 Getting Started

> Requires Python 3.10+, Node.js 20+, and Mosquitto MQTT

```bash
# Clone repository
git clone https://github.com/yourname/gestalyze.git
cd gestalyze

# Install Python & Node dependencies
make install

# Start development servers
make dev
```

Open your browser to `http://localhost:5173` to launch the interface.

---

## 🧠 Training Custom Models

To train your own gesture recognition model:

```bash
# Example with custom dataset
make extract-landmarks DATASET_NAME=your_dataset
make train MODEL_TYPE=custom DATASET_NAME=your_dataset
```

Models are saved to `models/` and can be switched via the interface.

---

## 🛠️ Makefile Commands

Common tasks for development and training:

- `make install` — Installs Python and Node.js dependencies
- `make dev` — Starts both frontend and backend in development mode
- `make build` — Builds the frontend for production
- `make run` — Runs the backend with built frontend and MQTT
- `make run-ssl` — Runs backend with SSL enabled
- `make train MODEL_TYPE=custom DATASET_NAME=name` — Trains a gesture model
- `make extract-landmarks DATASET_NAME=name` — Extracts MediaPipe landmarks from dataset
- `make clean` — Cleans compiled files, build folders and caches
- `make mqtt-start`, `make mqtt-stop` — Start/stop the Mosquitto broker
- `make ssl-key-gen` — Generates self-signed SSL certificates
- `make deploy-ha` — Deploys custom integration to Home Assistant
- `make website-dev` — Starts the public website in development mode
- `make website-build` — Builds the public website for production
- `make version` — Displays version info
- `make help` — Shows available commands

For advanced options and custom variables, inspect the `Makefile`.

---

## 💡 Smart Home Integration

Gestalyze communicates with [Home Assistant](https://www.home-assistant.io/) via [MQTT](https://mqtt.org). You can:

- Use our **plugin** (external service)
- Or the **custom integration** under `homeassistant/custom_components/gestalyze/`

This enables the use of sensors and event-based automations based on detected hand gestures.

---

## 🔒 Privacy & Security

All gesture processing happens **locally** on your device.
No images or biometric data are transmitted or stored externally.
See [`Privacy Policy`](https://gestalyze.com/privacy) for full details.

---

## 📖 Documentation

- Full system documentation: https://gestalyze.com
- Datasets, models and training configuration
- Code walkthroughs, diagrams and tutorials

---

## 📜 License

This project is licensed under the Apache License 2.0 — see [LICENSE](./LICENSE) for details.

---

## 🤝 Contributing

Pull requests, feature ideas and issue reports are welcome.
For contributions, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 👋 Acknowledgments

- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) by Google for hand tracking
- [Home Assistant](https://www.home-assistant.io) for smart home integration
- Hugging Face and Kaggle for gesture datasets
- All open-source contributors who inspire and make projects like this possible

---

## 🧭 Roadmap & TODO

Gestalyze is still under active development. Some upcoming features and improvements include:

- [ ] Support for multiple simultaneous frontend clients.
- [ ] Real-time model hot-swapping via the interface.
- [ ] Integration with additional smart home platforms.
- [ ] Gesture recording and labeling tools for data collection.
- [ ] Extended dynamic gesture recognition (sequential actions).
- [ ] Accessibility testing with real users and community feedback.
- [ ] CI/CD automation for releases and plugin deployment.
- [ ] Docker-based deployment flow.
- [ ] Unit testing for every module.
- [ ] Improved model modularity for easier experimentation and integration.
- [ ] Continued refinement of gesture recognition model accuracy.

---

© 2025 — Initially developed by [rbcorrales](https://github.com/rbcorrales).
