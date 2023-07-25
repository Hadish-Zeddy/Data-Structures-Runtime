from isa import ISA
from memory import Memory, MainMemory
from random import randint

class Cache(Memory):
  def __init__(self):
    super().__init__(name="Cache", access_time=0.5)
    self.main_memory = MainMemory()
    self.fifo_index = 0

    self.data = [
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
      {"tag": None, "data": ""},
    ]

  def read(self, address):
    super().read()
    data = None
    entry = self.get_entry(address)
    if entry is not None:
      data = entry["data"]
    else:
      data = self.main_memory.read(address)
      # Change the code below
      self.add_entry(address, data)

    return data

  def replace_entry(self, address, data):
    # Change the code below
    index = self.random_policy()
    self.data[index] = {"tag": address, "data": data}

  def random_policy(self):
    return randint(0, len(self.data)-1)

  def fifo_policy(self):
    index = self.fifo_index
    self.fifo_index += 1
    if self.fifo_index == len(self.data):
      self.fifo_index = 0

    return index

  # Adds data in an empty entry
  def add_entry(self, address, data):
    for entry in self.data:
      if entry["tag"] == None:
        entry["tag"] = address
        entry["data"] = data
        return

  # Returns entry on cache hit
  # Returns None on cache miss
  def get_entry(self, address):
    for entry in self.data:
      if entry["tag"] == address:
          print(f"HIT: ", end="")
          return entry

    print(f"MISS", end="")
    return None

  def get_exec_time(self):
    exec_time = self.exec_time + self.main_memory.get_exec_time()
    return exec_time

if __name__ == "__main__":
  cache_arch = ISA()
  cache_arch.set_memory(Cache())

  # Architecture runs the instructions
  cache_arch.read_instructions("ex6_instructions")

  # This outputs the memory data and code execution time
  exec_time = cache_arch.get_exec_time()
  if exec_time > 0:
    print(f"OUTPUT STRING: {cache_arch.output}")
    print(f"EXECUTION TIME: {exec_time:.2f} nanoseconds")