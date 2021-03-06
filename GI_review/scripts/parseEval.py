#!/usr/bin/python

from os import listdir
from os.path import isfile, join
from optparse import OptionParser



'''
Parse eval_std_ to get metrics
Only read the last line --> change to any line specified by linenum.
'''  
def getMetricsFromEvalFile(folder, linenum, tag='eval_std_'):
    # find all files with name as eval_std_*    
    file_list = [ join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and f.startswith(tag) ]
    base_metric_list = []
    for file in file_list:
        # get the suffix of file name
        start = file.index('d_') + 2
        suffix = file[start:]
        base_res = getMetrics(file, linenum)
        # some file may return no results due to interrupted run
        if base_res:
            base_metric_list.append((suffix, base_res))          
            
    final_metric = join(folder, 'metric_list')
    writeListOfTupleToFile(final_metric, base_metric_list)
    


def getMetrics(infile, linenum):
    last = ''
    with open(infile, 'r') as fh:
        lines = fh.readlines()
        # in case some output files are not complete
        if len(lines) > 0:
            last = lines[linenum]   
    if last is not '':
        metric = []
        fields = last.strip().split('\t')
        for f in fields: 
            value = f.split(':')[-1].strip()       
            metric.append(value)

        return tuple(metric)

    
# tuple format: (v, (v,v,...))
def writeListOfTupleToFile(filename, list):     
    outfile = open(filename, 'w')

    for key, values in list:
        suffix_str = '\t%s'             
        line = [key]
        line_str = '%s' 
        for value in values:
            line.append(value)
            line_str += suffix_str
        line_str += '\n'          
        outfile.write(line_str % tuple(line))

    outfile.close()
                  
                
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "", dest="directory", help="home directory")
    parser.add_option("-t", "--tag", dest="tag", help="tag in the name output file. Default: 'eval_std_'")
    parser.add_option("-l", "--linenum", dest="linenum", type='int', default='-1', help="line number of the output to extract")
    (options, args) = parser.parse_args()
       
    if options.tag:
        getMetricsFromEvalFile(options.directory, options.linenum, tag=options.tag)
    else:
        getMetricsFromEvalFile(options.directory, options.linenum)
