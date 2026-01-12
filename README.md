# Flowguard

**Flowguard** is a production-grade AI workflow orchestration and reliability platform designed to build, run, version, test, and monitor LLM-powered pipelines in production.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

## Basic Architecture of Flowguard

Flowguard operates on a layered architecture ensuring separation of concerns between client interfaces, control logic, execution, and data.

- **Client Layer**: Next.js Dashboard & CLI for user interaction.
- **Control Plane**: FastAPI services for managing workflow definitions and versions.
- **Execution Plane**: Async engine for reliable task orchestration.
- **AI Services**: Model-agnostic adapters for LLM interactions.

*(See `docs/system_architecture.md` for the full diagram)*

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic, SQLAlchemy, AsyncIO.
- **Frontend**: TypeScript, Next.js 14 (App Router), TailwindCSS, Shadcn/UI.
- **Infrastructure**: Docker, PostgreSQL, Redis (planned).

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/NiravTech22/Flowguard.git
    cd Flowguard
    ```

2.  **Start the Backend**:
    ```bash
    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate
    pip install -r requirements.txt
    uvicorn src.main:app --reload
    ```

3.  **Start the Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Visit the Dashboard**:
    Open [http://localhost:3000](http://localhost:3000)

## 🧪 Testing

- **Backend**: `pytest`
- **Frontend**: `npm run test` (configured later)

## 🤝 Contribution

Please verify all changes with `tools/verify_changes.sh` (planned) before pushing.
