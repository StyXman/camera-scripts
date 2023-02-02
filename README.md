# camera-scripts
A set of gphoto2 based scripts to do several usefull stuff with cameras (lens tests, bulb shots, etc)

## Motivation

https://www.bhphotovideo.com/explora/photography/tips-and-solutions/how-test-your-lens

TL;DR: set up a test target, put the camera on a tripod so the target fills the view, take pictures at different appertures. 

## What's here

This repo contains two things so far:

* A SVG test target that you can print on an A3 page. I chose A3 because that fills the view of a 18mm-on-APS-C (so ~28mm full frame equivalent) at a good distance ~1m, IIRC).

* A python script that iterates over all f-stops between f/3.5 and f/11.

It also supports zoom lenses, because it asks you the focal length you're taking pictures in, goes over the f-stops, and asks you again, so you could change the focal length, reposition the tripod, and go over the f-stops again and so on. I used it to test a 18-140mm and 18-200mm.

## TODO

I have more gphoto2 based scripts, and one for stacking photos. One day...
