import csv
import sys
import subprocess
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

CSV_FILE = "video_list.csv"
OUTPUT_DIR = "lecture_videos"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def download_video(url, start=None, end=None, index=1):

    print("\n==============================")
    print(f"[VIDEO {index}]")
    print(f"URL: {url}")
    print(f"START: {start}")
    print(f"END: {end}")
    print("==============================")

    output_template = str(
        Path(OUTPUT_DIR) / f"clip_{index:03d}_%(title)s.%(ext)s"
    )

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/mp4",
        "-o", output_template,
    ]

    # ========================================================
    # CASE 1: BOTH START AND END
    # ========================================================
    if start and end:
        cmd += ["--download-sections", f"*{start}-{end}"]

    # ========================================================
    # CASE 2: ONLY START (TO END OF VIDEO)
    # ========================================================
    elif start and not end:
        cmd += ["--download-sections", f"*{start}-inf"]

    # ========================================================
    # CASE 3: FULL VIDEO (NO TIMES)
    # ========================================================
    else:
        pass  # no section filtering

    cmd.append(url)

    subprocess.run(cmd)

# ============================================================
# READ CSV
# ============================================================

if not Path(CSV_FILE).exists():
    print(f"[ERROR] {CSV_FILE} not found")
    sys.exit(1)

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"[INFO] Found {len(rows)} videos")

# ============================================================
# PROCESS LOOP
# ============================================================

for i, row in enumerate(rows, start=1):

    url = row.get("url", "").strip()
    start = row.get("start", "").strip()
    end = row.get("end", "").strip()

    # normalize empty values
    start = start if start else None
    end = end if end else None

    if not url:
        print(f"[SKIP] Row {i} missing URL")
        continue

    download_video(url, start, end, i)

print("\n[DONE] All videos processed successfully!")