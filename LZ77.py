from argparse import ArgumentParser
import os

# in bytes
DICT_BUFFER_SIZE = 256
LOOK_AHEAD_BUFFER_SIZE = 15

def decode2TripletsFrom5Bytes(b):
  tri1 = (
    b[0],
    (b[1] & 0xF0) >> 4,
    (b[1] & 0x0F) << 4 | (b[2] & 0xF0) >> 4
    )
  tri2 = (
    (b[2] & 0x0F) << 4 | (b[3] & 0xF0) >> 4, 
    b[3] & 0x0F, 
    b[4]
    )
  return [tri1,tri2]

def decodeFile(filepath, outputFilepath):
  inputfile = open(filepath,"rb")
  outputfile = open(outputFilepath,"wb")

  triplets = []
  tmpstack = []
  for byte in inputfile.read():
    tmpstack.append(byte)
    # gdy mamy już odczytanych 5 bajtów możemy je rozkodować
    if(len(tmpstack) == 5):
      for t in decode2TripletsFrom5Bytes(tmpstack):
        triplets.append(t)
      del tmpstack[:]
  
  outputfile.write(bytes(decode(triplets)))

  inputfile.close()
  outputfile.close()

def encode2TripletsTo5Bytes(tri1, tri2):
  return bytes([
    tri1[0] & 0xFF,
    (tri1[1] & 0x0F) << 4 | (tri1[2] & 0xF0) >> 4,
    (tri1[2] & 0x0F) << 4 | (tri2[0] & 0xF0) >> 4,
    (tri2[0] & 0x0F) << 4 | (tri2[1] & 0x0F),
    tri2[2] & 0xFF
  ])


def encodeFile(filepath, outputFilepath):
  inputfile = open(filepath,"rb")
  outputfile = open(outputFilepath,"wb")

  tmpstack = []
  for triplet in encode(inputfile.read()):
    tmpstack.append(triplet)
    if(len(tmpstack) == 2):
      # can be saved
      outputfile.write(encode2TripletsTo5Bytes(tmpstack[0],tmpstack[1]))
      del tmpstack[0]
      del tmpstack[0]
    
  # spr czy w stacku cos nie zostalo
  if(len(tmpstack) != 0):
    outputfile.write(encode2TripletsTo5Bytes(tmpstack[0],(0,0,0)))

  inputfile.close()
  outputfile.close()

#stream w postaci listy znakow (string)
def encode(stream):
  index = 0
  while(len(stream) > index):
    matching = 0
    offset = 0

    didbreak = False
    while(matching < LOOK_AHEAD_BUFFER_SIZE and index + matching < len(stream)):
      dict_start_index = 0 if index-DICT_BUFFER_SIZE+1 < 0 else index-DICT_BUFFER_SIZE+1
      v = stream.rfind(stream[index:index+matching+1],dict_start_index,index)
      if(v == -1):
        yield (offset,matching,stream[index+matching])
        didbreak = True
        break
      else:
        matching += 1
        offset = index - v

    # slowo powtorzone jest tak dlugie jak LOOK_AHEAD_BUFFER_SIZE lub doszło do końca pliku
    # zmniejszamy to slowo o 1 by nie pobrać znaku z poza LOOK_AHEAD_BUFFER lub z poza pliku
    if(not didbreak):
      yield (offset,matching-1,stream[index+matching-1])
      index += matching
    else:
      index += matching + 1

#przyjmuje liste krotek postaci (offset, characters_matching, character_not_matched)
def decode(stream):
  dict_buffer = [0] * DICT_BUFFER_SIZE
  for tri in stream:
    offset = tri[0]
    matching = tri[1]
    lastchar = tri[2]

    index = len(dict_buffer)-offset
    for i in range(matching):
      # print(index)
      dict_buffer.append(dict_buffer[index])
      yield dict_buffer[-1]
      if(len(dict_buffer) > DICT_BUFFER_SIZE):
        del dict_buffer[0]
    
    dict_buffer.append(lastchar)
    yield lastchar
    if(len(dict_buffer) > DICT_BUFFER_SIZE):
      del dict_buffer[0]
    
def main():
  parser = ArgumentParser(description='Tool for lz77 encoding and decoding. By default tool decodes.')
  parser.add_argument("input_path", nargs=1, help='Path to input file')
  parser.add_argument("output_path", nargs=1, help='Path to output file (created if doesn\'t exist)')
  parser.add_argument('-e', '--encode', action='store_true', help='Encode input file')
  parser.add_argument('--csv', action='store_true', help='Print statistics in csv format')
  args = parser.parse_args()
  
  if(args.encode):
    encodeFile(args.input_path[0],args.output_path[0])
  else:
    decodeFile(args.input_path[0],args.output_path[0])

  size_in = os.stat(args.input_path[0]).st_size
  size_out = os.stat(args.output_path[0]).st_size
  cr = size_in / size_out
  cp = 1-(1/cr)
  br = 1/ cr * 8
  if(args.csv):
    print(args.input_path[0],args.output_path[0],size_in,size_out,cr,cp,br, sep=";")
  else:
    w = "Encoded:" if(args.encode) else "Decoded:"
    print(w,args.input_path[0],"(",size_in,"B ) to",args.output_path[0],"(",size_out,"B )","\t","CR = {:.3f}".format(cr),"CP = {:.3%}".format(cp),"BR = {:.3f}".format(br))


if __name__ == "__main__":
    main()