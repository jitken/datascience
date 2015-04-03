import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):

    matrix = record[0]
    row_idx = record[1]
    col_idx = record[2]
    value = record[3]

    # Need to be known a-priori
    a_numrows = 5
    b_numcols = 5

    # Compute AxB, key = (row_idx, col_idx) of AxB
    if matrix == 'a':
      for idx in range(b_numcols):
        mr.emit_intermediate((row_idx,idx),(col_idx, value))
    else:
      # it is matrix b
      for idx in range(a_numrows):
        mr.emit_intermediate((idx,col_idx),(row_idx, value))

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    my_dict = {}

    # Finding value of AxB at (i,j)
    total = 0
    for v in list_of_values:
      idx = v[0]
      val = v[1]
      if idx in my_dict:
        total += my_dict[idx] * val
      else:
        my_dict[idx] = val

    row_idx = key[0]
    col_idx = key[1]
    if total > 0:
      mr.emit((row_idx, col_idx, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
