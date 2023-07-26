<!DOCTYPE html>
<html>
<head>

</head>
<body>

<h1>Install pyiwr</h1>

<p>To install pyiwr, follow these steps:</p>

<ol start="1">
    <li>Create a new Conda environment (named <code>srt</code> in this example) with the required dependencies:</li>
    <pre><code>conda create -n srt python=3.9 jupyter arm_pyart pandas git -c conda-forge</code></pre>
</ol>

<ol start="2">
    <li>Activate the newly created Conda environment:</li>
    <pre><code>conda activate srt</code></pre>
</ol>
<ol start="3">
    <li>Install pyiwr using pip:</li>
    <pre><code>pip install git+https://github.com/nitigsingh/pyiwr.git</code></pre>
</ol>

</body>
</html>

