pyiwr can be installed as shown below:

```shell
conda create -n srt python=3.9 jupyter arm_pyart pandas git -c conda-forge
conda activate srt
pip install git+https://github.com/nitigsingh/pyiwr.git
