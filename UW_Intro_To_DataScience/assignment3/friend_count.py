import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
 
    # person name
    name = record[0]
    mr.emit_intermediate(name, 1)

def reducer(key, list_of_values):
    # key: name
    # list_of_values: its length indicate # of friends
    mr.emit((key, len(list_of_values)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
