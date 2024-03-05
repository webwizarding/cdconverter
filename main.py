import os
import mutagen
from pytube import YouTube
from moviepy.editor import VideoFileClip


def download_videos_from_file(file_path, folder_name='downloaded_videos'):
  """Download videos from YouTube links in a .txt"""
  create_directory_if_not_exists(folder_name)
  links = read_links_from_file(file_path)

  for link in links:
    download_video(link, folder_name)


def create_directory_if_not_exists(directory):
  """Create a directory if it does not already exist"""
  if not os.path.exists(directory):
    os.makedirs(directory)


def read_links_from_file(file_path):
  """Read YouTube video links from the .txt"""
  with open(file_path, 'r') as file:
    return [link.strip() for link in file.readlines()]


def download_video(link, output_path):
  """Download mp4 from a YouTube link."""
  try:
    yt = YouTube(link)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    print(f"Downloading: {yt.title}...")
    video.download(output_path=output_path)
    print(f"{yt.title} downloaded successfully!")
  except Exception as e:
    print(f"Failed to download {link}: {e}")


def convert_videos_to_audios(input_folder, output_folder='finished'):
  """Convert mp4's in a folder to mp3's"""
  create_directory_if_not_exists(output_folder)

  for file_name in os.listdir(input_folder):
    if file_name.endswith('.mp4'):
      convert_video_to_audio(file_name, input_folder, output_folder)


def convert_video_to_audio(file_name, input_folder, output_folder):
  """Convert the mp4 to mp3"""
  mp4_path = os.path.join(input_folder, file_name)
  mp3_path = os.path.join(output_folder,
                          os.path.splitext(file_name)[0] + ".mp3")
  try:
    print(f"Converting {file_name} to MP3...")
    video_clip = VideoFileClip(mp4_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()
    video_clip.close()
    print(f"{file_name} converted successfully!")
    verify_audio_file_integrity(mp3_path)
  except Exception as e:
    print(f"Failed to convert {file_name}: {e}")


def verify_audio_file_integrity(file_path):
  """Verify the integrity"""
  try:
    mutagen.File(file_path)
    print(f"{file_path} is a valid audio file.")
  except Exception as e:
    print(f"{file_path} is not a valid audio file: {e}")


if __name__ == "__main__":
  file_path = "links.txt"
  download_videos_from_file(file_path)
  convert_videos_to_audios('downloaded_videos')
