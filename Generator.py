
"""
Quarto Course Generator (Enhanced Stable Version)
--------------------------------------------------------
- Generates full course structure
- Copies template into each lecture folder as .qmd
- Builds README with full workflow instructions
- Works on Windows / Linux / macOS

Author: Dr. Mohamed Abdelhady
"""

from pathlib import Path
import re


AUTHOR = "Dr. Mohamed Abdelhady"
TEMPLATE_FILE = "template_lecture.txt"


def sanitize(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip())


BASE_DIR = Path(__file__).resolve().parent

print("\n[INFO] Script directory:", BASE_DIR)

course_name = input("Enter course name: ").strip()
num_lectures = int(input("Enter number of lectures: ").strip())

course_dir = BASE_DIR / sanitize(course_name)

print("[INFO] Creating course at:", course_dir)


folders = [
    course_dir,
    course_dir / "shared" / "styles",
    course_dir / "video_pipeline" / "downloaded",
    course_dir / "video_pipeline" / "processed",
    course_dir / "video_pipeline" / "thumbnails",
    course_dir / "build",
]

for f in folders:
    f.mkdir(parents=True, exist_ok=True)


template_path = BASE_DIR / TEMPLATE_FILE

if not template_path.exists():
    raise FileNotFoundError(f"Missing template file: {template_path}")

template_text = template_path.read_text(encoding="utf-8")


print("\n[INFO] Generating lectures...\n")

for i in range(1, num_lectures + 1):

    lecture_dir = course_dir / f"Lecture_{i:02d}"

    for sub in ["images", "videos", "code", "generated"]:
        (lecture_dir / sub).mkdir(parents=True, exist_ok=True)

    lecture_title = f"Lecture {i:02d}"

    from string import Template

    template = Template(template_text)

    qmd_content = template.substitute(
        course_name=course_name,
        lecture_title=lecture_title,
        author=AUTHOR
    )

    qmd_file = lecture_dir / f"lecture_{i:02d}.qmd"
    qmd_file.write_text(qmd_content, encoding="utf-8")

    print(f"[CREATED] {qmd_file}")


readme_path = course_dir / "README.md"

readme_content = f"""
# {course_name}

Generated Quarto Course

## Run

quarto preview Lecture_01/lecture_01.qmd
"""

readme_path.write_text(readme_content, encoding="utf-8")

print("\n====================================")
print("[SUCCESS] Done")
print(course_dir.resolve())
print("====================================")
