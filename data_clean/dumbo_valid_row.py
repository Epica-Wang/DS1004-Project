from pyspark import SparkContext
from csv import reader
from csv import writer


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def is_valid(row):
    
    return True


def write_csv(x):
    output = StringIO("")
    writer(output).writerow(x)
    return output.getvalue().strip()


if __name__ == "__main__":
    file_name = "ten_lines_data.csv"
    # file_name = "ten_thousand_lines_data.csv"
    result_file = "clean.csv"
    sc = SparkContext()
    lines = sc.textFile(file_name, 1)
    cells = lines.mapPartitions(lambda x: reader(x)). \
        filter(lambda x: is_valid(x) is True).\
        map(lambda x: write_csv(x)).saveAsTextFile(result_file)
    sc.stop()



# hfs -rm -r result.csv
# hfs -getmerge result.csv > result.csv