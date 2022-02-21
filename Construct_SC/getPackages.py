import csv
import sys
import mysql.connector
from tqdm import tqdm

in_path = sys.argv[1]
out_path = sys.argv[2]
pypi_packages = int(sys.argv[3])


def get_pypi_pakcages():
    with open('python_packages', 'w') as f:
        cnx = mysql.connector.connect(user='root', password='OSSLab@123', database='libraries')
        query = ("SELECT id, name, repository_url, repository_id  FROM projects WHERE platform = 'Pypi' and repository_url LIKE 'https://%'")
        curA = cnx.cursor(buffered=True)
        curA.execute(query)
        for id, name, repository_url, repository_id in curA:
            if id and name and repository_url and repository_id:
                f.write(str(id) + ';' + name + ';' + repository_url + ';' + str(repository_id) + '\n')

if pypi_packages == 1:
    get_pypi_pakcages()
package_name = {}
with open('python_packages') as f:
    for line in f:
        items = line.strip('\n').split(';')
        name, url = items[1], items[2]
        try:
            chunks = url.split('//')[1].split('/')
            if len(chunks) == 3:
                if chunks[0] == 'github.com':
                    package_name[chunks[1] + '_' + chunks[2]] = name
                else:
                    package_name[chunks[0] + '_' + chunks[1] + '_' + chunks[2]] = name
        except:
            print(url)

project_list = []
with open(in_path) as inf:
    for line in tqdm(inf):
        project_list.append(line.split(';')[0])
project_list = list(set(project_list))

with open(out_path, 'w') as outf:
    for p in tqdm(project_list):
        if p in package_name.keys():
            outf.write(package_name[p] + ';' + p + '\n')
