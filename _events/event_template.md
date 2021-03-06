---
title: Event Title
start: 1970-01-01T00:00
end: 1999-12-31T23:59
type: ctf
image: assets/events/event-image.jpg
facebook: http://facebook.com/facebook-link
sponsor: sponsor-id
location: Short Location
slack: slack-channel
hidden: true
---

This is a template for an event.

The full location can be included in this long
description, but the location field should only be a short name for the
location.

# Fields

* `title` is the name of the event.
* `start` and `end` are the end times of the event and **must** be in the form
  of `"%Y-%m-%dT%H%M"`.
* `type` is the event type and should be `"ctf"`, `"workshop"` or some other
  suitable descriptor
* `image` is the path from the root of the site to where thw image will be
  stored. The image is generated by the `event_images.py` script.
* `slack` is the slack channel name should not include the # and is optional.
* `facebook` should be a full URL for the facebook event and is optional.
* `sponsor` is the identifier for the sponsor from the `_data/sponsors.yaml`
  file and is optional.
