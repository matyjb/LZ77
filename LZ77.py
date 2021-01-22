# in bytes
DICT_BUFFER_SIZE = 7
LOOK_AHEAD_BUFFER_SIZE = 6

def decodeTripletFrom3Bytes(b, offsettedByHalfByte=False):
  if(offsettedByHalfByte):
    return (
      (b[0] & 0x0F) << 4 | (b[1] & 0xF0) >> 4, 
      b[1] & 0x0F, 
      b[2]
      )
  else:
    return (
      b[0],
      (b[1] & 0xF0) >> 4,
      (b[1] & 0x0F) << 4 | (b[2] & 0xF0) >> 4
    )
  

def decodeFile(filepath, outputFilepath):
  inputfile = open(filepath,"rb")
  outputfile = open(outputFilepath,"wb")

  triplets = []
  tmpstack = []
  offsetted = False
  byte = inputfile.read(1)
  while(byte):
    tmpstack.append(byte[0])
    if(len(tmpstack) == 3):
      print(tmpstack)
      triplets.append(decodeTripletFrom3Bytes(tmpstack, offsetted))
      if(offsetted):
        inputfile.seek(-1,1) #cofnij sie o jeden bajt
      offsetted = not offsetted
      del tmpstack[:]

    byte = inputfile.read(1)
    
  bajty = bytes(decode(triplets))
  outputfile.write(bajty)

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
      dict_start_index = 0 if index-DICT_BUFFER_SIZE < 0 else index-DICT_BUFFER_SIZE
      v = stream.find(stream[index:index+matching+1],dict_start_index,index)
      if(v == -1):
        yield (offset,matching,stream[index+matching])
        didbreak = True
        break
      else:
        matching += 1
        offset = index - v

    if(not didbreak):
      yield (offset,matching,0)

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
      dict_buffer.append(dict_buffer[index])
      yield dict_buffer[-1]
      if(len(dict_buffer) > DICT_BUFFER_SIZE):
        del dict_buffer[0]
    
    dict_buffer.append(lastchar)
    yield lastchar
    if(len(dict_buffer) > DICT_BUFFER_SIZE):
      del dict_buffer[0]
    
def main():
  # text = "abracadabrarray"
  # t = [(6,12,2),(3,11,195)]
  # e = encode2TripletsTo5Bytes(t[0],t[1])
  # print([ee for ee in e])
  # print(decode2TripletsFrom5Bytes(e))
  # print("######################", text)
  # d = list(decode(list(encode(text))))
  # print(text == ''.join(d))
  for f in ["test.txt","test2.txt","test3.txt"]:
    print("######################", f)
    encodeFile(f,f+".lz77")
    decodeFile(f+".lz77",f+".lz77.txt")
    pass


if __name__ == "__main__":
    main()