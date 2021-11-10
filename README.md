# Supply Chain Prototype
An IT prototype for constructing software supply chain

## World of Code (WoC)
World of Code (WoC) collects Git objects of open source repositories across code hosting platforms (such as GitHub, Bitbucket, GitLab, and SourceForge), curates the collected data by, for example, deforking repositories and parsing dependencies from each version of source code file (technical dependencies), and provides a variety of ways to query the data. 
The technical dependencies are stored by line where the format of each line is as the following:
```
commit;deforked repo;timestamp;author;blob;module1;module2;...` 
```
For example:
```
0a000387557ecfb8454af75012dc5c9f95b9b582;theTB_visualKBQA;1482365755;Huaizu Jiang <hzjiang@vonmises.cs.umass.edu>;157038d94eff0e2b0b267ada17c59268e352a173;read_data;itertools.izip;__future__.absolute_import;os;tensorflow;cPickle;__future__.print_function;numpy;time;image_networks;argparse;__future__.division;probability_networks;question_networks;sys
```
## Construct Supply Chain
### 