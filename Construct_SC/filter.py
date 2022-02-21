import sys

# python filter.py tensorflow_layer2 tensorflow_layer2_package_name tensorflow_layer3_project
file_path1 = sys.argv[1] # *layer2_project_time
file_path2 = sys.argv[2] # layer2_package_name
file_path3 = sys.argv[3] #layer3_project

packages = {}
with open(file_path2) as f:
    for line in f:
        name, _, repo = line.strip('\n').split(';')
        packages[repo] = name

layer2_package_time = {}
with open(file_path1) as f:
    for line in f:
        repo, dep, time = line.strip('\n').split(';')
        if repo in packages.keys():
            layer2_package_time[packages[repo]] = time

filter_package_list = ['app', 'to', 'mxnet', 'paddle', 'all']
with open(file_path3) as f:
    for line in f:
        repo, dep, time = line.strip('\n').split(';')
        if dep not in filter_package_list and layer2_package_time[dep] <= time:
            print(line.strip('\n'))
                
