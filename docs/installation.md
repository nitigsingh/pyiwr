
<html>
<head>

</head>
<body>
<div style="text-align: center; font-size: 24px; padding: 10px;">
  My Custom Header
</div>
<h1>Install pyiwr</h1>

<p>To install pyiwr, follow these steps:</p>

<ol start="1">
    <li>Create a new Conda environment (named <code>pyiwr</code> in this example) with the required dependencies:</li>
    <pre><code>conda create -n pyiwr python=3.9 jupyter git -c conda-forge</code></pre>
</ol>

<ol start="2">
    <li>Activate the newly created Conda environment:</li>
    <pre><code>conda activate pyiwr</code></pre>
</ol>
<ol start="3">
    <li>Install pyiwr using pip:</li>
    <pre><code>pip install git+https://github.com/nitigsingh/pyiwr.git</code></pre>
</ol>

</body>
</html>

