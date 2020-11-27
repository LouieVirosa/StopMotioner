'''
All tests here are for verification of basic functionality of this project.
'''
import os

from moviepy.editor import VideoFileClip

from conftest import TLD, yellow_print, green_print
from stopmotion import StopMotionCTX #pylint: disable=import-error

LENGTH_MIN_ACCURACY = 0.1

def test_builds_correctly():
    '''
    This test ensures that a valid .mp4 video is created using images from the testing
    directory.
    '''
    src_dir = os.path.join(TLD, 'testing', 'Killer Croc video')
    dest_dir = "/tmp/"
    filename = "test_KROC.mp4"

    ctx = StopMotionCTX(src=src_dir, dst=dest_dir, name=filename)
    yellow_print(f"Creating a {ctx.movie_len:.2f} second movie at "
        f"{os.path.join(dest_dir, filename)}...")
    ctx.generate_clip()
    green_print("Created.")

    yellow_print(f"Verifying created video has correct duration ({ctx.movie_len:.2f}s)...")
    clip = VideoFileClip(ctx.full_name)
    duration = clip.duration
    clip.close()
    assert abs(duration - ctx.movie_len) < LENGTH_MIN_ACCURACY
    green_print("File is correct duration.")

    yellow_print("Removing created video...")
    assert os.remove(ctx.full_name) is None
    green_print("Video file removed.")
