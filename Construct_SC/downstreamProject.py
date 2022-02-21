import sys
import gzip

package_file = sys.argv[1]
output_file = sys.argv[2]
package_list = []
with open(package_file) as f:
    for line in f:
        package_list.append(line.strip('\n').split(';')[0])
# print(package_list)
with open(output_file, 'w', encoding='utf-8') as of:
    for i in range(32):
        print("Reading gz file number " + str(i))
        file = gzip.open("/fast/DL_Supply_Chain/technical_dependency/c2bPtaPkgQPY." + str(i) + ".gz")
        for line in file.readlines():
            line = line.decode('utf-8', 'ignore')
            entry = line.strip('\n').split(';')
            repo = entry[1]
            modules = entry[5:]
            for m in modules:
                m = m.split('.')[0]
                if m in package_list:
                    of.write(m + ';' + line)
        '''
        file = gzip.open("/fast/DL_Supply_Chain/technical_dependency/c2bPtaPkgQipy." + str(i) + ".gz")
        for line in file.readlines():
            line = line.decode('utf-8', 'ignore')
            entry = line.strip('\n').split(';')
            repo = entry[1]
            modules = entry[5:]
            for m in modules:
                m = m.split('.')[0]
                if m in package_list:
                    of.write(m + ';' + line)
        '''
