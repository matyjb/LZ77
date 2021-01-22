# def bits(f):
#   bytes = (ord(b) for b in f.read())
#   print(list(bytes))
#   for b in bytes:
#     for i in reversed(range(8)):
#       yield (b >> i) & 1

# in bytes
DICT_BUFFER_SIZE = 7
LOOK_AHEAD_BUFFER_SIZE = 6

def encode(stream):
  index = 0
  matching = 0
  offset = 0
  while(len(stream) > index):
    matching = 0
    offset = 0
    for i in range(LOOK_AHEAD_BUFFER_SIZE):
      schar = stream[index:index+i+1]
      buffer_start_index = 0 if index-DICT_BUFFER_SIZE < 0 else index-DICT_BUFFER_SIZE
      v = stream.find(schar,buffer_start_index,index+i)
      
      if(v == -1):
        yield (offset, matching, schar[-1])
        break
      else:
        matching += 1
        offset = index-v

    index += matching+1

def decode(stream):
  output = ""
  for tri in stream:
    offset = tri[0]
    matching = tri[1]
    lastchar = tri[2]
    index = len(output)-offset
    for i in range(matching):
      output += output[index+i]
    output += lastchar
    
  return output

def main():
  file = open("test.txt")
  text = file.read()
  print(text)
  e = list(encode(text))
  print(e)
  d = decode(e)
  print(d)
  print(text == d)
  pass


if __name__ == "__main__":
    main()