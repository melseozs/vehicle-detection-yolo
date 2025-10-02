import sys, os, csv, math, cv2
from collections import defaultdict, deque
from ultralytics import YOLO
import supervision as sv

ARG = sys.argv[1] if len(sys.argv) > 1 else "imwrite" 
VIDEO_IN  = "input_video.mp4"
VIDEO_OUT = "output_video.avi"   
CSV_PATH  = "traffic_measurement.csv"
CROP_DIR  = "detected_vehicles"
os.makedirs(CROP_DIR, exist_ok=True)


model = YOLO("yolo11n.pt")  
names = model.names
VEHICLE_SET = {"car","truck","bus","motorcycle","motorbike","bicycle"}
vehicle_ids = [i for i,n in names.items() if n in VEHICLE_SET]


NORMAL_COLOR = (0, 255, 0)    
SPEEDING_COLOR = (0, 0, 255)   
BOX_THICKNESS = 3
TEXT_SCALE = 0.8
TEXT_THICKNESS = 2


info = sv.VideoInfo.from_video_path(VIDEO_IN)
fps = max(info.fps, 1)
frames = sv.get_video_frames_generator(source_path=VIDEO_IN)

box_annot  = sv.BoxAnnotator()
label_annot = sv.LabelAnnotator(text_thickness=2, text_scale=0.7)

PIX1 = sv.Point(x=400, y=info.height - 120)
PIX2 = sv.Point(x=900, y=info.height - 120)
D_METERS = 25.0
pix_dist = math.hypot(PIX2.x-PIX1.x, PIX2.y-PIX1.y)
M_PER_PIXEL = D_METERS / max(pix_dist, 1e-6)

history = defaultdict(lambda: deque(maxlen=5))
tracker = sv.ByteTrack()

def color_name(bgr):
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    hsv = cv2.cvtColor(
        cv2.resize(bgr.reshape(1,1,3).astype("uint8"), (1,1)), cv2.COLOR_BGR2HSV
    )[0,0]
    h, s, v = int(hsv[0]), int(hsv[1]), int(hsv[2])
    if v < 50: return "black"
    if s < 40: return "white" if v > 200 else "gray"
    if   0 <= h < 10 or 170 <= h <= 179: return "red"
    elif 10 <= h < 25:  return "orange"
    elif 25 <= h < 35:  return "yellow"
    elif 35 <= h < 85:  return "green"
    elif 85 <= h < 125: return "blue"
    elif 125 <= h < 160:return "purple"
    else: return "brown"

def direction_from(history_deque):
    if len(history_deque) < 2: return ""
    (px,py,_), (qx,qy,_) = history_deque[-2], history_deque[-1]
    dy = qy - py
    dx = qx - px
    if abs(dy) >= abs(dx):
        return "down" if dy > 0 else "up"
    return "right" if dx > 0 else "left"



USE_WRITE = (ARG == "imwrite")
writer = None
if USE_WRITE:
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(
        VIDEO_OUT, fourcc, fps, (int(info.width), int(info.height))
    )

try:
    for fi, frame in enumerate(frames):
        res = model(frame)[0]
        det = sv.Detections.from_ultralytics(res)

        mask = [cid in vehicle_ids for cid in det.class_id]
        det = det[mask]

        
        det = tracker.update_with_detections(det)

        labels = []

        for (x1, y1, x2, y2), cid, tid in zip(det.xyxy, det.class_id, det.tracker_id):
            if tid is None:
                continue

            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
            history[tid].append((cx, cy, fi))

            
            speed_kmh = 0.0
            if len(history[tid]) >= 2 and M_PER_PIXEL > 0:
                (px, py, pi), (qx, qy, qi) = history[tid][-2], history[tid][-1]
                dt = (qi - pi) / max(fps, 1)
                if dt > 0:
                    dpix = math.hypot(qx - px, qy - py)
                    speed_kmh = (dpix * M_PER_PIXEL / dt) * 3.6

            x1i, y1i, x2i, y2i = map(int, [x1, y1, x2, y2])
            cx1, cy1 = max(x1i, cx - 3), max(y1i, cy - 3)
            cx2, cy2 = min(x2i, cx + 3), min(y2i, cy + 3)
            patch = frame[cy1:cy2, cx1:cx2]
            col = color_name(patch.mean(axis=(0, 1))) if patch.size else "gray"

            
            mov = direction_from(history[tid])

        cname = names[int(cid)]

        vis = frame.copy()
        
        for (x1, y1, x2, y2), cid, tid in zip(det.xyxy, det.class_id, det.tracker_id):
            if tid is None:
                continue
                
            speed_kmh = 0.0
            if len(history[tid]) >= 2 and M_PER_PIXEL > 0:
                (px, py, pi), (qx, qy, qi) = history[tid][-2], history[tid][-1]
                dt = (qi - pi) / max(fps, 1)
                if dt > 0:
                    dpix = math.hypot(qx - px, qy - py)
                    speed_kmh = (dpix * M_PER_PIXEL / dt) * 3.6
            
            speed_limit = 50.0
            if speed_kmh > speed_limit:
                color = SPEEDING_COLOR  
                status = " HIZLI!"
            else:
                color = NORMAL_COLOR     
                status = "NORMAL"
            
            
            cv2.rectangle(vis, (int(x1), int(y1)), (int(x2), int(y2)), color, BOX_THICKNESS)
            
            
            cname = names[int(cid)]
            text = f"{cname} #{tid} {speed_kmh:.1f}km/h"
            
            
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, TEXT_THICKNESS)[0]
            cv2.rectangle(vis, (int(x1), int(y1)-25), (int(x1) + text_size[0] + 10, int(y1)-5), (0, 0, 0), -1)
            
            
            cv2.putText(vis, text, (int(x1)+5, int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       TEXT_SCALE, color, TEXT_THICKNESS)
        
        
        
        
        cv2.putText(vis, f"Vehicle Detection System", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        

        
        if USE_WRITE and writer is not None:
            writer.write(vis)
        elif ARG == "imshow":
            cv2.imshow("Vehicle Counting (YOLO)", vis)
            if cv2.waitKey(1) & 0xFF == 27:
                break

finally:
    
    if writer is not None:
        try:
            writer.release()
        except Exception:
            pass
    
    if ARG == "imshow":
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
