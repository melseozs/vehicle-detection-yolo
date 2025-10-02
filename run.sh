#!/bin/bash

echo "🚗 Starting Vehicle Detection System..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if input video exists
if [ ! -f "input_video.mp4" ]; then
    echo "⚠️  Warning: input_video.mp4 not found"
    echo "Please place your video file in the project directory and rename it to 'input_video.mp4'"
    echo
fi

echo "Choose run mode:"
echo "1) Show on screen (imshow)"
echo "2) Save to file (imwrite)"
echo
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🎬 Starting real-time detection (Press ESC to close)..."
        python vehicle_detection_main_yolo.py imshow
        ;;
    2)
        echo "💾 Starting detection and saving to file..."
        python vehicle_detection_main_yolo.py imwrite
        echo "✅ Output saved as output_video.avi"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
