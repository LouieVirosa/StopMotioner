#!/usr/bin/env python3
'''
Creates an m4v movie from multiple .jpg images. 
'''
import argparse

from stopmotion import stopmotion_ctx

def init():
    """
    Make sure we get the destination directory, the filename we want to save as, and
    how many frames per second we want. 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", help="Number of images to create one second of video", type=int)
    parser.add_argument("--dst", help="Destination folder for completed movie")
    parser.add_argument("--src", help="Source folder for images")
    parser.add_argument("--out", help="Output Name", dest="output")
    res = parser.parse_args()
    return stopmotion_ctx(fps=res.fps, src=res.src, dst=res.dst, name=res.output)


if __name__ == "__main__":
    ctx = init()
    print(f"Creating a {ctx.movie_len:.2f} second long video from {len(ctx)} images: {ctx.full_name}")
    ctx.generate_clip()
