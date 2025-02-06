import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# Function to format date as RFC-822 (Required for valid RSS)
def format_pub_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

# Define RSS structure with media & atom namespaces
rss = ET.Element("rss", version="2.0", attrib={
    "xmlns:media": "http://search.yahoo.com/mrss/",
    "xmlns:atom": "http://www.w3.org/2005/Atom"
})
channel = ET.SubElement(rss, "channel")

# Add required feed metadata
ET.SubElement(channel, "title").text = "Build with GenAI - Video Feed"
ET.SubElement(channel, "link").text = "https://github.com/victordelrosal/buildwithGenAI"
ET.SubElement(channel, "description").text = "Latest video updates"
ET.SubElement(channel, "atom:link", href="https://raw.githubusercontent.com/victordelrosal/buildwithGenAI/main/feed.xml", rel="self", type="application/rss+xml")

# Read JSON files, sort by date, and add them as RSS items
video_dir = "videos"
videos = []

for filename in os.listdir(video_dir):
    if filename.endswith(".json"):
        with open(os.path.join(video_dir, filename), "r") as f:
            video = json.load(f)
        videos.append(video)

# Sort videos by date (newest first)
videos.sort(key=lambda v: v["date"], reverse=True)

for video in videos:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = video["title"]
    ET.SubElement(item, "link").text = f"https://www.youtube.com/watch?v={video['id']}"

    # Add CDATA for description (fix encoding issues)
    description = ET.SubElement(item, "description")
    description.text = f"<![CDATA[{video['description']}]]>"

    # Correctly format pubDate (RFC-822 format)
    ET.SubElement(item, "pubDate").text = format_pub_date(video["date"])

    # Add media:thumbnail properly
    if video["thumbnail"] != "PENDING":
        thumbnail = ET.SubElement(item, "media:thumbnail", url=video["thumbnail"])

    # Add GUID
    ET.SubElement(item, "guid", isPermaLink="true").text = f"https://www.youtube.com/watch?v={video['id']}"

    # Add complexity as a category
    ET.SubElement(item, "category").text = f"Complexity: {video['complexity']}"

    # Add tools as separate categories
    for tool in video["tools"]:
        ET.SubElement(item, "category").text = f"Tool: {tool}"

    # Add keywords as separate categories
    for keyword in video["keywords"]:
        ET.SubElement(item, "category").text = f"Keyword: {keyword}"

# Write XML file
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

print("✅ RSS feed updated successfully! Now test it on W3C Validator.")
