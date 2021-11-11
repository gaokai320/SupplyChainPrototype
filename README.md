# Supply Chain Prototype
An IT prototype for constructing software supply chain

## How to Run
### World of Code (WoC)
World of Code (WoC) collects Git objects of open source repositories across code hosting platforms (such as GitHub, Bitbucket, GitLab, and SourceForge), curates the collected data by, for example, deforking repositories and parsing dependencies from each version of source code file (technical dependencies), and provides a variety of ways to query the data. 
The technical dependencies are stored by line where the format of each line is as the following:
```
commit;deforked repo;timestamp;author;blob;module1;module2;...` 
```
For example:
```
0a000387557ecfb8454af75012dc5c9f95b9b582;theTB_visualKBQA;1482365755;Huaizu Jiang <hzjiang@vonmises.cs.umass.edu>;157038d94eff0e2b0b267ada17c59268e352a173;read_data;itertools.izip;__future__.absolute_import;os;tensorflow;cPickle;__future__.print_function;numpy;time;image_networks;argparse;__future__.division;probability_networks;question_networks;sys
```
### Construct Supply Chain
Needed code files: `downstreamProject.py`, `projectImportTime.py`, `filter.py`, `getPackages.py`, all in `./src/Construct SC` folder.
- `downstreamProject.py`: query the technical dependencies provided by WoC to retrieve all records that contain given modules. It needs two command line parameters: 
    > the first parameter: path to the file containing given upstream package informations. Each line of the file should follow the format: package import name;packge name in [Libraries.io](https://libraries.io/);package name in WoC. For example, 'torch,pytorch,pytorch_pytorch'
    > the second parameter: path to the file storing retrieved records. Each line of the file follows the format: upstream package import name;commit;deforked repo;timestamp;author;blob;module1;module2;...

- `projectImportTime.py`: preprocess the WoC records retrieved by `downstreamProject.py` to get the first import time of a project importing an upstream package. It needs two command line parameters:
    > the first parameter: path to the file storing retrieved output from WoC, each line of the file is: upstream package import name;commit;deforked repo;timestamp;author;blob;module1;module2;...
    > the second parameter: path to the file storing projects' first import time, each line of the file follows the format: project;imported_pakcage;first import time

- `filter.py`: filter projects whose first import time of an upstream package is earlier than the first import time of the upstream package importing its upstream packages in the supply chain. For example, if an upstream package *U* first imported another package in the supply chain *UU* at time *T1*, and a project *P* first imported *U* at time *T2*, if *T2* < *T1*, we filter out *P*. It needs three parameters:
    > the first parameter: path to the file storing last layer project's first import name, each line of the file is: project;imported_pakcage;first import time
    > the second parameter: path to the file storing last layer package's information, each line of the file is: package import name;packge name in [Libraries.io](https://libraries.io/);package name in WoC
    > the third parameter: path the the file storing current layer project's first import name, each line of the file is: project;imported_pakcage;first import time
    

- `getPackages.py`: match retrieved downstream projects with Libraries.io data to find downstream packages. It needs three command line parameters:
    > the first parameter: path to the file storing the filtered downstream projects. each line of the file is: project;imported_pakcage;first import time
    > the second parameter: path to the file storing the matched downstream packages, each line of the file is: packge name in Libraries.io,package name in WoC
    > the third parameter: whether to retrieve Python packages from Libraries.io. When first run `filter.py`, set to 1, otherwise, set to 0.

- **Caution:** after running `getPackages.py`, you need to manually label the import name of each package, as some packages' import name is different from their package name, for instance, Pytorch's import name is torch. Each line of the labelled file should follow the format: `package import name;packge name in [Libraries.io](https://libraries.io/);package name in WoC`

#### Construct TensorFlow supply chain
```shell


## populate information to TensorFlow first layer
echo "tensorflow;tensorflow;tensorflow_tensorflow" > tensorflow_layer1_package_name

## find all second layer's projects and packages
python downstreamProject.py tensorflow_layer1_package_name tensorflow_layer2_info
python projectImportTime.py tensorflow_layer2_info tensorflow_layer2_project
python getPackages.py tensorflow_layer2_project tensorflow_layer2_package 1
### manually label packages in tensorflow_layer2_package, and store the results in tensorflow_layer2_package_name

## find all third layer's projects and packages
python downstreamProject.py tensorflow_layer2_package_name tensorflow_layer3_info
python projectImportTime.py tensorflow_layer3_info tensorflow_layer3_project
python filter.py tensorflow_layer2_project tensorflow_layer2_package_name tensorflow_layer3_project > tensorflow_layer3_project_filtered
### remove second layer's packges
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer3_project_filtered > tensorflow_layer3_project_filtered2
mv tensorflow_layer3_project_filtered2 tensorflow_layer3_project_filtered
python getPackages.py tensorflow_layer3_project_filtered tensorflow_layer3_package 0
### manually label packages in tensorflow_layer3_package, and store the results in tensorflow_layer3_package_name

## find all fourth layer's projects and packages
python downstreamProject.py tensorflow_layer3_package_name tensorflow_layer4_info
python projectImportTime.py tensorflow_layer4_info tensorflow_layer4_project
python filter.py tensorflow_layer3_project tensorflow_layer3_package_name tensorflow_layer4_project > tensorflow_layer4_project_filtered
### remove second and third layer's packges
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer4_project_filtered > tensorflow_layer4_project_filtered2
mv tensorflow_layer4_project_filtered2 tensorflow_layer4_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer4_project_filtered > tensorflow_layer4_project_filtered2
mv tensorflow_layer4_project_filtered2 tensorflow_layer4_project_filtered
python getPackages.py tensorflow_layer4_project_filtered tensorflow_layer4_package 0
### manually label packages in tensorflow_layer4_package, and store the results in tensorflow_layer4_package_name

## find all fifth layer's projects and packages
python downstreamProject.py tensorflow_layer4_package_name tensorflow_layer5_info
python projectImportTime.py tensorflow_layer5_info tensorflow_layer5_project
python filter.py tensorflow_layer4_project tensorflow_layer4_package_name tensorflow_layer5_project > tensorflow_layer5_project_filtered
### remove second and third and fourth layer's packges
cut -d\; -f2 tensorflow_layer4_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer5_project_filtered > tensorflow_layer5_project_filtered2
mv tensorflow_layer5_project_filtered2 tensorflow_layer5_project_filtered
python getPackages.py tensorflow_layer5_project_filtered tensorflow_layer5_package 0
### manually label packages in tensorflow_layer5_package, and store the results in tensorflow_layer5_package_name

## find all sixth layer's project
python downstreamProject.py tensorflow_layer5_package_name tensorflow_layer6_info
python projectImportTime.py tensorflow_layer6_info tensorflow_layer6_project
python filter.py tensorflow_layer5_project tensorflow_layer5_package_name tensorflow_layer6_project > tensorflow_layer6_project_filtered
### remove second and third and fourth and fifth layer's packges
cut -d\; -f2 tensorflow_layer5_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer4_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer3_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
cut -d\; -f2 tensorflow_layer2_package | grep -v -f - tensorflow_layer6_project_filtered > tensorflow_layer6_project_filtered2
mv tensorflow_layer6_project_filtered2 tensorflow_layer6_project_filtered
python getPackages.py tensorflow_layer6_project_filtered tensorflow_layer6_package 0
### tensorflow_layer6_package is null, terminate
```

#### Construct PyTorch supply chain
```shell


## populate information to torch first layer
echo "torch;pytorch;pytorch_pytorch" > torch_layer1_package_name

## find all second layer's projects and packages
python downstreamProject.py torch_layer1_package_name torch_layer2_info
python projectImportTime.py torch_layer2_info torch_layer2_project
python getPackages.py torch_layer2_project torch_layer2_package 1
### manually label packages in torch_layer2_package, and store the results in torch_layer2_package_name

## find all third layer's projects and packages
python downstreamProject.py torch_layer2_package_name torch_layer3_info
python projectImportTime.py torch_layer3_info torch_layer3_project
python filter.py torch_layer2_project torch_layer2_package_name torch_layer3_project > torch_layer3_project_filtered
### remove second layer's packges
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer3_project_filtered > torch_layer3_project_filtered2
mv torch_layer3_project_filtered2 torch_layer3_project_filtered
python getPackages.py torch_layer3_project_filtered torch_layer3_package 0
### manually label packages in torch_layer3_package, and store the results in torch_layer3_package_name

## find all fourth layer's projects and packages
python downstreamProject.py torch_layer3_package_name torch_layer4_info
python projectImportTime.py torch_layer4_info torch_layer4_project
python filter.py torch_layer3_project torch_layer3_package_name torch_layer4_project > torch_layer4_project_filtered
### remove second and third layer's packges
cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer4_project_filtered > torch_layer4_project_filtered2
mv torch_layer4_project_filtered2 torch_layer4_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer4_project_filtered > torch_layer4_project_filtered2
mv torch_layer4_project_filtered2 torch_layer4_project_filtered
python getPackages.py torch_layer4_project_filtered torch_layer4_package 0
### manually label packages in torch_layer4_package, and store the results in torch_layer4_package_name

## find all fifth layer's projects and packages
python downstreamProject.py torch_layer4_package_name torch_layer5_info
python projectImportTime.py torch_layer5_info torch_layer5_project
python filter.py torch_layer4_project torch_layer4_package_name torch_layer5_project > torch_layer5_project_filtered
### remove second and third and fourth layer's packges
cut -d\; -f2 torch_layer4_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer5_project_filtered > torch_layer5_project_filtered2
mv torch_layer5_project_filtered2 torch_layer5_project_filtered
python getPackages.py torch_layer5_project_filtered torch_layer5_package 0
### manually label packages in torch_layer5_package, and store the results in torch_layer5_package_name

## find all sixth layer's project
python downstreamProject.py torch_layer5_package_name torch_layer6_info
python projectImportTime.py torch_layer6_info torch_layer6_project
python filter.py torch_layer5_project torch_layer5_package_name torch_layer6_project > torch_layer6_project_filtered
### remove second and third and fourth and fifth layer's packges
cut -d\; -f2 torch_layer5_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer4_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer3_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
cut -d\; -f2 torch_layer2_package | grep -v -f - torch_layer6_project_filtered > torch_layer6_project_filtered2
mv torch_layer6_project_filtered2 torch_layer6_project_filtered
### torch_layer6_project_filtered is null, terminate
```

#### Put all layer's project (\*project_filtered files) and packages (\*package_name files) together and get layer
- `new_sc.py`: Put all layer's project (\*project_filtered files) and packages (\*package_name files) together, output is tensorflow_new_sc, torch_new_sc
- `get_layers.py`: Add layer information to tensorflow_new_sc and torch_new_sc,
```shell
python new_sc.py
python get_layers.py tensorflow_new_sc tensorflow_tensorflow
python get_layers.py torch_new_sc pytorch_pytorch
```

### Supply Chain Structure
#### Structure: structure
Data are in `./src/RQ1_structure/structure` folder
```shell
awk -F ':' '{print $NF}' tensorflow_tensorflow.layer | sort | uniq -c
awk -F ':' '{print $NF}' pytorch_pytorch.layer | sort | uniq -c
```
#### Structure: evolution
Data and scripts are in `./src/RQ1_structure/evolution` folder
##### Growth trend
Data and scripts in `all_repos` folder.
```shell
python draw_growth_trend.py
```
##### cumulative distribution
Data and scripts in `cumulative_distribution_downstream_projects` folder.
```shell
## get the cumulative distributions of the fraction of life cyle that a project in a SC takes to obtain at least 10%, at least 50%, and at least 90% of its downstream projects
python cumulative.py
## get the distribution of the fraction of downstream projects obtained in the first and last month of the packages in the two SCs 
python first_last_month.py
```
#### Structure: vulnerability
Data are in `./src/RQ1_structure/structure` folder.
```shell
## construct edges
python process_data.py

## calculate and draw indegree
python calculate_in_degree.py
python draw_indegree_plot.py

## calculate and draw outdegree
python calculate_out_degree.py
python draw_outdegree_plot.py

## calculate and draw betweeness
python calculate_betweeness.py
```

### Supply Chain Domain Distribution
#### Package Domain Distribution
Data in `./src/RQ2_domain_distribution/packages` folder.
#### Project Domain Distribution
Data in `./src/RQ2_domain_distribution/projects` folder.
- `ga_lda.py`: run LDA on README corpus. Each project's README.md file should stored in separate files and named with the project's name under the same folder. It needs two parameters: the first specify the folder path storing README, the second specify the folder path storing LDA model.

### Supply Chain Evolutionary Factors
Data and scripts in `./src/RQ3_Evolutionary_Factors` folder.
- `analysis.R`: perform gam fitting.

## Report
The final report please refer to `./prototype.html`.