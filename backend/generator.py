# generator.py
import os
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "generated_sites"

def generate_website(data: dict):
    business_name = data.get("name", "Unnamed Business")
    theme = data.get("theme", "minimalist")
    services = data.get("services", ["Service 1", "Service 2"])
    contact_email = data.get("email", "info@example.com")
    color_primary = data.get("color_primary", "#1a73e8")
    address = data.get("address", "")
    description = data.get("description", f"{business_name} offers top-tier services tailored to your needs.")

    # Load template
    env = Environment(loader=FileSystemLoader(f"{TEMPLATE_DIR}/{theme}"))
    template = env.get_template("index.html")

    # Render website with injected data
    output_html = template.render(
        name=business_name,
        services=services,
        email=contact_email,
        color=color_primary,
        address=address,
        description=description,
    )

    # Create output folder
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    site_folder = f"{OUTPUT_DIR}/{business_name.replace(' ', '_')}_{timestamp}"
    os.makedirs(site_folder, exist_ok=True)

    # Save generated HTML
    with open(f"{site_folder}/index.html", "w", encoding="utf-8") as f:
        f.write(output_html)

    # Copy static assets
    static_src = f"{TEMPLATE_DIR}/{theme}/assets"
    static_dst = f"{site_folder}/assets"
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)

    return {
        "message": "Website generated successfully",
        "site_path": site_folder,
        "preview_url": f"/{site_folder}/index.html"
    }
