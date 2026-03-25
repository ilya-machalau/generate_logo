# Image Generator for QA Testing

A Python-based utility for **Quality Assurance (QA)** to generate image files of specific sizes. This tool is designed to test file upload limits, boundary values, and system stability when handling large image files.

## 🚀 Key Features
- Supports multiple formats: **PNG, JPEG, WEBP, HEIC, and SVG**.
- Generates files close to **20 MB** for positive testing.
- Includes a dedicated **Negative Test Case** file (> 21 MB).
- Uses random noise generation to ensure files are not easily "compressed" by system optimizers.

## 🛠 Prerequisites
Ensure you have **Python 3** installed. You will also need to install the following image processing libraries:

##```bash
pip install Pillow pillow-heif

📋 How to Use
1. Clone the repository:
git clone [https://github.com/ilya-machalau/generate_logo.git](https://github.com/ilya-machalau/generate_logo.git)
cd generate_logo
2. Run the script:
python3 generate_logo.pypython3
3. Check the results:
The script will generate several files in the same directory, labeled logo_final_20.* and logo_negative_21.png.

🧠 Why the different resolutions?
Because different formats use different compression methods, the script automatically adjusts the resolution to hit the target file size:

PNG/WEBP: Balanced resolution (~2600x2600).

JPEG/HEIC: Higher resolution required (~5000x5000+) due to aggressive compression.

SVG: Uses vector path injection to reach the exact byte size.

