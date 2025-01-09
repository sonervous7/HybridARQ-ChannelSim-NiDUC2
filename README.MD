# HybridARQ-ChannelSim-NiDUC2

Course project from Wrocław University of Science and Technology, simulating reliable data transmission with Hybrid ARQ using error detection and correction to maintain data integrity over noisy channels.

## Features
- Simulates data transmission over noisy channels using Hybrid ARQ.
- Supports Binary Symmetric Channel (BSC) and Gilbert-Elliott Channel.
- Implements error detection (CRC8, CRC16, CRC32, parity check) and error correction (Reed-Solomon).
- Visualizes transmission results using Matplotlib.

## Requirements
- Python 3.8 or higher

The required Python libraries are listed in the `requirements.txt` file.

## Installation and Setup

### 1. Clone the repository
Clone this repository to your local machine using the following command:
```bash
git clone <repository_url>
```
Replace `<repository_url>` with the actual URL of the repository.

### 2. Create a virtual environment
Navigate to the project directory and create a virtual environment:
```bash
cd HybridARQ-ChannelSim-NiDUC2
python -m venv venv
```
Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## How to Run
The program entry point is `main.py`. To run the simulation, execute the following command:
```bash
python main.py
```

## Project Structure
- `main.py`: Entry point of the program.
- `channel/`: Contains channel implementations (e.g., BSC, Gilbert-Elliott).
- `error_detection_code/`: Error detection code implementations (CRC8, CRC16, CRC32, parity check).
- `error_correction_code/`: Reed-Solomon error correction code.
- `image_handler/`: Handles image loading and processing.
- `frame/`: Defines the data structure for transmitting packets.
- `requirements.txt`: List of Python libraries required to run the project.

## Usage Notes
- Ensure you have installed all dependencies listed in `requirements.txt`.
- Configure simulation parameters (e.g., channel type, error probabilities) in the program prompts or by editing `main.py` as needed.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
If you encounter any issues, feel free to contact the project contributors.

