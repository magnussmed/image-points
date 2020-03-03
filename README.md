# Point
Small python script that detects colors on a photo.<br>
The script will draw lime-green pointers displayed where it has detected colored pixels.<br>See down below for usage information!

## Installation and usage
Project is written in python 3.7 and using `pip` for python dependency management.

Install all required runtime dependencies with following commands:

```bash
pip install pillow
pip install opencv-python
pip install opencv-python-headless
```

Run the script in your terminal:
```bash
python ./point.py
```
After a few seconds depending on image size, a drawed image will popup as result.
<br><br>
You can find test images in assets/img folder. You are more than welcome to add more images!

## Tips
It is possible to change the outcome by increasing or decreasing the sentiment percentage from 0-1. As default it is set to 0.25
<br><br>
If you need the point coordinates, simply uncomment the point found print statement.
