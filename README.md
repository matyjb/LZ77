# LZ77 encoder and decoder. 
By default tool decodes.

Usage: 
```
$ python LZ77.py [-h] [-e] [--csv] <input_path> <output_path>
```

#### positional arguments:
- `input_path`    path to input file
- `output_path`   path to output file (created if doesn't exist)

#### options:
- `-h` or `--help`    show this help message and exit
- `-e` or `--encode`  encode input file
- `--csv`         print statistics in csv format