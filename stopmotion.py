#!/usr/bin/env python3
'''
Creates an m4v movie from multiple .jpg images. 
'''
import datetime
import os


MIN_FPS     = 1
DEFAULT_FPS = 12
MAX_FPS     = 72


class stopmotion_ctx:
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
        '''
        Updates the list of files that will be used to create the video.
        '''
        self.files = sorted([ os.path.join(self.src, f) for f in os.listdir(self.src) if f.lower().endswith(".jpg") ])
        
    def __len__(self):
        return len(self.files)

    @property
    def frame_duration(self):
            return 1 / self.fps
    
    @property
    def movie_len(self):
            return self.__len__() / self.fps

    @property
    def full_name(self):
            return os.path.join(self.dst, self.name)
    
    def generate_clip(self):
        assert len(self) > 0, "No suitable images found."

        # Import included here because it takes a while to load...
        from moviepy.editor import concatenate_videoclips, ImageClip
        clips = [ ImageClip(f).set_duration(self.frame_duration) for f in self.files ]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(self.full_name, fps=self.fps, codec='libx264')
