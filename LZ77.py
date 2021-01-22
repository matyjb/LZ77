# def bits(f):
#   bytes = (ord(b) for b in f.read())
#   print(list(bytes))
#   for b in bytes:
#     for i in reversed(range(8)):
#       yield (b >> i) & 1

# in bytes
DICT_BUFFER_SIZE = 7
LOOK_AHEAD_BUFFER_SIZE = 6

def encodeFile(filepath, outputFilepath):
  
  pass


#przyjmuje stream w postaci ciagu znakow
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
        # print((offset,matching,stream[index+matching]))
        yield (offset,matching,stream[index+matching])
        didbreak = True
        break
      else:
        matching += 1
        offset = index - v

    if(not didbreak):
      yield (offset,matching,'')

    index += matching + 1

#przyjmuje liste krotek postaci (offset, characters_matching, character_not_matched)
def decode(stream):
  dict_buffer = [''] * DICT_BUFFER_SIZE
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
  text = "abracadabrarray"
  print("######################", text)
  d = list(decode(list(encode(text))))
  print(text == ''.join(d))
  for f in ["test.txt","test2.txt","test3.txt"]:
    print("######################", f)
    file = open(f)
    text = file.read()
    d = list(decode(list(encode(text))))
    print(text == ''.join(d))
    file.close()
    pass


if __name__ == "__main__":
    main()