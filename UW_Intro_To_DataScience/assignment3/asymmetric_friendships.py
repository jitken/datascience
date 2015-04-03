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
    nameA = record[0]
    nameB = record[1]
    mr.emit_intermediate((nameA, nameB), 1)
    mr.emit_intermediate((nameB, nameA), 1)

def reducer(key, list_of_values):
    # key: person name
    # list_of_values: if len(self) = 1, it's asymmetric calculation

    if len(list_of_values) == 1:
      mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
