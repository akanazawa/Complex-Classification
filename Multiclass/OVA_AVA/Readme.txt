Before running any thing, you need to make sure you have the following file in this directory:
1.test_multiclass.megam 
2.train_multiclass.megam
These are the training and testing data labeled as classes 1 to 4. These data are pre-processed. If you would like to use different data sets, please run multiclass_data_relable.pyin this folder. It will relabel the data from binary classes to multiclasses. 

Note: multiclass_data_relabel.py is hard coded to be 4 classes in total, and you need to change the file names to the new data file yourself. (Sorry for the laziness)  


ova.py:
This is OneversusAll multiclass classification script.
It utilizes megam, so please make sure you copy the compiled megam in the same folder before running it.
