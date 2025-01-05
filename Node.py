class Node:
  
  """
  Klasa reprezentująca węzeł drzewa
  """
  
  label = ""
  left = None
  right = None
  freq = 0

  def __init__(self, label, freq):
    self.label = label
    self.freq = freq

  def __lt__(self, other):
      # Porównanie najpierw po częstotliwości
      
          # Jeśli częstotliwości są równe, porównaj etykiety
    if self.label is None:
      return False  # Węzły wewnętrzne powinny być traktowane jako "większe"
    if other.label is None:
      return True   # Węzły wewnętrzne traktowane jako "większe"
    if self.freq == other.freq: 
      return self.label < other.label
    return self.freq < other.freq
    

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
      if self.is_empty():
          raise IndexError("peek() called on empty heap")
      return self.heap[0]

  def is_empty(self):
      return len(self.heap) == 0

  def size(self):
      return len(self.heap)

class Compression:
  def __init__(self):
      self.q = PriorityQueue()

  def get_text(self, filename):
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
    

  def Huffman(self, occurences):
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
    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text

  def write_to_file(self, codes, encoded_text, filename):
      # Dodaj znak końca pliku do zakodowanego tekstu # gdzie 'EOF' to symbol oznaczający koniec

      with open(filename, 'wb') as file:
          byte_array = bytearray()
          
          for i in range(0, len(encoded_text), 8):
              byte = encoded_text[i:i+8]
              if len(byte) < 8:
                  byte = byte.ljust(8, '0')
              byte_array.append(int(byte, 2))
          
          file.write(byte_array)

      

  def compress(self, input_filename,output_filename):
    text = self.get_text(input_filename)
    occurrences = self.count_occurrences(text)
    root = self.Huffman(occurrences)
    codes = self.generate_huffman_codes(root)
    encoded_text = self.encode(text, codes)
    self.write_to_file(codes, encoded_text, output_filename)

    return codes

  def decompress(self, input_filename, output_filename, codes):
      with open(input_filename, "rb") as f:
          byte_data = f.read()
          binary_string = ''.join(format(byte, '08b') for byte in byte_data)

          reversed_codes = {v: k for k, v in codes.items()}

          current_code = ""
          decoded_text = ""
          
          for bit in binary_string:
              current_code += bit
              if current_code in reversed_codes:
                  character = reversed_codes[current_code]
                  decoded_text += character
                  current_code = ""

      with open(output_filename, "w") as f:
          f.write(decoded_text)
  
  


def main():
    
  c = Compression()
  codes = c.compress("test.txt", "compressed.txt")
  c.decompress("compressed.txt", "decompressed.txt", codes)

main()