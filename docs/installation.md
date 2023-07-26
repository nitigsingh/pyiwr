To install `pyiwr`, follow these steps:

1. Create a new Conda environment (named `srt` in this example) with the required dependencies:

```shell
conda create -n srt python=3.9 jupyter arm_pyart pandas git -c conda-forge
```

2. Activate the newly created Conda environment:

```shell
conda activate srt
```

3. Install `pyiwr` using pip:

```shell
pip install git+https://github.com/nitigsingh/pyiwr.git
```

