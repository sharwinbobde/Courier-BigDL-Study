# QPE-Group-12

## Running experiments

The main code to run in order to get the results is in `Run-Experiments.ipynb`. Here you can configure
the parameters such as number of epochs, place to save the logs, etc...

In order to be able to run the script you need to have accessible your GCLOUD private key (normally
stored in the `.ssh` folder in linux), and also create a service account and a `.json` key for the
libcloud driver.

The experiments to run are saved in `.csv` format in the `experiment_designs` folder, both for the 
2k factorial as for the full factorial.

## Generating the experiments

In case you want to tweak or change those files you can just edit the `create-experiments.ipynb` 
notebook, and change the factors and levels directly there.

## CPU and IO wait script

To get the measurements from the different servers, you need to copy the `cpu_io_stats.py` files to
your servers, and specify in the main notebook the location of this file. This outputs a pickle file 
with the cpu and io wait percentages every interval seconds.

