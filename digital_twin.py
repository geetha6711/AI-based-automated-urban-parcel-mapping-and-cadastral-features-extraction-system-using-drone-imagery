import json
import glob
import os

OUTPUT_DIR = "output"

# Ella JSON files-um find pannrom
json_files = glob.glob(os.path.join(OUTPUT_DIR, "*_data.json"))
print(f"Found {len(json_files)} data files")

for json_file in json_files:
    with open(json_file, "r") as f:
        data = json.load(f)

    image_name = os.path.basename(data["image"])

    # ---- Interactive HTML digital twin build pannrom ----
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Digital Twin - Urban Parcel Mapping</title>
<style>
  body {{ font-family: Arial; background:#111; color:#eee; text-align:center; }}
  .container {{ position: relative; display:inline-block; margin-top:20px; }}
  img {{ max-width: 900px; }}
  .plot {{
    position: absolute; border: 2px solid lime; cursor: pointer;
    background: rgba(0,255,0,0.05);
  }}
  .plot:hover {{ background: rgba(0,255,0,0.35); }}
  .tooltip {{
    display: none; position: absolute; background: #000; color:#0f0;
    padding: 6px 10px; border: 1px solid lime; border-radius:5px; font-size:13px;
    white-space: nowrap; z-index: 10;
  }}
  .plot:hover .tooltip {{ display: block; }}
  h1 {{ color: #0f0; }}
  .summary {{ margin: 15px; font-size: 16px; }}
</style>
</head>
<body>
  <h1> Urban Parcel Digital Twin</h1>
  <div class="summary">
    Total Parcels: <b>{data['total_parcels']}</b> &nbsp; | &nbsp;
    Total Area: <b>{data['total_sqft']} sqft</b>
  </div>
  <div class="container">
    <img src="{image_name}" id="mapImg">
"""

    for p in data["parcels"]:
        html += f"""
    <div class="plot" style="left:{p['x']}px; top:{p['y']}px; width:{p['width']}px; height:{p['height']}px;">
      <div class="tooltip">Plot {p['plot_id']}<br>Area: {p['area_sqft']} sqft</div>
    </div>
"""

    html += """
  </div>
</body>
</html>
"""

    out_html = json_file.replace("_data.json", "_digital_twin.html")
    with open(out_html, "w",encoding="utf-8") as f:
        f.write(html)

    print(f" -> Digital twin created: {out_html}")

print("\nDigital Twin generation complete! Open the .html file in your browser.")