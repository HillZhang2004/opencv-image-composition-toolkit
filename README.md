# OpenCV Image Composition Toolkit

Small OpenCV toolkit for compositing RGBA elements onto RGB backgrounds using alpha blending. Implements aspect ratio preserving resize, normalized placement, and edge safe clipping.

## What it does
* Crops an element to the minimal nonzero alpha bounding box
* Resizes the element so the bounding box height matches a normalized target height
* Places the element by aligning the bounding box center to a normalized (x, y) location
* Alpha blends the element into the background
* Clips safely when the element extends beyond image boundaries

## Core function
`place_object(bkg_img, element, elmask, location, height)`

Inputs
* `bkg_img`: RGB background image
* `element`: RGB element image
* `elmask`: alpha mask for the element, values in 0 to 255
* `location`: normalized (x, y) location for the element bounding box center
* `height`: normalized height of the element bounding box relative to background height

Output
* New RGB image in uint8 with the composite result

## Requirements
* Python
* numpy
* opencv python

## Notes
This repo contains the core compositing logic only. Example assets are not included.
