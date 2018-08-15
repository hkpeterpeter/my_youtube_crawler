from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import os, os.path, string

def format_filename(s):
    """ Source: https://gist.github.com/seanh/93666
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename

def crawlYouTube(url):

    yt = YouTube(url)

    print("video_id = %s" % yt.video_id)
    print("YouTube video title = %s" % yt.title)

    dirName = format_filename(yt.title)

    # Make a directory for the given title
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    # Apply operations in the sub-folder
    os.chdir(dirName)

    script_fname = format_filename("script.csv")
    if not os.path.exists(script_fname):
        # Grab the youtube transcript
        transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)

        # Prepare the csv content
        content = "start,duration,text\n"
        for item in transcript:
            content += str(item["start"]) + "," + str(item["duration"]) + "," + item["text"] + "\n"

        # Write the csv content
        text_file = open(script_fname, "w")
        text_file.write(content)
        text_file.close()
        print("%s downloaded" % script_fname)
    else:
        print("%s exists. Skip downloading" % script_fname)


    source_fname = format_filename("source.csv")
    if not os.path.exists(source_fname):
        content = ""
        content += "url,%s\n" % url
        content += "video_id,%s\n" % yt.video_id
        content += "title,%s\n" % yt.title
        content += "thumbnail_url,%s\n" % yt.thumbnail_url

        # Write the csv content
        text_file = open(source_fname, "w")
        text_file.write(content)
        text_file.close()
        print("%s downloaded" % source_fname)
    else:
        print("%s exists. Skip downloading." % source_fname)


    # Download the mp4
    mp4_name = format_filename("video")
    if not os.path.exists(mp4_name + ".mp4"):
        print("start downloading")
        yt.streams.first().download(filename=mp4_name)
        print("finish downloading")
    else:
        print("%s exists. Skip downloading." % mp4_name)

    os.chdir("..")


if __name__ == "__main__":
    batchMode = True

    # non-batch mode: testing
    url = "https://www.youtube.com/watch?v=S52rxZG-zi0"

    # batch mode
    youtube_list_fname = "youtube_list.txt"

    # Make a directory for the given title
    video_dir = "video"
    if not os.path.exists(video_dir):
        os.mkdir(video_dir)

    content = ""
    with open(youtube_list_fname) as f:
        content = f.readlines()

    os.chdir(video_dir)
    if batchMode == False:
        crawlYouTube(url)
    else:
            for url in content:
                crawlYouTube(url)
    os.chdir("..")