#!/usr/bin/env python3

import argparse
import datetime
import os
import sys

from moviepy.editor import *

class ctx:
    """
    Empty class we use for saving context
    """
    pass

def init_argparser(ctx):
    """
    Make sure we get the destination directory, the filename we want to save as, and
    how many frames per second we want. 
    """
    default_name = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S.m4v')
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", help="Number of images to create one second of video", type=int, default=12)
    parser.add_argument("--dst", help="Destination folder for completed movie", default=os.getcwd())
    parser.add_argument("--src", help="Source folder for images", default=os.getcwd())
    parser.add_argument("--out", help="Output Name", dest="output", default=default_name)
    res = parser.parse_args()

    if not os.path.isdir(res.src):
        parser.print_help(sys.stderr)
        print("\n--src directory specified does not exist.\n")
        sys.exit(1)
    
    if not os.path.isdir(res.dst):
        parser.print_help(sys.stderr)
        print("\n--dst directory specified does not exist.\n")
        sys.exit(1)
   
    if res.fps > 72 or res.fps < 1:
        parser.print_help(sys.stderr)
        print("\n--fps must be an integer within 1 and 72, inclusive.\n")
        sys.exit(1)
        
         
    ctx.fps = res.fps
    ctx.dst = res.dst
    ctx.src = res.src
    ctx.name = res.output


if __name__ == "__main__":
    ctx = ctx()
    init_argparser(ctx)
    
    name = os.path.join(ctx.dst, ctx.name)
    duration = 1 / ctx.fps

    files = sorted([os.path.join(ctx.src,f) for f in os.listdir(ctx.src) if f.endswith(".jpg") or f.endswith(".JPG")])
    if len(files) < 1:
        print("No images ending in .jpg found in src directory.")
        sys.exit(1)

    clips = [ImageClip(f).set_duration(duration) for f in files]    

    final_clip = concatenate_videoclips(clips)
    
    num_imgs = len(files)
    print("Found %d images." % num_imgs)
    print("Creating a %f second long video: %s" % (num_imgs/ctx.fps, name))

    final_clip.write_videofile(name, fps=ctx.fps, codec='libx264')
             
    sys.exit(0)
