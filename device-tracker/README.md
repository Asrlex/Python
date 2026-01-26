# Device Tracker

This project is a lightweight application designed to track the battery life and general information of connected devices on a Windows 11 system. It provides a simple graphical user interface (GUI) using Tkinter, allowing users to monitor device metrics in real-time.

## Project Structure

```
device-tracker
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui.py           # Implementation of the Tkinter GUI
│   ├── device_tracker.py # Logic for tracking connected devices
│   ├── utils.py         # Utility functions for data handling
│   └── assets
│       └── styles.css   # CSS styles for the GUI
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd device-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in the terminal:
```
python src/main.py
```

The application will initialize and start polling for connected devices every minute. Each device will have its own tab in the GUI, displaying a small graph that shows the current latency and battery drain.

## Libraries and APIs Used

- **Tkinter**: For creating the GUI.
- **Matplotlib**: For graphing the latency and battery drain.
- **Windows 11 APIs**: To gather information about connected devices and their battery life.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.