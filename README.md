# FI-Fitness using Google Fit API with Flask

This project aims to create a fitness website that utilizes the Google Fit API to retrieve and display fitness data for users. The website will be built using the Flask web framework, allowing for a smooth integration of API calls and a user-friendly interface for fitness tracking.

![image](https://github.com/totallyalien/Fi-Fitness/assets/97169836/489c3e4a-9e1d-4b68-b2da-8c542aaee4ae)
![image](https://github.com/totallyalien/Fi-Fitness/assets/97169836/fbb5128e-f61b-4165-bbd7-7460cf28683e)



## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Modern lifestyles emphasize the importance of maintaining a healthy lifestyle, and tracking fitness activities plays a vital role in achieving that goal. This fitness website will allow users to connect their Google Fit accounts, retrieve data about their daily steps, distance walked, and other fitness-related metrics, and present them in an easy-to-understand format.

## Features

- User authentication and authorization system.
- Google Fit API integration to fetch fitness data.
- Display of daily steps, distance, and other relevant metrics.
- User-friendly dashboard to visualize fitness progress.

## Getting Started

Follow these steps to set up and run the fitness website on your local machine.

### Prerequisites

- Python (3.6 or higher)
- Flask (`pip install Flask`)
- Google Cloud Platform Project with Google Fit API enabled

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/totallyalien/Fi-Fitness.git
   cd Fi-Fitness
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r library.txt
   ```

### Configuration

1. Create a project on the [Google Cloud Platform](https://console.cloud.google.com/).

2. Enable the Google Fit API for your project and create API credentials (OAuth 2.0 Client ID).

3. Update the `config.py` file with your Google Fit API credentials:
   ```python
   CLIENT_ID = 'your_client_id'
   CLIENT_SECRET = 'your_client_secret'
   ```

## Usage

1. Run the Flask development server:
   ```bash
   flask run
   ```

2. Open a web browser and navigate to `http://127.0.0.1:3210` to access the fitness website.

3. Sign up or log in to your account.

4. Connect your Google Fit account by authorizing the application to access your fitness data.

5. Once connected, you'll be able to see your fitness metrics on the dashboard.

## Contributing

Contributions are welcome! Feel free to open issues and pull requests for any enhancements or fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Disclaimer:** This project is for educational purposes and not officially affiliated with Google. Use at your own risk.

For any questions or support, contact [trex49001@gmail.com](mailto:trex49001@gmail.com).

**Note:** Replace placeholders such as  `CLIENT_SECRET`, and `CLIENT_ID` with actual values relevant to your project.
