import os
import json
import xml.etree.ElementTree as ET

# Define RSS structure
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Build with GenAI - Video Feed"
ET.SubElement(channel, "link").text = "https://github.com/victordelrosal/buildwithGenAI"
ET.SubElement(channel, "description").text = "Latest video updates"

# Read video JSON files and add them as RSS items
video_dir = "videos"
for filename in sorted(os.listdir(video_dir), reverse=True):
    if filename.endswith(".json"):
        with open(os.path.join(video_dir, filename), "r") as f:
            video = json.load(f)
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = video["title"]
        ET.SubElement(item, "link").text = f"https://www.youtube.com/watch?v={video['id']}"
        ET.SubElement(item, "description").text = f"<![CDATA[{video['description']}]]>"
        ET.SubElement(item, "pubDate").text = video["date"]
        thumbnail = ET.SubElement(item, "media:thumbnail")
        thumbnail.set("url", video["thumbnail"])

# Write XML file
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

print("✅ RSS feed updated successfully!")
