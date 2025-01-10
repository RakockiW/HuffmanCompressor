import sys

class Node:
  
  """
  Klasa reprezentująca węzeł drzewa
  """

  def __init__(self, label, freq):
    self.label = label
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq
  
  def __eq__(self, other):
    if (other == None):
      return False
    if (not isinstance(other, Node)):
      return False
    return self.freq == other.freq
    

class PriorityQueue:

  """
  Klasa reprezentująca kolejke priorytetową
  """

  def __init__(self):
      self.heap = []

  def heapify(self, index):

    """
    Utrzymuje własność kopca w drzewie, modyfikując jeśli to konieczne.
    """

    left = 2 * index + 1
    right = 2 * index + 2
    smallest = index

    if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
        smallest = left

    if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
        smallest = right

    if smallest != index:
        self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
        self.heapify(smallest)

  def insert(self, node):

    """
    Wstawia węzeł do kopca, utrzymując własność kopca.
    """

    self.heap.append(node)
    index = len(self.heap) - 1

    while index > 0 and self.heap[(index - 1) // 2] > self.heap[index]:
        self.heap[(index - 1) // 2], self.heap[index] = self.heap[index], self.heap[(index - 1) // 2]
        index = (index - 1) // 2

  def extract_min(self):

    """
    Usuwa i zwraca węzeł z minimalną wartością z kopca.
    """

    if self.is_empty():
        raise IndexError("extract_min() called on empty heap")

    min_node = self.heap[0]
    self.heap[0] = self.heap[-1]
    self.heap.pop()
    self.heapify(0)

    return min_node

  def peek(self):

    """
    Zwraca węzeł z minimalną wartością z kopca, nie usuwając go.
    """

    if self.is_empty():
        raise IndexError("peek() called on empty heap")
    return self.heap[0]

  def is_empty(self):

    """
    Sprawdza, czy kopiec jest pusty.
    """

    return len(self.heap) == 0

  def size(self):
      return len(self.heap)

class Compression:
  def __init__(self):

    """
    Inicjalizuje obiekt klasy Compression, tworząc pustą kolejkę priorytetową.
    """

    self.q = PriorityQueue()

  def get_text(self, filename):

    """
    Czyta z pliku o podanej nazwie i zwraca zawartość tekstu.
    """

    with open(filename, "r") as file:
      text = file.read()

    return text

  def count_occurrences(self, text):

    """
    Liczy wystąpienia każdego znaku w tekście i zwraca słownik.
    """

    occurrences = {}
    for char in text:
      if char in occurrences:
        occurrences[char] += 1
      else:
        occurrences[char] = 1

    return occurrences
    

  def huffman(self, occurences):

    """
    Zwraca korzeń drzewa Huffmana utworzonego na podstawie
    słownika wystąpień znaków w tekście.
    """

    n = len(occurences)

    for c in occurences.keys():
      node = Node(c, occurences[c])
      self.q.insert(node)

    for i in range(n-1):
      z = Node(None, 0)
      z.left = x = self.q.extract_min()
      z.right = y = self.q.extract_min()
      z.freq = x.freq + y.freq
      self.q.insert(z)

    return self.q.extract_min()

  def generate_huffman_codes(self, root, current_code="", codes=None):

    """
    Rekurencyjnie generuje kody Huffmana w drzewie, zaczynając od korzenia.
    """

    if codes is None:
      codes = {}

    if root.label is not None:
      codes[root.label] = current_code
      return codes

    if root.left:
      self.generate_huffman_codes(root.left, current_code + "0", codes)

    if root.right:
      self.generate_huffman_codes(root.right, current_code + "1", codes)

    return codes
  
  def encode(self, text, codes):

    """
    Koduje tekst za pomocą kodów Huffmana.
    """

    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text

  def pad_encooded_text(self, encoded_text):

    """
    Dodaje padding do zakodowanego tekstu, tak aby jego długość była
    wielokrotnonością 8. Do tekstu dodawany jest prefiks - 8-bitową 
    reprezentację wartości extra padding, którą dekoder musi usunąć przy dekodowaniu.
    """

    extra_padding = 8 - (len(encoded_text) % 8)
    for i in range(extra_padding):
      encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text
  
  def get_byte_array(self, padded_encoded_text):

    """
    Konwertuje zakodowany i skonwertowany tekst na listę bajtów.
    """

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
      byte = padded_encoded_text[i:i+8]
      b.append(int(byte, 2))
    return b
  
  def compress(self, filename, output_filename):

    """
    Kompresuje plik o podanej nazwie i zapisuje do pliku o podanej nazwie.
    W pliku wyjściowym zapisywany jest słownik kodów Huffmana w czytelnym formacie, a następnie
    zakodowany tekst binarnie.
    """
    
    text = self.get_text(filename)
    occurences = self.count_occurrences(text)
    root = self.huffman(occurences)
    codes = self.generate_huffman_codes(root)
    encoded_text = self.encode(text, codes)
    padded_encoded_text = self.pad_encooded_text(encoded_text)
    byte_array = self.get_byte_array(padded_encoded_text)

    with open(output_filename, "w") as file:
      file.write(str(codes) + '\n')
    with open(output_filename, "ab") as file:
      file.write(bytes(byte_array))
  
  def remove_padding(self, padded_encoded_text):

    """
    Usuwa padding z zakodowanego tekstu.
    """
    
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text
  
  def decode_text(self, encoded_text, codes):

    """
    Dekoduje zakodowany tekst przy pomocy słownika kodów Huffmana.
    """

    current_code = ""
    decoded_text = ""
    reversed_codes = {v: k for k, v in codes.items()}
    for bit in encoded_text:
      current_code += bit
      if current_code in reversed_codes:
        character = reversed_codes[current_code]
        decoded_text += character
        current_code = ""

    return decoded_text
  
  def decompress(self, filename, output_filename):
    
    """
    Dekompresuje plik o podanej nazwie i zapisuje odkompresowany tekst
    do pliku o podanej nazwie.
    """

    with open(filename, "rb") as file:
      codes = eval(file.readline())
      byte_array = bytearray(file.read())

    padded_encoded_text = "".join([format(byte, "08b") for byte in byte_array])
    encoded_text = self.remove_padding(padded_encoded_text)
    decoded_text = self.decode_text(encoded_text, codes)

    with open(output_filename, "w") as file:
      file.write(decoded_text)
     

def main():

  """
  Główna funkcja programu. Przyjmuje 3 argumenty z linii komend:
  - 'c' lub 'd' - c dla kompresji, d dla dekomresji
  - nazwa pliku wejściowego
  - nazwa pliku wyjściowego
  """

  if sys.argv[1] == 'c':
    c = Compression()
    c.compress(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'd':
    c = Compression()
    c.decompress(sys.argv[2], sys.argv[3])
  

main()