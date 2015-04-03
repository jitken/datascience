import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents

    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts

    order = None

    # Find Order
    for value in list_of_values:
      if value[0] == 'order':
        order = value
        break

    for value in list_of_values:
      if value[0] == 'line_item':
        mr.emit(order + value)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
