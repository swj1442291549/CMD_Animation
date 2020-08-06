#!/bin/bash

ffmpeg -r 1/1 -i cmd%02d.png -c:v libx264 -r 30 out.mp4   
