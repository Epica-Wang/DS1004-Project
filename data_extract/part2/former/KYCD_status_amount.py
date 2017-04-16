from __future__ import print_function

import sys
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
        sc = SparkContext()
        tuples = sc.textFile(sys.argv[1], 1).mapPartitions(lambda x: reader(x))
        tuples = tuples.filter(lambda x : len(x) > 10).filter(lambda x : x[10] != '' and x[6] != '')
        pairs = tuples.map(lambda x : ((x[6].strip(), x[10].strip()), 1))
        result = pairs.reduceByKey(lambda x, y : x + y).sortByKey()
        result = result.map(lambda x: '%s\t%s\t%s' % (x[0][0], x[0][1], x[1]))
        result.saveAsTextFile("KYCD_status_amount.out")
        sc.stop()

