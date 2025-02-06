import os
import json
import xml.etree.ElementTree as ET

# Create the root element for the RSS feed with version 2.0
rss = ET.Element("rss", version="2.0")

# Create the <channel> element and add the required metadata
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Build with GenAI - Video Feed"
ET.SubElement(channel, "link").text = "https://github.com/victordelrosal/buildwithGenAI"
ET.SubElement(channel, "description").text = "Latest video updates"

# Directory containing video JSON files
video_dir = "videos"

# Process each JSON file (sorted in reverse order so newest files appear first)
for filename in sorted(os.listdir(video_dir), reverse=True):
    if filename.endswith(".json"):
        with open(os.path.join(video_dir, filename), "r") as file:
            video = json.load(file)
        
        # Create an <item> element with only a <title> and a <link>
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = video["title"]
        ET.SubElement(item, "link").text = f"https://www.youtube.com/watch?v={video['id']}"

# Write the generated RSS feed to feed.xml with the XML declaration
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

print("✅ RSS feed updated successfully! Only video titles and links included.")
