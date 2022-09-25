Clear frames folder

```
del /q ".\\frames\\*"
```

Output image every 1 / fps = 2 seconds

```
ffmpeg -i episodes/s05e16.mkv -vf fps=0.5 frames/out%d.png
```

Install tesseract & python libraries

```
pip install pillow
pip install pytesseract
pip install opencv-python
```
