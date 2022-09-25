import argparse
import subprocess
import shutil
import os
import glob
from ocr import parse_frames

parser = argparse.ArgumentParser(description='Cut Haluatko miljonääriksi')
parser.add_argument("-i", dest="input", required=True,
                    help="input file", metavar="FILE")
parser.add_argument("-o", dest="output", required=True,
                    help="output file", metavar="FILE")
parser.add_argument("--temp", dest="temp", default="frames/",
                    help="temporary folder for ffmpeg extracted frames", metavar="FILE")

args = parser.parse_args()
frames_folder = args.temp
if not frames_folder.endswith('/'):
    frames_folder += '/'

# files = glob.glob(f'{frames_folder}*')
# for f in files:
#     os.remove(f)

# subprocess.call(f"ffmpeg -i {args.input} -vf fps=0.5 {frames_folder}out%d.png")

parse_frames(frames_folder)
