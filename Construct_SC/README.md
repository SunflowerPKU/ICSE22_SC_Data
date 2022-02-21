## Characterizing Deep Learning Supply Chain

### Get all projects in the supply chain.

1. First layer only contains Tensorflow and PyTorch, then get all downstream projects using them:

```shell
# layer2_info contains just relevant lines from c2bPtaPkgQ*.gz
python downstreamProject.py layer1_project layer2_info
# layer2_project format: project;imported_pakcage;first_import_time
python projectImportTime.py layer2_info layer2_project
```

2. Get released packages of second layer projects from Libraries.io

```shell
# layer2_package format: libraries.io_name;repo_name
# the last argument is 1 only when you first run getPackages.py
grep ";tensorflow;" layer2_project > tensorflow_layer2
grep ";torch;" layer2_project > torch_layer2
# if have python_packages, use parameter 0, else use parameter 1
python getPackages.py tensorflow_layer2 tensorflow_layer2_package 0
python getPackages.py torch_layer2 torch_layer2_package 0
python getPackages.py layer2_project layer2_package 1
# after manually labelled, layer2_package format: import_name;libraries.io_name;repo_name
grep -f tensorflow_layer2_package layer2_package > tensorflow_layer2_package_name
grep -f torch_layer2_package layer2_package > torch_layer2_package_name
```

3. Get third layer projects based on second layer's packages

```shell

python downstreamProject.py tensorflow_layer2_package_name tensorflow_layer3_info
python downstreamProject.py torch_layer2_package_name torch_layer3_info
python projectImportTime.py tensorflow_layer3_info tensorflow_layer3_project
python projectImportTime.py torch_layer3_info torch_layer3_project
```

After exploration, we find some unusal cases:

```shell
cut -d\; -f2 layer3_project | sort | uniq -c | sort -t " "
...
 115800 app
 134150 to
```

`app` and `to` are general terms, and will introduce many false positives. So, we need to filter out those unusal cases, so as to `mxnet`, `paddle`, and `all`;
we also need to filter projects that import time is earlier than it dependency time.

```shell
python filter.py tensorflow_layer2 tensorflow_layer2_package_name tensorflow_layer3_project > tensorflow_layer3_project_filtered
python filter.py torch_layer2 torch_layer2_package_name torch_layer3_project > torch_layer3_project_filtered
# rm layer2 package
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer3_project_filtered > tensorflow_layer3_project_filtered2
mv tensorflow_layer3_project_filtered2 tensorflow_layer3_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer3_project_filtered > torch_layer3_project_filtered2
mv torch_layer3_project_filtered2 torch_layer3_project_filtered

```

4. Get released packages of thrid layer projects from Libraries.io

```shell
python getPackages.py tensorflow_layer3_project_filtered tensorflow_layer3_package 0
python getPackages.py torch_layer3_project_filtered torch_layer3_package 0
```

5. Get fourth layer projects based on third layer's packages

```shell
python downstreamProject.py tensorflow_layer3_package_name tensorflow_layer4_info
python downstreamProject.py torch_layer3_package_name torch_layer4_info
python projectImportTime.py tensorflow_layer4_info tensorflow_layer4_project
python projectImportTime.py torch_layer4_info torch_layer4_project
python filter.py tensorflow_layer3_project tensorflow_layer3_package_name tensorflow_layer4_project > tensorflow_layer4_project_filtered
python filter.py torch_layer3_project torch_layer3_package_name torch_layer4_project > torch_layer4_project_filtered
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer4_project_filtered > tensorflow_layer4_project_filtered2
mv tensorflow_layer4_project_filtered2 tensorflow_layer4_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer4_project_filtered > tensorflow_layer4_project_filtered2
mv tensorflow_layer4_project_filtered2 tensorflow_layer4_project_filtered

cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer4_project_filtered > torch_layer4_project_filtered2
mv torch_layer4_project_filtered2 torch_layer4_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer4_project_filtered > torch_layer4_project_filtered2
mv torch_layer4_project_filtered2 torch_layer4_project_filtered
python getPackages.py tensorflow_layer4_project_filtered tensorflow_layer4_package 0
python getPackages.py torch_layer4_project_filtered torch_layer4_package 0
```

5. Get fifth layer projects based on forth layer's packages

```shell
python downstreamProject.py tensorflow_layer4_package_name tensorflow_layer5_info
python downstreamProject.py torch_layer4_package_name torch_layer5_info
python projectImportTime.py tensorflow_layer5_info tensorflow_layer5_project
python projectImportTime.py torch_layer5_info torch_layer5_project

python filter.py tensorflow_layer4_project tensorflow_layer4_package_name tensorflow_layer5_project > tensorflow_layer5_project_filtered
python filter.py torch_layer4_project torch_layer4_package_name torch_layer5_project > torch_layer5_project_filtered

cut -d\; -f2 tensorflow_layer4_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered

cut -d\; -f2 torch_layer4_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
python getPackages.py tensorflow_layer5_project_filtered tensorflow_layer5_package 0
python getPackages.py torch_layer5_project_filtered torch_layer5_package 0
```

5. Get sixth layer projects based on fifth layer's packages

```shell
python downstreamProject.py tensorflow_layer5_package_name tensorflow_layer6_info
python downstreamProject.py torch_layer5_package_name torch_layer6_info

python projectImportTime.py tensorflow_layer6_info tensorflow_layer6_project
python projectImportTime.py torch_layer6_info torch_layer6_project

python filter.py tensorflow_layer5_project tensorflow_layer5_package_name tensorflow_layer6_project > tensorflow_layer6_project_filtered
python filter.py torch_layer5_project torch_layer5_package_name torch_layer6_project > torch_layer6_project_filtered

cut -d\; -f2 tensorflow_layer5_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer4_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered

cut -d\; -f2 torch_layer5_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer4_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered

python getPackages.py tensorflow_layer6_project_filtered tensorflow_layer6_package 0
python getPackages.py torch_layer6_project_filtered torch_layer6_package 0
```