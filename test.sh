echo "encoding"
python LZ77.py -e --csv input/icing.wav lz77/icing.wav.lz77
python LZ77.py -e --csv input/song.wav lz77/song.wav.lz77
python LZ77.py -e --csv input/img1.bmp lz77/img1.bmp.lz77
python LZ77.py -e --csv input/piesel.jpg lz77/piesel.jpg.lz77
python LZ77.py -e --csv input/tenor.png lz77/tenor.png.lz77
python LZ77.py -e --csv input/ogromny.png lz77/ogromny.png.lz77
python LZ77.py -e --csv input/lorem.txt lz77/lorem.txt.lz77
python LZ77.py -e --csv input/pantadeusz.txt lz77/pantadeusz.txt.lz77
python LZ77.py -e --csv input/lokomotywa.txt lz77/lokomotywa.txt.lz77
echo "decoding"
python LZ77.py -d --csv lz77/icing.wav.lz77 decoded/icing.wav.lz77.wav
python LZ77.py -d --csv lz77/song.wav.lz77 decoded/song.wav.lz77.wav
python LZ77.py -d --csv lz77/img1.bmp.lz77 decoded/img1.bmp.lz77.bmp
python LZ77.py -d --csv lz77/piesel.jpg.lz77 decoded/piesel.jpg.lz77.jpg
python LZ77.py -d --csv lz77/tenor.png.lz77 decoded/tenor.png.lz77.png
python LZ77.py -d --csv lz77/ogromny.png.lz77 decoded/ogromny.png.lz77.png
python LZ77.py -d --csv lz77/lorem.txt.lz77 decoded/lorem.txt.lz77.txt
python LZ77.py -d --csv lz77/pantadeusz.txt.lz77 decoded/pantadeusz.txt.lz77.txt
python LZ77.py -d --csv lz77/lokomotywa.txt.lz77 decoded/lokomotywa.txt.lz77.txt