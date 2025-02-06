import os
import json
import xml.etree.ElementTree as ET

# Create the RSS root element with version 2.0 and declare the Atom namespace.
rss = ET.Element("rss", version="2.0", attrib={"xmlns:atom": "http://www.w3.org/2005/Atom"})

# Create the channel element with required metadata.
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Build with GenAI - Video Feed"
ET.SubElement(channel, "link").text = "https://github.com/victordelrosal/buildwithGenAI"
ET.SubElement(channel, "description").text = "Latest video updates"

# Add the recommended atom:link element for self-reference.
atom_link = ET.SubElement(channel, "{http://www.w3.org/2005/Atom}link")
atom_link.set("href", "https://raw.githubusercontent.com/victordelrosal/buildwithGenAI/main/feed.xml")
atom_link.set("rel", "self")
atom_link.set("type", "application/rss+xml")

# Process each JSON file in the "videos" directory.
video_dir = "videos"
for filename in sorted(os.listdir(video_dir), reverse=True):
    if filename.endswith(".json"):
        with open(os.path.join(video_dir, filename), "r") as f:
            video = json.load(f)
        # Create an <item> that includes only <title> and <link>.
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = video["title"]
        ET.SubElement(item, "link").text = f"https://www.youtube.com/watch?v={video['id']}"
        # Add a <guid> element (recommended for duplicate detection)
        ET.SubElement(item, "guid").text = f"https://www.youtube.com/watch?v={video['id']}"

# Write the RSS feed to file with an XML declaration.
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

print("✅ RSS feed updated successfully!")
