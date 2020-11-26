#!/usr/bin/env python3
'''
Creates an m4v movie from multiple .jpg images. 
'''

import argparse
import datetime
import os
import sys


MIN_FPS     = 1
DEFAULT_FPS = 12
MAX_FPS     = 72

class ctx:
    """
    Empty class we use for saving context
    """
    def __init__(self, fps=DEFAULT_FPS, src=None, dst=None, name=None):
        self.fps = fps
        if src is None:
            src = os.getcwd()
        self.src = os.path.abspath(src)
        if dst is None:
            dst = os.getcwd()
        self.dst = os.path.abspath(dst)
        if name is None:
            name = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S.m4v')
        self.name = name

        assert MIN_FPS <= fps <= MAX_FPS, f"FPS must be between {MIN_FPS} and {MAX_FPS} (inclusive)" 
        assert os.path.isdir(self.src), f"Source directory {self.dst} does not exist."
        assert os.path.isdir(self.dst), f"Destination directory {self.dst} does not exist."
        self._get_files()

    def _get_files(self):
        self.files = sorted([ os.path.join(self.src, f) for f in os.listdir(self.src) if f.lower().endswith(".jpg") ])
        
    def __len__(self):
        return len(self.files)

    def __getattr__(self, name):
        if name == 'frame_duration':
            return 1 / self.fps
        elif name == 'movie_len':
            return self.__len__() / self.fps
        elif name == 'full_name':
            return os.path.join(self.dst, self.name)
        raise AttributeError(f"\'{self}\' has no attribute \'{name}\'")
    
    def generate_clip(self):
        # Import included here because it takes a while to load...
        from moviepy.editor import concatenate_videoclips, ImageClip
        clips = [ ImageClip(f).set_duration(self.frame_duration) for f in self.files ]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(self.full_name, fps=self.fps, codec='libx264')

def init():
    """
    Make sure we get the destination directory, the filename we want to save as, and
    how many frames per second we want. 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--fps", help="Number of images to create one second of video", type=int, default=12)
    parser.add_argument("--dst", help="Destination folder for completed movie")
    parser.add_argument("--src", help="Source folder for images")
    parser.add_argument("--out", help="Output Name", dest="output")
    res = parser.parse_args()
    return ctx(fps=res.fps, src=res.src, dst=res.dst, name=res.output)


if __name__ == "__main__":
    ctx = init()
    print(f"Creating a {ctx.movie_len} second long video from {len(ctx)} images: {ctx.full_name}")
    ctx.generate_clip()
    sys.exit(0)
