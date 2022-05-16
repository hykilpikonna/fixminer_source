# FixMiner ![Build Status](https://travis-ci.com/SerVal-DTF/fixminer_source.svg?branch=master)[![Coverage Status](https://coveralls.io/repos/github/SerVal-DTF/fixminer_source/badge.svg?branch=master)](https://coveralls.io/github/SerVal-DTF/fixminer_source?branch=master)

# Code of FixMiner

Reference: [FixMiner: Mining Relevant Fix Patterns for Automated Program Repair](http://arxiv.org/pdf/1810.01791) (Empirical Software Engineering, [doi:10.1007/s10664-019-09780-z](https://doi.org/10.1007/s10664-019-09780-z))
## Citing FixMiner

You can cite FixMiner using the following bibtex:

```
@article{koyuncu2020fixminer,
  title={Fixminer: Mining relevant fix patterns for automated program repair},
  author={Koyuncu, Anil and Liu, Kui and Bissyand{\'e}, Tegawend{\'e} F and Kim, Dongsun and Klein, Jacques and Monperrus, Martin and Le Traon, Yves},
  journal={Empirical Software Engineering},
  pages={1--45},
  year={2020},
  publisher={Springer}
}
  ```
# FixMiner

* [I. Introduction of FixMiner](#user-content-i-introduction)
* [II. Environment setup](#user-content-ii-environment)
* [III. Replication Data](#user-content-iii-data)
* [IV. Step-by-Step execution](#user-content-iv-how-to-run)
<!--
* [V. Evaluation Result](#user-content-v-evaluation-result)
* [VI. Generated Patches](#user-content-vi-generated-patches)
* [VII. Structure of the project](#user-content-vii-structure-of-the-project)
-->

## I. Introduction

Fixminer is a systematic and automated approach to mine relevant and actionable fix patterns for automated program repair.
![The workflow of this technique.\label{workflow}](worflow.png)

** This version of the Fixminer has some changes compared to the one published in the paper. 

    - The iteration that was computing the shapes separetely is removed. Now the operation of the shape trees are performed together with the action trees. As a result of this change no shape clusters are generated separately anymore. The initial output of the pattern mining iteration is action trees (a.k.a patterns ) 

## II. Environment setup

* OS: macOS Mojave (10.14.3)
* JDK8: (**important!**)
* To mine from c code, [srcml 1.0.0](https://www.srcml.org/#download)
* Download and configure Anaconda
* Create an python environment using the [environment file](environment.yml)
  ```powershell
  conda env create -f environment.yml
  ```
* After creating the environment, activate it. It is containing necessary dependencies for redis, and python.
  ```powershell
  source activate fixminerEnv
  ```

* Update the config.yml file with the corresponding paths in your computer. An example config.yml file could be found under
  ```powershell
  fixminer_source/src/main/resources/config.yml
  ```
<!---
[fixminer.sh](python/fixminer.sh)

Unzip it,to the datasetPath path indicated in app.properties.

    7z x allDataset.7z
    
In order to launch FixMiner, execute [fixminer.sh](python/fixminer.sh)

    bash fixminer.sh /Users/..../enhancedASTDiff/python/ stats
--->

## IV. Step-by-Step execution

#### Before running

* Update [config file](src/main/resources/config.yml) with corresponding user paths.

* Install the project with maven from root. (usage [pom.xml](pom.xml))
  ```powershell
  mvn clean package
  ```
* Active the conda environment from shell
  ```powershell
  source activate fixminerEnv
  ```

In order to launch FixMiner, execute [fixminer.sh](python/fixminer.sh)

    bash fixminer.sh [CONFIG_FILE] [JOB]
     e.g. bash fixminer.sh  /Users/projects/release/fixminer_source/src/main/resources/config.yml dataset4c
     
A log file (app.log) is created after every execution of the [fixminer.sh]((python/fixminer.sh)). Please check this log file in order to access more information. 
 

    
#### Job Types  

*FixMiner* needs to follow an execution, **in the order listed below** in order to create clusters of patches.

   1. __dataset4j__ / __dataset4c__: Create a java/c mining dataset from the projects listed in [subjects.csv](python/data/subjects.csv) or [datasets.csv](python/data/datasets.csv) for c
      
   2. __richedit__: Calls the jar file produced as the results as maven package to compute Rich edit scripts.
   This step can be invoke natively from java or using the [Launcher](src/main/java/edu/lu/uni/serval/richedit/Launcher.java) with appropriate arguments.

         ```powershell
         java -jar FixPatternMiner-1.0.0-jar-with-dependencies.jar  /Users/projects/release/fixminer_source/src/main/resources/config.yml RICHEDITSCRIPT
         ```   
   3. __actionSI__: Search index creation for actions. The output of this step is written to __pairs__ folder which will be generated under __datapath__ in [config file](src/main/resources/config.yml)
    
   4. __compare__ : Calls the jar file produced as the results as maven package to compare the trees.
                             This step can be invoke natively from java or using the [Launcher](src/main/java/edu/lu/uni/serval/richedit/Launcher.java) with appropriate arguments.
                             
        ```powershell
        java -jar FixPatternMiner-1.0.0-jar-with-dependencies.jar  /Users/projects/release/fixminer_source/src/main/resources/config.yml COMPARE
        ```       
   5. __cluster__ : Forms clusters of identical trees. The output of this step is written to __actions__ folder which will be generated under __datapath__ in [config file](src/main/resources/config.yml)
   
   6. __tokenSI__ : Search index creation for tokens. The output of this step is written to __pairsToken__ folder which will be generated under __datapath__ in [config file](src/main/resources/config.yml)
   
   7. __compare__ : Calls the jar file produced as the results as maven package to compare the trees.
                                   This step can be invoke natively from java or using the [Launcher](src/main/java/edu/lu/uni/serval/richedit/Launcher.java) with appropriate arguments.
                                   
        ```powershell
        java -jar FixPatternMiner-1.0.0-jar-with-dependencies.jar  /Users/projects/release/fixminer_source/src/main/resources/config.yml COMPARE
        ```     
   
   8. __stats__: Calculate frequency statistics of the patterns under statsactions.csv in datapath. The information is also written in app.log file.
   
   9. __patterns__ : Export FixPatterns of APR integration under patterns folder located in datapath/


##### Structure of the cluster folders
```powershell
  |--- actions                    : Action clusters
  |------ReturnStatement          : AST Node type
  |---------4                     : The size of the rich edit script
  |------------0                  : 0th Action cluster of ReturnStatement of rich edit size 4
  |--------------- filename       : 0th member of the cluster


  |--- tokens                     : Token clusters
  |------ReturnStatement          : AST Node type
  |---------4                     : The size of the rich edit script
  |------------0                  : 0th Action cluster of ReturnStatement of rich edit size 4
  |---------------0               : 0th Token cluster of ReturnStatement of rich edit size 4 of 0th action cluster
  |----------------- filename       : 0th member of the cluster


```
                                                                                                                   
   <!--
    
    6. 'actionSI': Search index creation for actions. The output of this step is written to [pairs](python/data/pairsAction)
    
    7. 'compareActions' : ActionTree comparison
    
    8. 'clusterActions': Forms clusters of identical ActionTree. The output of this step is written to [shapes](python/data/actions)
    
    9. 'tokenSI': Search index creation for shapes. The output of this step is written to [pairs](python/data/pairsToken)
    
    10. 'compareTokens' : TokenTree comparison
    
    11. 'clusterTokens': Forms clusters of identical TokenTree. The output of this step is written to [shapes](python/data/tokens)
    
    12. 'stats' : Calculate some statistics about patterns under python/data/statsactions.csv,statsshapes.csv,statstokens.csv, and export FixPatterns of APR integration [fixpatterns](actionPattern2verify.csv)
    
   -->

<!--
App.properties:


FixMiner consists of several jobs that needs to run in order to extract fix pattern from the dataset.
It is necessary to run the FixMiner, following the order.
  1.ENHANCED AST DIFF calcuation

    By setting the jobType = ENHANCEDASTDIFF. This will create the ENHANCEDASTDIFF for the dataset regardless of the actionType.

  2.CACHE the enhanced AST Diff into memory cache

    By setting the jobType = CACHE
    
  3.SI search index construction.
  
    By setting the jobType = SI
    
  4.SIMI in order to compare the similarity between the trees.
  
    By setting the jobType = SIMI

  5.LEVEL1 mining

    By setting the jobType = LEVEL1

  6.LEVEL2 mining

    By setting the jobType = LEVEL2

  7.LEVEL3 mining

    By setting the jobType = LEVEL3
    
    
 A mining is iteration is executed for the actionType. In order to execute for all the actionTypes, the iteration should be repeated from 2-7 by changing the actionType.
    
  There are some additional parameters in the app.config. 
  
  actionType
    
    The admitted values are UPD,INS,DEL,MOV,MIX, which represents the ENHANCEDASTDIFF actions.
    UPD/INS/DEL/MOV considers tree where a single action operation is done in the action set
    MIX considers any action.
  
  parallelism
    
    The engine to use for parallelism. It is either FORKJOIN or AKKA. 
    FORKJOIN is recommended is the FixMiner is running on a single machine. 
    AKKA is suggested for distributed machines.
    
  numOfWorkers
  
    The number of workers that will be generated when AKKA is selected as the parallelism engine.
    
  cursor
  
    The maximum number of pairs in during the search index SI creation.
    
   eDiffTimeout
   
    The timeout value in seconds for the Enhanced Diff computation (ENHANCEDASTDIFF). 
    In case ENHANCEDASTDIFF step logs timeouts, this value can be increase. 
    
    
   The following parameters should be used when dealing with extremely large dataset. Otherwise, default values are suggested.
    
   isBigPair
    
    This flag when set to true, splits the pairs that into chunks as ..0.txt,1.txt etc. 
    
   chunk
   
    The extension of the pairs files. When isBigPair is set to false(which is default), it needs to be set as .csv 
    When isBigPair mode is activated then the SIMI step executed for each chunk by stepping the chunk as 0.txt, 1,txt) 

    
## V. Evaluation Result
## VI. Generated Patches
## VII. Structure of the project
--> 
    
<!--
    
## III. Replication Data
Replication Data:
    
   [singleBR.pickle](python/data/singleBR.pickle)
    
    This pickle contains the list bug reports (i.e. bid) with the their corresponding fixes (i.e. commit) for each project in the dataset (i.e. project). 
    
   [bugReports.7z.00X](python/data/bugReports.7z.001)
   
    This is the dump of the bug reports archive extracted from each commit. These bug reports are not necessarily considered as BUG,CLOSED; this archive is the contins initial bug reports before identifying the fixes. 
    
   [gumInput.7z.001](python/data/gumInput.7z.001)
   
    This archive contains all the patches in our dataset, formatted in a way that can be processed by GumTree (i.e DiffEntries, prevFiles, revFiles)
    
   [ALLbugReportsComplete.pickle](python/data/ALLbugReportsComplete.pickle)
   
    The pickle object that represents the bug reports under the following columns 'bugReport', 'summary', 'description', 'created', 'updated', 'resolved', 'reporterDN', 'reporterEmail','hasAttachment', 'attachmentTime', 'hasPR', 'commentsCount'
-->

#### Data Viewer

The intermediate data provided computed during the steps are listed in directory datapath (see [config file](src/main/resources/config.yml))
                                                                                                  
The data is stored in different formats. (e.g. pickle, redis db, csv, etc..)

###### Redis Commands

Connect to redis instance

 ```powershell
     redis-cli -p 6399
  ```   

We use 3 databases inside the redis, 0,1,2,3.
DB 0 stores the richedit dumps, comparison indices
DB 1 stores the filenames and their indices (used in comparison and stored in DB2, DB3) 
DB 2 stores the output of comparison action trees.
DB 3 stores the output of comparison token trees.

In order to switch between these database use the following command

 ```powershell
     select 2
  ```   

In order to trace the status of the stored rich edit scripts, use the following command

 ```powershell
     hlen dump
  ```   

In order to access the rich edit of a single hunk, first locate the key from DB 0. This command returns the exact name of the keys

 ```powershell
keys *NAME_OF_THE_HUNK

keys *fuse_67b14b_04e5b1_fabric#fabric-client#src#main#java#org#fusesource#fabric#jolokia#facade#facades#ProfileFacade.java.txt_1

OUTPUT:
1) "MethodDeclaration/40/fuse_67b14b_04e5b1_fabric#fabric-client#src#main#java#org#fusesource#fabric#jolokia#facade#facades#ProfileFacade.java.txt_1"
  ```   

Then, use the exact key in order to access the rich edit:
 ```powershell
hget dump NAME_OF_THE_EXACT_KEY

hget dump MethodDeclaration/40/fuse_67b14b_04e5b1_fabric#fabric-client#src#main#java#org#fusesource#fabric#jolokia#facade#facades#ProfileFacade.java.txt_1

OUTPUT:
"INS MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @TO@ TypeDeclaration@@[public]ProfileFacade, [Profile, HasId] @AT@ 7279 @LENGTH@ 309\n---INS Modifier@@public @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7279 @LENGTH@ 6\n---INS PrimitiveType@@void @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7286 @LENGTH@ 4\n---INS SimpleName@@MethodName:setConfiguration @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7291 @LENGTH@ 16\n---INS SingleVariableDeclaration@@String pid @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7308 @LENGTH@ 10\n------INS SimpleType@@String @TO@ SingleVariableDeclaration@@String pid @AT@ 7308 @LENGTH@ 6\n------INS SimpleName@@pid @TO@ SingleVariableDeclaration@@String pid @AT@ 7315 @LENGTH@ 3\n---INS SingleVariableDeclaration@@Map<String,String> configuration @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7320 @LENGTH@ 33\n------INS ParameterizedType@@Map<String,String> @TO@ SingleVariableDeclaration@@Map<String,String> configuration @AT@ 7320 @LENGTH@ 19\n---------INS SimpleType@@Map @TO@ ParameterizedType@@Map<String,String> @AT@ 7320 @LENGTH@ 3\n---------INS SimpleType@@String @TO@ ParameterizedType@@Map<String,String> @AT@ 7324 @LENGTH@ 6\n---------INS SimpleType@@String @TO@ ParameterizedType@@Map<String,String> @AT@ 7332 @LENGTH@ 6\n------INS SimpleName@@configuration @TO@ SingleVariableDeclaration@@Map<String,String> configuration @AT@ 7340 @LENGTH@ 13\n---INS VariableDeclarationStatement@@Map<String,Map<String,String>> configurations=getConfigurations(); @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7365 @LENGTH@ 70\n------INS ParameterizedType@@Map<String,Map<String,String>> @TO@ VariableDeclarationStatement@@Map<String,Map<String,String>> configurations=getConfigurations(); @AT@ 7365 @LENGTH@ 32\n---------INS SimpleType@@Map @TO@ ParameterizedType@@Map<String,Map<String,String>> @AT@ 7365 @LENGTH@ 3\n---------INS SimpleType@@String @TO@ ParameterizedType@@Map<String,Map<String,String>> @AT@ 7369 @LENGTH@ 6\n---------INS ParameterizedType@@Map<String,String> @TO@ ParameterizedType@@Map<String,Map<String,String>> @AT@ 7377 @LENGTH@ 19\n------------INS SimpleType@@Map @TO@ ParameterizedType@@Map<String,String> @AT@ 7377 @LENGTH@ 3\n------------INS SimpleType@@String @TO@ ParameterizedType@@Map<String,String> @AT@ 7381 @LENGTH@ 6\n------------INS SimpleType@@String @TO@ ParameterizedType@@Map<String,String> @AT@ 7389 @LENGTH@ 6\n------INS VariableDeclarationFragment@@configurations=getConfigurations() @TO@ VariableDeclarationStatement@@Map<String,Map<String,String>> configurations=getConfigurations(); @AT@ 7398 @LENGTH@ 36\n---------INS SimpleName@@configurations @TO@ VariableDeclarationFragment@@configurations=getConfigurations() @AT@ 7398 @LENGTH@ 14\n---------INS MethodInvocation@@MethodName:getConfigurations:[] @TO@ VariableDeclarationFragment@@configurations=getConfigurations() @AT@ 7415 @LENGTH@ 19\n---INS IfStatement@@if (configurations != null) {  configurations.put(pid,configuration);  setConfigurations(configurations);} @TO@ MethodDeclaration@@public, void, MethodName:setConfiguration, String pid, Map<String,String> configuration,  @AT@ 7444 @LENGTH@ 138\n------INS InfixExpression@@configurations != null @TO@ IfStatement@@if (configurations != null) {  configurations.put(pid,configuration);  setConfigurations(configurations);} @AT@ 7448 @LENGTH@ 22\n---------INS SimpleName@@configurations @TO@ InfixExpression@@configurations != null @AT@ 7448 @LENGTH@ 14\n---------INS Operator@@!= @TO@ InfixExpression@@configurations != null @AT@ 7462 @LENGTH@ 2\n---------INS NullLiteral@@null @TO@ InfixExpression@@configurations != null @AT@ 7466 @LENGTH@ 4\n------INS Block@@ThenBody:{  configurations.put(pid,configuration);  setConfigurations(configurations);} @TO@ IfStatement@@if (configurations != null) {  configurations.put(pid,configuration);  setConfigurations(configurations);} @AT@ 7472 @LENGTH@ 110\n---------INS ExpressionStatement@@MethodInvocation:configurations.put(pid,configuration) @TO@ Block@@ThenBody:{  configurations.put(pid,configuration);  setConfigurations(configurations);} @AT@ 7486 @LENGTH@ 39\n------------INS MethodInvocation@@configurations.put(pid,configuration) @TO@ ExpressionStatement@@MethodInvocation:configurations.put(pid,configuration) @AT@ 7486 @LENGTH@ 38\n---------------INS SimpleName@@Name:configurations @TO@ MethodInvocation@@configurations.put(pid,configuration) @AT@ 7486 @LENGTH@ 14\n---------------INS SimpleName@@MethodName:put:[pid, configuration] @TO@ MethodInvocation@@configurations.put(pid,configuration) @AT@ 7501 @LENGTH@ 23\n------------------INS SimpleName@@pid @TO@ SimpleName@@MethodName:put:[pid, configuration] @AT@ 7505 @LENGTH@ 3\n------------------INS SimpleName@@configuration @TO@ SimpleName@@MethodName:put:[pid, configuration] @AT@ 7510 @LENGTH@ 13\n---------INS ExpressionStatement@@MethodInvocation:setConfigurations(configurations) @TO@ Block@@ThenBody:{  configurations.put(pid,configuration);  setConfigurations(configurations);} @AT@ 7538 @LENGTH@ 34\n------------INS MethodInvocation@@setConfigurations(configurations) @TO@ ExpressionStatement@@MethodInvocation:setConfigurations(configurations) @AT@ 7538 @LENGTH@ 33\n---------------INS SimpleName@@MethodName:setConfigurations:[configurations] @TO@ MethodInvocation@@setConfigurations(configurations) @AT@ 7538 @LENGTH@ 33\n------------------INS SimpleName@@configurations @TO@ SimpleName@@MethodName:setConfigurations:[configurations] @AT@ 7556 @LENGTH@ 14\n"  
  ```  

Or use the following command to access specialized trees:

 ```powershell
hgetall NAME_OF_THE_EXACT_KEY

hgetall MethodDeclaration/40/fuse_67b14b_04e5b1_fabric#fabric-client#src#main#java#org#fusesource#fabric#jolokia#facade#facades#ProfileFacade.java.txt_1

OUTPUT:
1) "tokens"
2) "public  void  MethodName:setConfiguration  String  pid  Map  String  String  configuration  Map  String  Map  String  String  configurations  MethodName:getConfigurations:[]  configurations  !=  null  Name:configurations  pid  configuration  configurations "
3) "targetTree"
4) "[(55@@[(31@@)][(31@@)][(31@@)][(31@@[(44@@)][(44@@)])][(31@@[(44@@[(74@@)][(74@@)][(74@@)])][(44@@)])][(31@@[(60@@[(74@@)][(74@@)][(74@@[(74@@)][(74@@)][(74@@)])])][(60@@[(59@@)][(59@@)])])][(31@@[(25@@[(27@@)][(27@@)][(27@@)])][(25@@[(8@@[(21@@[(32@@)][(32@@[(42@@)][(42@@)])])])][(8@@[(21@@[(32@@[(42@@)])])])])])])]"
5) "actionTree"
6) "[(100@@[(100@@)][(100@@)][(100@@)][(100@@[(100@@)][(100@@)])][(100@@[(100@@[(100@@)][(100@@)][(100@@)])][(100@@)])][(100@@[(100@@[(100@@)][(100@@)][(100@@[(100@@)][(100@@)][(100@@)])])][(100@@[(100@@)][(100@@)])])][(100@@[(100@@[(100@@)][(100@@)][(100@@)])][(100@@[(100@@[(100@@[(100@@)][(100@@[(100@@)][(100@@)])])])][(100@@[(100@@[(100@@[(100@@)])])])])])])]"
7) "shapeTree"
8) "[(31@@[(83@@)][(39@@)][(42@@)][(44@@[(43@@)][(42@@)])][(44@@[(74@@[(43@@)][(43@@)][(43@@)])][(42@@)])][(60@@[(74@@[(43@@)][(43@@)][(74@@[(43@@)][(43@@)][(43@@)])])][(59@@[(42@@)][(32@@)])])][(25@@[(27@@[(42@@)][(-1@@)][(33@@)])][(8@@[(21@@[(32@@[(42@@)][(42@@[(42@@)][(42@@)])])])][(21@@[(32@@[(42@@[(42@@)])])])])])])]"
  ```  

After executing the actionSI / tokenSI steps, the rich edit scripts to be compared are stored in a key in DB 0. Use the following command to verify number of comparison to be made. 
The trees that are labelled to be same are stored in DB2 for action trees and,in DB3 for token trees. 

This command can also be used in order to progress the compare step. When the comparison is completed the following command will return 0.
 ```powershell
scard compare
  ``` 


###### Pickle
The see content of the .pickle file the following script could be used.

  ```python
   import pickle as p
   import gzip
   def load_zipped_pickle(filename):
      with gzip.open(filename, 'rb') as f:
          loaded_object = p.load(f)
          return loaded_object
  ```
Usage

  ```python
  result = load_zipped_pickle('code/LANGbugReportsComplete.pickle')
  # Result is pandas object which can be exported to several formats
  # Details on how to export is listed in offical library documentation
  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html

  ```

