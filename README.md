# Prima Flask API

Prima is a simple Flask API for user creation and retrieval, featuring a SQLite database and environment variable-based configuration.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Server](#running-the-server)
2. [API Endpoints](#api-endpoints)
   - [Create User](#create-user-endpoint)
   - [Get User](#get-user-endpoint)
3. [Request/Response Formats](#requestresponse-formats)
   - [Create User](#create-user-post-apiusers)
   - [Get User](#get-user-get-apiusersuser_id)
4. [Error Handling](#error-handling)
5. [Conclusion](#conclusion)

## Getting Started

### Prerequisites

- Flask
- Flask-SQLAlchemy
- Werkzeug
- SQLAlchemy

### Installation

```bash
git clone https://github.com/Syed-Hamza-Zahir/Prima.git
cd Prima
python -m venv venv
.\venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
