# Landmark trials

Educational reference of practice-changing trials in hematologic malignancies, created by Andres Ferber, MD, with the assistance of Claude (Anthropic). Content is updated monthly.

## How it works

- `topics.json` lists the topics shown. Sections appear in the order listed; "group" (Lymphoma, Myeloma) sets the group label and colour.
- `topics/<key>.html` holds each topic's self-contained content.
- `loader.js` builds the accordion on any page that includes:

```html
<div id="landmark-trials"></div>
<script src="https://USERNAME.github.io/landmark-trials/loader.js"></script>
```

- `index.html` is a standalone page showing the same content.

## Adding a topic

Add `topics/<key>.html` (generated with `tools/to_weebly.py` from the topic's page) and a matching entry in `topics.json`. The website picks it up automatically.

## Backup of the previous website setup

The files in `topics/` are the same self-contained embeds used before this setup. To go back to one Weebly section per topic, paste a topic file's full contents into that section's Embed Code element.
