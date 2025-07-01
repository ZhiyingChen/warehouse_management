---
title: Warehouse Management
emoji: 🧩
colorFrom: indigo
colorTo: blue
sdk: docker
sdk_version: "1.33.0"
app_file: app.py
pinned: false
---

# Warehouse Management
**Problem Statement**

This is a problem to solve the situation of warehouse management. There are x cities having demands, and there are y cities available to build warehouses in order to satisfy those demands. The question is
to decide which cities are the best options to build warehouses so that the total cost is minimized of different scenarios.
The distance and transport duration are provided.

A data sample is provided in data_example folder.

**Environment Deployment**


Install Python Executor (version >= 3.8.0), Anaconda IDE is recommended


The required packages are listed in requirements.txt. You can install them using:

<pre><code>
    pip install -r requirements.txt
</code></pre>

Install CPLEX (For this project, you need a CPLEX version >= 20.1.0.):

<pre><code>
    1. run CPLEX installer.
    2. move to {CPLEX_HOME}/python, execute python setup.py.
</code></pre>


**Run**

To run project:

<pre><code>
    1. prepare your input data in a folder, and set the folder as your working dir
    2. execute python launch.py
    3. the results will be shown in the output folder of the set working dir
</code></pre>
