#! /usr/local/bin/python3

import datetime
import os

from moviepy.editor import *
from shutil import copyfile

# Paths to relevant Dropbox locations
base_path = "/Users/louieearle/Dropbox/Movie_Editing/"
input_path = os.path.join(base_path, "Input")
processing_path = os.path.join(base_path, "Processing")
output_path = os.path.join(base_path, "Output")
constants_path = os.path.join(base_path, "Constants")

def create_intro(title_text="", subtitle_text=""):
    """
    Returns a CompositeVideoClip of the title background, with any 
    titles or subtitles passed in animated on it.
    """
    background = ImageClip(os.path.join(constants_path, "Louie_Logo_1.png")).set_duration(3.5)

    x_center = 1920 / 2
    y_center = 1080 / 2

    clips = [background]
    titles_exist = False

    if len(title_text) > 0:
        titles_exist = True
        title = TextClip(title_text, font='MKXTitle', fontsize=200, color='white').set_duration(2.5)
        title_width = title.size[0]
        title_x = int(x_center - title_width / 2)
        title_pos = (title_x, y_center)
        clips.append(title.set_pos(title_pos).set_start(1).crossfadein(0.5))

    if len(subtitle_text) > 0:
        titles_exist = True
        subtitle = TextClip(subtitle_text, fontsize = 75, color = 'white').set_duration(1.5)
        subtitle_width = subtitle.size[0]
        subtitle_x = int(x_center - subtitle_width / 2)
        subtitle_pos = (subtitle_x, y_center + 200)
        clips.append(subtitle.set_pos(subtitle_pos).set_start(2).crossfadein(0.5))

    # If we have no title or subtitle, shorten the length to 2 seconds
    if not titles_exist:
        clips[0].set_duration(2)

    background_txt = CompositeVideoClip(clips) 
    background_txt.add_mask()
    background_txt.crossfadein(0.5)
    background_txt.crossfadeout(0.5)

    fade_final = CompositeVideoClip([background, background_txt])
    #fade_final.write_videofile('/Users/louieearle/Desktop/logo_dynamic.mp4', codec='libx264', fps=24)
    return fade_final

def get_new_files():
    """
    Checks the Dropbox Input directory for any new files. If found, creates a new directory
    in the processing directory, moves the files in there, and creates a JSON manifest.
    """

    title = "title.txt"
    subtitle = "subtitle.txt"

    files = []
    files = [f for f in os.listdir(input_path) if f.endswith(".mp4")]
    print("Found files: %s" % files)
    
    if len(files) > 0:
        # Add title and subtitle if they are there.
        if title in os.listdir(input_path):
            files.append(title)
        if subtitle in os.listdir(input_path):
            files.append(subtitle)

        # Create a new directory with current timestamp
        current_time = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
        working_dir_path = os.path.join(processing_path, current_time)
        os.makedirs(working_dir_path)

        # Move all files into this new working directory
        clips = []
        for file in sorted(files):
            video_file = os.path.join(working_dir_path, file)
            os.rename(os.path.join(input_path, file),
                video_file)
            if video_file.endswith(".mp4"):
                clips.append(VideoFileClip(video_file))

        # Concatenate all valid files
        # TODO: write a JSON file instead, with everything imported
        # by creation date

        # Create a layered video file from all clips. If clips are > 0.5 seconds, they will be cross-
        # faded in to prevent abrupt transitions.
        final_clips = []
        
        # Add an intro
        #logo_1 = ImageClip(os.path.join(constants_path, "Louie_Logo_1.png")).set_duration(2)
        #logo_2 = ImageClip(os.path.join(constants_path, "Louie_Logo_2.png")).set_duration(2)
        #final_clips.append(logo_1.fadein(0.3))
        #final_clips.append(logo_2.set_start(1.5).crossfadein(.5))
        
        title_text = ""
        subtitle_text = ""

        # Try to open title file (if one exists)
        try:
            with open(os.path.join(working_dir_path, 'title.txt'), 'r') as titlefile:
                title_text = titlefile.readline()

        except   FileNotFoundError:
            pass

        # Try to open subtitle file (if one exists)
        try:
            with open(os.path.join(working_dir_path, 'subtitle.txt'), 'r') as subtitlefile:
                subtitle_text = subtitlefile.readline()

        except   FileNotFoundError:
            pass

        print("Title: %s" % title_text)
        print("Subtitle: %s" % subtitle_text)

        final_clips.append(create_intro(title_text, subtitle_text))

        # Add in the movies...
        start_time = 3.5
        fade_in = 0.5
        for clip in clips:
            final_clips.append(clip.set_start(start_time).crossfadein(fade_in))
            start_time += clip.duration
            if clip.duration > fade_in:
                start_time -= fade_in

        # Fade out the last video
        last_clip = final_clips.pop()
        final_clips.append(last_clip.fadeout(0.4))        

        final_movie = CompositeVideoClip(final_clips)

        # May not be necessary...
        final_height = clips[0].size[0]
        final_width = clips[0].size[1]
        final_movie.resize((final_width, final_height))     

        # Write the file to the output directory
        output_file = os.path.join(output_path, current_time + ".mp4")
        print("Will write output file to %s." % output_file) 
        final_movie.write_videofile(output_file, codec='libx264')


if __name__ == "__main__":
    get_new_files()
