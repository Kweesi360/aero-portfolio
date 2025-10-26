import os
import cv2

# Path to your CAD videos
VIDEO_FOLDER = "models"
OUTPUT_HTML = "cad.html"   # output page
BACKGROUND_IMAGE = "space.jpg"  # put your space image in same folder

# Create thumbnails folder
THUMBNAIL_FOLDER = "thumbnails"
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

cards_html = ""

# Loop through videos and create thumbnails
for i, file in enumerate(os.listdir(VIDEO_FOLDER)):
    if file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
        video_path = os.path.join(VIDEO_FOLDER, file)
        cap = cv2.VideoCapture(video_path)
        success, frame = cap.read()
        cap.release()

        if success:
            thumb_path = os.path.join(THUMBNAIL_FOLDER, f"thumb_{i}.jpg")
            cv2.imwrite(thumb_path, frame)

            description = os.path.splitext(file)[0].replace("_", " ").title()

            cards_html += f"""
            <div class="card" onclick="openModal('{video_path}', '{description}')">
                <img src="{thumb_path}" alt="{description}">
                <p>{description}</p>
            </div>
            """

# HTML template with modal
html_template = f"""
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CAD Portfolio</title>
    <style>
        html, body {{
            height: 100%;
            margin: 0;
        }}
        body {{
            background: url('{BACKGROUND_IMAGE}') no-repeat center center fixed;
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
        }}
        .container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);  /* exactly 4 per row */
            gap: 20px;
            padding: 40px;
        }}
        .card {{
            background: rgba(0,0,0,0.6);
            border-radius: 15px;
            border: 3px solid white;  /* thicker border */
            overflow: hidden;
            text-align: center;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.7);
            cursor: pointer;
            transition: transform 0.2s;
            width: 220px;   /* fixed card width */
            margin: auto;   /* center card in grid cell */
        }}
        .card:hover {{
            transform: scale(1.05);
        }}
        .card img {{
            width: 100%;
            height: 150px;  /* smaller thumbnail */
            object-fit: cover;
            display: block;
        }}
        .card p {{
            margin: 10px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1 style="text-align:center; padding:20px;">My CAD PORTFOLIO</h1>
    <div class="container">
        {cards_html}
    </div>
</body>
</html>
"""

