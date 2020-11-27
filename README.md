Stitches together JPG images to create a stopmotion video.


Install all requirements with (modify as necessary for virtualenv or docker):
`pip3 install -r requirements.txt`


To run, issue the following command:


`python3 ./make_stopmotion.py --src ./testing/Killer\ Croc\ video/ --dst ~/Desktop/ --fps 72 --out KCROC.mp4`


To run suite of automated tests (make sure you didn't break anything!):

`pytest -sv ./testing/`
