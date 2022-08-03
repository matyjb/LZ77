echo "encoding"
python LZ77.py -e --csv input/icing.wav lz77/icing.wav.lz77
python LZ77.py -e --csv input/song.wav lz77/song.wav.lz77

python LZ77.py -e --csv input/img1.bmp lz77/img1.bmp.lz77
python LZ77.py -e --csv input/lena.png lz77/lena.png.lz77
python LZ77.py -e --csv input/moon.jpg lz77/moon.jpg.lz77

python LZ77.py -e --csv input/pantadeusz.txt lz77/pantadeusz.txt.lz77
python LZ77.py -e --csv input/lokomotywa.txt lz77/lokomotywa.txt.lz77
echo "decoding"
python LZ77.py --csv lz77/icing.wav.lz77 decoded/icing.wav.lz77.wav
python LZ77.py --csv lz77/song.wav.lz77 decoded/song.wav.lz77.wav

python LZ77.py --csv lz77/img1.bmp.lz77 decoded/img1.bmp.lz77.bmp
python LZ77.py --csv lz77/lena.png.lz77 decoded/lena.png.lz77.png
python LZ77.py --csv lz77/moon.jpg.lz77 decoded/moon.jpg.lz77.jpg

python LZ77.py --csv lz77/pantadeusz.txt.lz77 decoded/pantadeusz.txt.lz77.txt
python LZ77.py --csv lz77/lokomotywa.txt.lz77 decoded/lokomotywa.txt.lz77.txt