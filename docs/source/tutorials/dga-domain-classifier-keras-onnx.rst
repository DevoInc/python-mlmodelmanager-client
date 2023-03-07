DGA domain classifier (Keras-ONNX)
==================================

This tutorial is related to the
:ref:`DGA domain classifier using H2O engine tutorial
<tutorials/dga-domain-classifier:DGA domain classifier>`
but in this case is used `Keras <https://keras.io/>`_ as machine learning engine.

We are going to use the `Keras framework <https://github.com/keras-team/keras>`_
to create a model capable of detecting whether a domain is malicious
or not. Then in order to be able to register and use the `Keras` model in
`Devo <https://www.devo.com>`_ we will show how to transform it into `ONNX`
format.

.. note::

    `The tutorial is available as a Jupyter notebook
    <https://github.com/DevoInc/python-mlmodelmanager-client/blob/main/notebooks/dga-domain-classifier-keras-onnx.ipynb>`_.

Build the model
---------------


Let's start by installing the required packages.

.. code-block:: bash

    $ pip install devo-sdk
    $ pip install devo-mlmodelmanager
    $ pip install tensorflow
    $ pip install tf2onnx
    $ pip install scikit-learn
    $ pip install numpy
    $ pip install pandas

We can start coding by the needed imports.

.. code-block::

    import os
    import math
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import tensorflow as tf
    import tf2onnx

    from collections import Counter
    from sklearn.preprocessing import LabelEncoder
    from devo.api import Client, ClientConfig, SIMPLECOMPACT_TO_OBJ
    from devo_ml.modelmanager import create_client_from_token, engines

Declare some constants for convenience in the code.

.. code-block::

    # A valid Devo access token
    TOKEN = '<your_token_here>'

    # URL of Devo API, e.g. https://apiv2-us.devo.com/search/query/
    DEVO_API_URL = '<devo_api_url_here>'

    # URL of Devo ML Model Manager, e.g. https://api-us.devo.com/mlmodelmanager/
    DEVO_MLMM_URL = '<devo_mlmm_url_here>'

    # The domain to connect to, e.g. self
    DOMAIN = '<your_domain_here>'

    # The name of the model
    NAME = 'dga_classifier_onnx'

    # The description of the models
    DESCRIPTION = 'DGA domain classifier (Keras-ONNX)'

    # File to store the onnx model
    MODEL_FILE = f'{NAME}.onnx'

    # The URL of a dataset to build the model
    DATASET_URL = "https://devo-ml-models-public-demos.s3.eu-west-3.amazonaws.com/legit_dga/dataset.csv"

    VOWELS = "aeiouAEIOU"

    # fix random seed for reproducibility
    seed = 42
    np.random.seed(seed)

This `dataset
<https://devo-ml-models-public-demos.s3.eu-west-3.amazonaws.com/legit_dga/dataset.csv>`_
will help us to train our model once it has been built. The dataset has the
form ``host;domain;class;subclass``.

.. code-block:: text

    host;domain;class;subclass
    000directory.com.ar;000directory;legit;legit
    001fans.com;001fans;legit;legit
    ...
    1002n0q11m17h017r1shexghfqf.net;1002n0q11m17h017r1shexghfqf;dga;newgoz
    100bestbuy.com;100bestbuy;legit;legit
    ...

In the dataset preparation we will add the columns ``length``, ``entropy`` and
``vowel_proportion`` for each domain, and also the flag ``malicious`` indicating
if it is a DGA domain according to the ``class`` column value.

.. code-block::

    def entropy(s):
        l = len(s)
        return -sum(map(lambda a: (a/l)*math.log2(a/l), Counter(s).values()))

    domains = pd.read_csv(DATASET_URL, ';')

    domains = domains[~domains['subclass'].isna()]
    domains['length'] = domains['domain'].str.len()
    domains['entropy'] = domains['domain'].apply(lambda row: entropy(row))
    domains['vowel_proportion'] = 0
    for v in VOWELS:
        domains['vowel_proportion'] += domains['domain'].str.count(v)
    domains['vowel_proportion'] /= domains['length']
    domains['malicious'] = domains['class'] != 'legit'

After preparation our dataset of domains should looks like this.

.. code-block::

    >>> domains.head()
                     host         domain class subclass length  entropy vowel_proportion malicious
    0 000directory.com.ar   000directory legit    legit     12 3.022055         0.250000     False
    1      000webhost.com     000webhost legit    legit     10 2.846439         0.200000     False
    2         001fans.com        001fans legit    legit      7 2.521641         0.142857     False
    3  01-telecharger.com 01-telecharger legit    legit     14 3.324863         0.285714     False
    4      010shangpu.com     010shangpu legit    legit     10 3.121928         0.200000     False

.. note::

    Be aware that our dataset is a `pandas.DataFrame
    <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_.

We are now ready to build the model. We will rely on a
`Keras Sequential model <https://keras.io/guides/sequential_model/>`_ for that.

.. code-block::

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
        10,
        input_dim=3,
        activation=tf.nn.relu,
        kernel_initializer='he_normal',
        kernel_regularizer=tf.keras.regularizers.l2(0.01)
    ))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(
        7,
        activation=tf.nn.relu,
        kernel_initializer='he_normal',
        kernel_regularizer=tf.keras.regularizers.l1_l2(l1=0.001, l2=0.001)
    ))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(
        5,
        activation=tf.nn.relu,
        kernel_initializer='he_normal',
        kernel_regularizer=tf.keras.regularizers.l1_l2(l1=0.001, l2=0.001)
    ))
    model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

Before we can train our model we have to properly transform the data for `Keras`.

.. code-block::

    Y = domains['malicious']
    X = domains.drop(
        ['host', 'domain', 'class', 'subclass', 'malicious'],
        axis=1
    )

    # Keras requires your output feature to be one-hot encoded values.
    lbl_clf = LabelEncoder()
    Y_final = tf.keras.utils.to_categorical(lbl_clf.fit_transform(Y))

Let's train our model with our transformed datasets, ``X`` and ``Y_final``.

.. code-block::

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.fit(X , Y_final , epochs=10,  batch_size=7)

You will see the progress of the training in the output, something like this.

.. code-block::

    >>>
    Epoch 1/10
    19133/19133 [==============================] - 59s 3ms/step - loss: 0.4520 - accuracy: 0.8100
    Epoch 2/10
    19133/19133 [==============================] - 58s 3ms/step - loss: 0.4413 - accuracy: 0.8037
    Epoch 3/10
    19133/19133 [==============================] - 54s 3ms/step - loss: 0.4282 - accuracy: 0.8098
    Epoch 4/10
    19133/19133 [==============================] - 54s 3ms/step - loss: 0.4301 - accuracy: 0.8098
    Epoch 5/10
    19133/19133 [==============================] - 55s 3ms/step - loss: 0.4299 - accuracy: 0.8085
    Epoch 6/10
    19133/19133 [==============================] - 55s 3ms/step - loss: 0.4249 - accuracy: 0.8124
    Epoch 7/10
    19133/19133 [==============================] - 54s 3ms/step - loss: 0.4284 - accuracy: 0.8101
    Epoch 8/10
    19133/19133 [==============================] - 57s 3ms/step - loss: 0.4292 - accuracy: 0.8083
    Epoch 9/10
    19133/19133 [==============================] - 58s 3ms/step - loss: 0.4295 - accuracy: 0.8096
    Epoch 10/10
    19133/19133 [==============================] - 57s 3ms/step - loss: 0.4278 - accuracy: 0.8091
    <keras.callbacks.History at 0x7f02e1620610>

.. note::

    The `Keras framework` is beyond the scope of this tutorial, please, refer
    to `Keras API reference <https://keras.io/api/>`_ to learn more.

Register the model
------------------

In order to register the model in Devo we need to transform it to `ONNX` format
first.

We will use the
`tf2onnx <https://onnxruntime.ai/docs/tutorials/tf-get-started.html>`_
tool to convert our `Keras` model to `ONNX`.

.. code-block::

    tf2onnx.convert.from_keras(model, opset=13, output_path=MODEL_FILE)

Once the model has been transformed and saved, it must be registered on the
Devo platform in order to exploit it.

We will use the ML Model Manager Client for that.

.. code-block::

    # create the mlmm client
    mlmm = create_client_from_token(DEVO_MLMM_URL, TOKEN)

    # register the model
    mlmm.add_model(
        NAME,
        engines.ONNX,
        MODEL_FILE,
        description=DESCRIPTION,
        force=True
    )

.. note::

    Refer to :ref:`user_guide/index:User's Guide` of this documentation to learn
    more about the ML Model Manager Client.

So far we have everything ready to exploit our model, i.e. to detect
malicious domains.

Classify domains
----------------

One way to evaluate a model is to use the ``mlevalmodel(...)`` operator when
querying a table. The ``mlevalmodel(...)`` operator is capable of evaluating
machine learning models and is available in the Devo query engine.

We are going to use the ``demo.ecommerce.data`` table, which contains the
``referralUri`` field, from which we can extract the domain we want to check.

A query that might be worthwhile would be something like this.

.. code-block::

    query = f'''from demo.ecommerce.data
      select split(referralUri, "/",2) as domain,
      float(length(domain)) as length,
      shannonentropy(domain) as entropy,
      float(countbyfilter(domain, "{VOWELS}")) as vowel_proportion,
      at(mlevalmodel("{DOMAIN}", "{NAME}", [float4(length), float4(vowel_proportion)]),0) as res,
      ifthenelse(res>0.5, "false", "true") as isMalicious
    '''

.. note::

    Refer to `Build a query using LINQ
    <https://docs.devo.com/space/latest/95191261/Build+a+query+using+LINQ>`_
    to learn more about queries.

Well, now we just need to create an access to the Devo API and launch the
query.

With the `Devo Python SDK <https://github.com/DevoInc/python-sdk>`_,
among other features, we can execute queries against the Devo platform easily
and securely.

.. code-block::

    # create a Devo API client
    api = Client(
        auth={"token": TOKEN},
        address=DEVO_API_URL,
        config=ClientConfig(
            response="json/simple/compact",
            stream=True,
            processor=SIMPLECOMPACT_TO_OBJ
        )
    )

    response = api.query(query=query, dates={'from': "now()-1*hour()"})

    for row in response:
        print("domain: ",row['domain'], "isMalicious:", row['isMalicious'])

You will see a result like the following depending on the contents of the
``demo.ecommerce.data`` table.

.. code-block::

    >>>
    domain:  www.logcasts.com isMalicious: false
    domain:  www.google.com isMalicious: false
    domain:  www.logtrust.com isMalicious: false
    ...

.. note::

    Refer to `Query API <https://docs.devo.com/space/latest/95128275>`_
    to learn more about the Devo Query API.
