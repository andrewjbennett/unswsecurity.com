#!/usr/bin/env python2

"""
This uses the YAML frontmatter from events to create pretty images to display
event details on the site and as header files for facebook.

This script depends on pyYAML and Pillow.

Author: Curtis Millar <curtis@unswsecurity.com>

Copyright 2017 Curtis Millar.

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""

from yaml import load as yml_load
from os import listdir
from os.path import isfile, join as path_join, getmtime
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

### CONSTANTS ###
EVENTS_DIR = "./_events"

FONTS_DIR  = "/usr/share/fonts"
FIRA_MONO  = ImageFont.truetype(path_join(FONTS_DIR, "fira/FiraMono-Medium.otf"), 22)
FIRA_SANS  = ImageFont.truetype(path_join(FONTS_DIR, "fira/FiraSans-Medium.otf"), 22)
MONTSERRAT = path_join(FONTS_DIR, "julietaula-montserrat/Montserrat-Bold.ttf")
MONTSERRAT_TITLE = ImageFont.truetype(MONTSERRAT, 88)
MONTSERRAT_DATE  = ImageFont.truetype(MONTSERRAT, 72)

IMAGE_DIR     = "./assets/img"
CTF_BACK      = path_join(IMAGE_DIR, "ctf_back.png")
WORKSHOP_BACK = path_join(IMAGE_DIR, "workshop_back.png")
MISC_BACK     = path_join(IMAGE_DIR, "event_back.png")

ARC_LOGO    = "assets/arc-wob.png"
LOGO_SCALE  = 4
LOGO_AFFINE = (LOGO_SCALE, 0, 0, 0, LOGO_SCALE, 0)

def frontmatter(fd):
    """Load the frontmatter of a given file"""
    matter = ""
    start = False

    for line in fd:
        if start:
            if line.startswith("---"):
                break
            else:
                matter += line
        elif line.startswith("---"):
            start = True


    return matter

def get_events():
    """ Get a list of all site events. Includes event file iand image create
    times"""

    events = {}

    for file_name in listdir(EVENTS_DIR):
        if file_name.endswith(".md"):
            path = path_join(EVENTS_DIR, file_name)
            event = yml_load(frontmatter(file(path)))

            event_id = file_name[:-len(".md")]

            event["mtime"] = getmtime(path)

            # check for image
            if "image" in event:
                img_path = event["image"]
                if isfile(img_path):
                    event["img_mtime"] = getmtime(img_path)
                    event["img_old"] = event["mtime"] > event["img_mtime"]
                else:
                    event["img_old"] = True

            events[event_id] = event

    return events

def get_background(event):
    """Get the background image for an event"""
    image_path = MISC_BACK

    if "type" in event:
        if event["type"] == "ctf":
            image_path = CTF_BACK
        elif event["type"] == "workshop":
            image_path = WORKSHOP_BACK

    image = Image.open(image_path)

    return image

def get_logo():
    """Get a sensibly sized ARC logo"""

    logo = Image.open(ARC_LOGO)
    logo_size = (logo.size[0] / LOGO_SCALE, logo.size[1] / LOGO_SCALE)

    return logo.transform(logo_size, Image.AFFINE, LOGO_AFFINE)

def date_string(original):
    """Get a pretty date string"""
    date = datetime.strptime(original, "%Y-%m-%dT%H:%M")
    return date.strftime("%A, %-d %B %Y")

def center(image_size, block_size):
    return tuple([(image_size[n] - block_size[n]) / 2 for n in xrange(len(image_size))])

def shift(position, displace):
    return (position[0] + displace[0], position[1] + displace[1])

def render_header(event):
    image = get_background(event)
    draw = ImageDraw.Draw(image)

    # Get event title
    title_text = event["title"].upper()
    title_size = MONTSERRAT_TITLE.getsize(title_text)
    title_pos = shift(center(image.size, title_size), (0, -96))
    draw.text(title_pos, title_text, font=MONTSERRAT_TITLE)

    # Get event date
    date_text = date_string(event["start"])
    date_size = MONTSERRAT_DATE.getsize(date_text)
    date_pos = shift(center(image.size, date_size), (0, 32))
    draw.text(date_pos, date_text, font=MONTSERRAT_DATE)

    # Add logo
    logo = get_logo()
    logo_pos = (image.size[0] - logo.size[0] - 24,
                image.size[1] - logo.size[1] - 24)
    image.paste(logo, logo_pos)

    image.save(event["image"])


if __name__ == "__main__":

    events = get_events()

    for event_id in events:
        event = events[event_id]
        print "Checking event: {}".format(event_id)
        print "{} - {}".format(event["title"], date_string(event["start"]))
        if "image" in event and event["img_old"]:
            print "Creating header..."
            render_header(event)
        print


