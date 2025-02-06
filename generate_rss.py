import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

# Function to format date as RFC-822
def format_pub_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

# Define RSS structure
rss = ET.Element("rss", version="2.0", attrib={"xmlns:media": "http://search.yahoo.com/mrss/"})
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Build with GenAI - Video Feed"
ET.SubElement(channel, "link").text = "https://github.com/victordelrosal/buildwithGenAI"
ET.SubElement(channel, "description").text = "Latest video updates"

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

    # Add CDATA for description
    description = ET.SubElement(item, "description")
    description.text = f"<![CDATA[{video['description']}]]>"

    # Correctly format pubDate
    ET.SubElement(item, "pubDate").text = format_pub_date(video["date"])

    # Add media:thumbnail
    thumbnail = ET.SubElement(item, "media:thumbnail", url=video["thumbnail"])

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

print("✅ RSS feed updated successfully!")
