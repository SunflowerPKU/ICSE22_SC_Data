import sys
from tqdm import tqdm
from collections import defaultdict

path = sys.argv[1]
output_file = sys.argv[2]

upstream_project_import_time = defaultdict(lambda : defaultdict(int))
with open(path) as f:
    for line in tqdm(f):
        items = line.strip('\n').split(';')
        upstream, project, timestamp = items[0], items[2], int(items[3])
        if upstream_project_import_time[upstream][project] == 0 or upstream_project_import_time[upstream][project] > timestamp:
            upstream_project_import_time[upstream][project] = timestamp

upstream_project_import_time = dict(upstream_project_import_time)
with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
    for upstream, projects in upstream_project_import_time.items():
        for p, t in tqdm(projects.items()):
            f.write(p + ';' + upstream + ';' + str(t) + '\n')