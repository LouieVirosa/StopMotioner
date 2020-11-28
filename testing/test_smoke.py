'''
All tests here are for verification of basic functionality of this project.
'''
import os
import random

from moviepy.editor import VideoFileClip
import pytest

from conftest import TLD, yellow_print, green_print
from stopmotion import StopMotionCTX, MIN_FPS, MAX_FPS #pylint: disable=import-error

LENGTH_MIN_ACCURACY = 0.1

def test_builds_correctly():
    '''
    This test ensures that a valid .mp4 video is created using images from the testing
    directory.
    '''
    src_dir = os.path.join(TLD, 'testing', 'Killer Croc video')
    dest_dir = "/tmp/"
    filename = "test_KROC.mp4"

    fps = random.randrange(MIN_FPS, MAX_FPS + 1)
    ctx = StopMotionCTX(src=src_dir, dst=dest_dir, fps=fps, name=filename)
    yellow_print(f"Creating a {ctx.movie_len:.2f} second movie at {ctx.fps} fps: "
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


def test_throw_errors():
    '''
    This test ensures that exceptions are raised if we try to create a stopmotion context
    with bad params
    '''
    non_existing_dir = "/DOESNOTEXIST/"
    assert not os.path.isdir(non_existing_dir)

    yellow_print("Attempting to create StopMotionCTX with invalid source dir...")
    with pytest.raises(AssertionError):
        StopMotionCTX(src=non_existing_dir)
    green_print("Threw exception (expected)")

    yellow_print("Attempting to create StopMotionCTX with invalid dest dir...")
    with pytest.raises(AssertionError):
        StopMotionCTX(dst=non_existing_dir)
    green_print("Threw exception (expected)")

    yellow_print("Attempting to create StopMotionCTX with FPS too low...")
    with pytest.raises(AssertionError):
        StopMotionCTX(fps=MIN_FPS - 1)
    green_print("Threw exception (expected)")

    yellow_print("Attempting to create StopMotionCTX with FPS too high...")
    with pytest.raises(AssertionError):
        StopMotionCTX(fps=MAX_FPS + 1)
    green_print("Threw exception (expected)")
