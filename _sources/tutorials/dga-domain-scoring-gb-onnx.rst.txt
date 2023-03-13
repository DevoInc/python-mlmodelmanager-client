DGA domain scoring (GB-ONNX)
============================

This tutorial shows how to perform real-time `DGA` domain classification using
a machine learning model to have as output the classification probability
`(score)`.

We will use the
`Gradient Boosting <https://en.wikipedia.org/wiki/Gradient_boosting>`_
algorithm from the `scikit-learn <https://scikit-learn.org/>`_ library to
create a model capable of detecting whether a domain is malicious. Then we will
transform the model into `ONNX <https://onnx.ai/>`_ format in order to
aggregate the scoring of the classification. Finally, we will register the
model in **ML Model Manager** to enable it in the `Devo <https://www.devo.com>`_
platform and exploit it through Devo query engine.

.. note::

    `The tutorial is available as a Jupyter notebook
    <https://github.com/DevoInc/python-mlmodelmanager-client/blob/main/notebooks/dga-domain-scoring-gb-onnx.ipynb>`_.

Requirements
------------

* Python >= 3.7.
* Devo table ``demo.ecommerce.data``.

It is recommended for convenience to create a virtual environment to run the
tutorial or use the notebook provided.

Setup
-----

Let's start by installing the required packages. Open your favourite terminal
and type the following command.

.. code-block:: bash

    $ pip install devo-sdk \
        devo-mlmodelmanager \
        numpy \
        onnx \
        onnxruntime \
        pandas \
        scikit-learn \
        skl2onnx

We are ready to start coding, so in your coding environment let's start by
the needed imports.

.. code-block::

    import os
    import math
    import time
    import numpy as np
    import pandas as pd

    from onnx import TensorProto
    from onnx.defs import ONNX_ML_DOMAIN
    from onnx.helper import make_node, make_tensor_value_info
    from onnxruntime import InferenceSession
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.metrics import f1_score
    from sklearn.model_selection import train_test_split
    from skl2onnx import convert_sklearn, to_onnx
    from skl2onnx.common.data_types import FloatTensorType
    from devo.api import Client, ClientConfig, SIMPLECOMPACT_TO_OBJ
    from devo_ml.modelmanager import create_client_from_token, engines

Declare some constants for convenience in the code.

.. code-block::

    # A valid Devo access token
    DEVO_TOKEN = '<your_token_here>'

    # URL of Devo API, e.g. https://apiv2-us.devo.com/search/query/
    DEVO_API_URL = '<devo_api_url_here>'

    # URL of Devo ML Model Manager, e.g. https://api-us.devo.com/mlmodelmanager/
    DEVO_MLMM_URL = '<devo_mlmm_url_here>'

    # The domain to connect to, e.g. self
    DOMAIN = '<your_domain_here>'

    # The name of the model
    MODEL_NAME = 'dga_scoring'

    # The description of the models
    MODEL_DESCRIPTION = 'DGA domain label scoring'

    # File to store the onnx model
    MODEL_FILE = f'{MODEL_NAME}.onnx'

    # The URL of a dataset to build the model
    DATASET_URL = "https://devo-ml-models-public-demos.s3.eu-west-3.amazonaws.com/legit_dga/dataset.csv"

  # Random seed to initialize random variables
    RANDOM_SEED = 42

Prepare the data
----------------

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

With the `pandas <https://pandas.pydata.org/>`_ library we can handle and
transform data in a simple way, so create a `pandas.DataFrame
<https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ from the
dataset.

.. code-block::

    df = pd.read_csv(DATASET_URL, sep=';')

This is the dataset as a `pandas.DataFrame`.

.. code-block::

    >>> df.head()
                      host          domain  class subclass
    0  000directory.com.ar    000directory  legit    legit
    1       000webhost.com      000webhost  legit    legit
    2          001fans.com         001fans  legit    legit
    3   01-telecharger.com  01-telecharger  legit    legit
    4       010shangpu.com      010shangpu  legit    legit


We need to add the columns ``length``,
``entropy`` and ``vowel_proportion`` for each domain, and also the flag
``malicious`` indicating if it is a DGA domain according to the ``class``
column value.

.. code-block::

    def entropy(text):
        """Helper function to calculate the Shannon entropy of a text."""
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum([p * math.log(p) / math.log(2.0) for p in prob])

    df = df[~df['subclass'].isna()]
    df['length'] = df['domain'].apply(lambda x: len(x))
    df['vowel_proportion'] = df['domain'].apply(lambda x: sum([x.lower().count(v) for v in "aeiou"]) / len(x))
    df['entropy'] = df['domain'].apply(lambda x: entropy(x))
    df['malicious'] = df['class'].apply(lambda x: int(x != 'legit'))

This is the dataset ready to use.

.. code-block::

    >>> df.head()
                      host          domain  class subclass  length  vowel_proportion   entropy  malicious
    0  000directory.com.ar    000directory  legit    legit      12          0.250000  3.022055          0
    1       000webhost.com      000webhost  legit    legit      10          0.200000  2.846439          0
    2          001fans.com         001fans  legit    legit       7          0.142857  2.521641          0
    3   01-telecharger.com  01-telecharger  legit    legit      14          0.285714  3.324863          0
    4       010shangpu.com      010shangpu  legit    legit      10          0.200000  3.121928          0


Build the model
---------------

We are now ready to build the model. We will rely on a
`sklearn GradientBoostingClassifier <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html/>`_ for that.

.. code-block::

    X_data = df[['length', 'vowel_proportion', 'entropy']].values
    y_data = df['malicious'].values

    # Split the data in test and train chunks
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, random_state=RANDOM_SEED)

    model = GradientBoostingClassifier(random_state=RANDOM_SEED)

    # Train the model
    model = model.fit(X_train, y_train)

We can now check the accuracy of our model. We will use the
`F-score <https://en.wikipedia.org/wiki/F-score>`_ measure provided by the
`sklearn.metrics.f1_score <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html>`_
function.

The ``X_test`` chunk splited before allows us to validate the model.

.. code-block::

    # Validate how good is the model
    pred_test = model.predict(X_test)
    score = f1_score(y_test, pred_test)

.. code-block::

    >>> print(f'F1-Score: {score:.4f}')
    F1-Score: 0.9199

`F1 score` reaches its best value at ``1`` and worst score at ``0``. We have
``0.9199``, so our model has a goog accuracy. So far so good.

Transform into ONNX
-------------------

In order to calculate the `scoring` we need to transform the model to `ONNX`
format first. We will use the
`skl2onnx.to_onnx <https://onnx.ai/sklearn-onnx/api_summary.html?highlight=to_onnx#skl2onnx.to_onnx>`_
function of the `sklearn-onnx <https://onnx.ai/sklearn-onnx/index.html>`_
library for that.

.. code-block::

    # Transform to ONNX format
    onnx_model = to_onnx(
        model,
        X_train.astype(np.float32),
        target_opset=13,
    )

We now proceed to the calculation of the score. This is done by modifying the
ONNX graph, removing the current output of the model and adding nodes to
compute the desired output.

.. code-block::

    # Remove all defined outputs
    while onnx_model.graph.output:
        _ = onnx_model.graph.output.pop()

    # Remove node ZipMap since it won't be necessary
    n_nodes = len(onnx_model.graph.node)
    for i in range(n_nodes):
        if onnx_model.graph.node[i].name == 'ZipMap':
            del onnx_model.graph.node[i]
            break

    # Define the outputs by adding proper nodes

    onnx_model.graph.node.append(
        make_node(
            'Constant',
            inputs=[],
            outputs=['output_pos'],
            value_int=0,
        )
    )
    onnx_model.graph.node.append(
        make_node(
            'ArrayFeatureExtractor',
            inputs=['probabilities', 'output_pos'],
            outputs=['output_probability_at'],
            domain=ONNX_ML_DOMAIN,
        )
    )
    onnx_model.graph.output.append(
        make_tensor_value_info(
            name='output_probability_at',
            elem_type=TensorProto.FLOAT,
            shape=[-1, 1],
        )
    )

.. note::

    Refer to `ONNX documentation <https://onnx.ai/onnx/intro/>`_ to learn more
    about to manipulate an `ONNX` graph.

We can check is the transformed model works correctly by comparing the
predictions of the ``model`` and ``onnx_model``.

.. code-block::

    # Predict with ONNX model
    session = InferenceSession(onnx_model.SerializeToString())
    input_name = session.get_inputs()[0].name
    result = session.run(None, {input_name: X_test.astype(np.float32)})
    onnx_scores = result[0].reshape(-1)

    # Predict with model
    scores = model.predict_proba(X_test)[:, 0]

    # Compare predictions
    threshold = 1e-3
    prediction_validation = (np.abs(scores - onnx_scores) < threshold).all()

.. code-block::

    >>> print(f'Predictions are similar: {prediction_validation}')
    Predictions are similar: True

Great, seems our ``onnx_model`` is valid, now let's to save it.

.. code-block::

    with open(MODEL_FILE, 'wb') as fp:
        fp.write(onnx_model.SerializeToString())

Register the model
------------------

Once the model has been built and saved, it must be registered on the
Devo platform in order to exploit it. We will use the ML Model Manager Client
for that.

.. code-block::

    # create the mlmm client
    mlmm = create_client_from_token(DEVO_MLMM_URL, DEVO_TOKEN)

    # register the model
    mlmm.add_model(
        MODEL_NAME,
        engines.ONNX,
        MODEL_FILE,
        description=MODEL_DESCRIPTION,
        force=True
    )

.. note::

    Refer to :ref:`user_guide/index:User's Guide` of this documentation to
    learn more about the ML Model Manager Client.

So far we are ready to exploit our model, i.e. to score domains according to
how malicious they are.

Scoring domains
---------------

One way to evaluate a model is to use the ``mlevalmodel(...)`` operator when
querying a table. The ``mlevalmodel(...)`` operator is capable of evaluating
machine learning models and is available in the Devo query engine.

We are going to use the ``demo.ecommerce.data`` table, which contains the
``referralUri`` field, from which we can extract the domain we want to score.

A query that might be worthwhile would be something like this.

.. code-block::

    query = f'''from demo.ecommerce.data
    select
        eventdate,
        split(referralUri, "/", 2) as domain
    group by domain every -
    select
        float4(length(domain)) as length,
        float4(shannonentropy(domain)) as entropy,
        float4(countbyfilter(domain, "aeiouAEIOU") / length) as vowel_proportion,
        at(mlevalmodel(
            "{DOMAIN}",
            "{MODEL_NAME}",
            [length, vowel_proportion, entropy]
        ), 0) as score
    '''

.. note::

    Refer to `Build a query using LINQ
    <https://docs.devo.com/space/latest/95191261/Build+a+query+using+LINQ>`_
    to learn more about queries.

Well, now we just need to create an access to the Devo API and launch the
query.

With the `Devo Python SDK <https://github.com/DevoInc/python-sdk>`_
we can execute queries against the Devo platform easily
and securely.

.. code-block::

    # create a Devo API client
    api = Client(
        auth={"token": DEVO_TOKEN},
        address=DEVO_API_URL,
        config=ClientConfig(
            response="json/simple/compact",
            stream=True,
            processor=SIMPLECOMPACT_TO_OBJ
        )
    )
    response = api.query(
        query=query,
        dates={'from': 'now() - 1 * hour()', 'to': 'now()'}
    )

    for row in response:
        print(f"{row['domain']} -> {row['score']})

You will see the scoring like the following depending on the contents of the
``demo.ecommerce.data`` table.

.. code-block::

    >>>
    www.bing.com -> 0.0182034969329834
    www.google.com -> 0.5790193676948547
    www.logcasts.com -> 0.24745863676071167
    www.logtrust.com -> 0.28057998418807983
    ...

.. note::

    Refer to `Query API <https://docs.devo.com/space/latest/95128275>`_
    to learn more about the Devo Query API.
