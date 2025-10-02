# Vehicle Detection & Speed Measurement System

A real-time vehicle detection and speed measurement system using YOLO11 and ByteTrack. This system detects vehicles in traffic videos, tracks them, and calculates their speeds with visual feedback.

## 🚗 Features

- **Real-time Vehicle Detection**: Detects cars, trucks, buses, motorcycles, and bicycles
- **Speed Measurement**: Calculates vehicle speeds in km/h with calibration support
- **Visual Feedback**: Color-coded bounding boxes (green for normal speed, red for speeding)
- **Vehicle Tracking**: Stable tracking with unique IDs using ByteTrack
- **Multiple Output Options**: Real-time display or video file output

## 📋 Requirements

- Python 3.8 or higher
- Windows 10/11 (tested on Windows)
- Internet connection (for initial model download)
- ~2GB free disk space

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd computer-vision-vehicle-detection
```

### 2. Setup Environment

#### Windows Users:
```powershell
# Quick setup (recommended)
setup.bat

# OR manual setup:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### macOS/Linux Users:
```bash
# Quick setup (recommended)
chmod +x setup.sh run.sh
./setup.sh

# OR manual setup:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Prepare Your Video
- Place your traffic video in the project folder
- Rename it to `input_video.mp4` OR modify the `VIDEO_IN` variable in the script

### 4. Run the System

#### Windows Users:
```powershell
# Activate environment first
.\.venv\Scripts\Activate.ps1

# Real-time display (ESC to close)
python vehicle_detection_main_yolo.py imshow

# Save to video file
python vehicle_detection_main_yolo.py imwrite
```

#### macOS/Linux Users:
```bash
# Quick run with menu (recommended)
./run.sh

# OR manual run:
source .venv/bin/activate
python vehicle_detection_main_yolo.py imshow    # Real-time display
python vehicle_detection_main_yolo.py imwrite   # Save to file
```

## 📁 Project Structure

```
computer-vision-vehicle-detection/
├── vehicle_detection_main_yolo.py    # Main detection script
├── yolo11n.pt                        # YOLO model weights
├── input_video.mp4                   # Your input video
├── output_video.avi                  # Generated output (when using imwrite)
├── requirements.txt                  # Python dependencies
├── setup.bat                         # Windows setup script
├── setup.sh                          # macOS/Linux setup script
├── run.sh                            # macOS/Linux run script
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## ⚙️ Configuration

### Speed Calibration
For accurate speed measurements, calibrate the system by modifying these values in `vehicle_detection_main_yolo.py`:

```python
PIX1 = sv.Point(x=400, y=info.height - 120)  # First calibration point
PIX2 = sv.Point(x=900, y=info.height - 120)  # Second calibration point  
D_METERS = 25.0  # Real distance between points in meters
```

### Speed Limit
```python
speed_limit = 50.0  # km/h threshold for speeding detection
```

### Vehicle Types
```python
VEHICLE_SET = {"car","truck","bus","motorcycle","motorbike","bicycle"}
```

## 🎯 Usage Examples

### Basic Detection
```powershell
# Activate environment first
.\.venv\Scripts\Activate.ps1

# Run with real-time display
python vehicle_detection_main_yolo.py imshow
```

### Save Results
```powershell
# Save processed video to file
python vehicle_detection_main_yolo.py imwrite
```

## 🔧 Troubleshooting

### Common Issues

**1. Virtual Environment Activation Error**
```powershell
# Run in Admin PowerShell once:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**2. Model Download Issues**
- Ensure internet connection is active
- The model will be downloaded automatically on first run

**3. Slow Performance**
- The system works on CPU but GPU acceleration is recommended for better performance
- Consider using a smaller YOLO model for faster processing

**4. Incorrect Speed Measurements**
- Calibrate the system using real-world measurements
- Ensure calibration points are on the same horizontal line

## 📊 Output

- **Real-time Mode**: Shows live detection with bounding boxes and speed labels
- **Save Mode**: Creates `output_video.avi` with all detections and measurements
- **Console Output**: Displays detection statistics and progress

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for the detection model
- [Supervision](https://github.com/roboflow/supervision) for tracking and visualization
- [ByteTrack](https://github.com/ifzhang/ByteTrack) for multi-object tracking

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.
