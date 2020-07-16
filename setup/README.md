# Installation

Install Anaconda if not already installed. You can use Miniconda for faster installation:

On Linux:
```
    $ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    $ chmod +x miniconda.sh
    $ ./miniconda.sh
    $ export PATH=$HOME/miniconda3/bin:$PATH
```

On Mac or Windows:
    Install Miniconda from [here](https://conda.io/en/latest/miniconda.html)

Next perform the necessary conda installations by running the command.

```
    $ conda env create -f environment.yml
```

This creates a new conda environment called fsmGen. To execute this project you must be in a terminal currently using that conda environment.

After initial installation you can activate the conda environment with:

```
    $ conda activate fsmGen
``` 

To deactivate the environment you are no longer using run the command:

```
    $ conda deactivate
``` 

If you are done working with the project and wish to delete the created conda environment you can delete the environment by running:

```
    $ conda env remove --name fsmGen
```
