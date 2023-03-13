Entity classification (kmeans-ONNX)
===================================

This tutorial shows how to register and use a ML model in
`ONNX <https://onnx.ai/>`_ format in the `Devo <https://www.devo.com>`_
platform.

``ONNX`` is an open format to represent different machine learning models. There
are many frameworks like *Pytorch*, *Libsvm*, *Keras*, *Mxnet*, *Tensorflow*,
etc. whose models can be exported to ``ONNX``.

In this example we are going to use the
`scikit-learn <https://scikit-learn.org/>`_ library to perform a classification
task based on unsupervised training using the
`kmeans <https://en.wikipedia.org/wiki/K-means_clustering>`_ clustering method.

Then we convert the model to an ``ONNX`` model before register and exploit it
using the Devo query engine.

.. note::

    `The tutorial is available as a Jupyter notebook
    <https://github.com/DevoInc/python-mlmodelmanager-client/blob/main/notebooks/entity-classification-kmeans-onnx.ipynb>`_.

Requirements
------------

* Python >= 3.7.
* Devo table ``demo.ecommerce.data``.

It is recommended for convenience to create a virtual environment to run the
tutorial or use the notebook provided.

Setup
-----

Let's start by installing the required packages.

.. code-block:: bash

    $ pip install devo-sdk
    $ pip install devo-mlmodelmanager
    $ pip install scikit-learn
    $ pip install onnx
    $ pip install numpy
    $ pip install pandas
    $ pip install skl2onnx

Then the needed imports.

.. code-block::

    import numpy as np
    import pandas as pd
    import onnx

    from onnx import helper, TensorProto
    from onnx.tools import update_model_dims
    from sklearn.cluster import KMeans
    from skl2onnx import convert_sklearn, to_onnx
    from devo.api import Client, ClientConfig, JSON,  SIMPLECOMPACT_TO_OBJ
    from devo_ml.modelmanager import

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
    MODEL_NAME = 'entity_classification_ip'

    # The description of the models
    MODEL_DESCRIPTION = 'Demo of entity classification ip'

    # File to store the onnx model
    MODEL_FILE = f'{MODEL_NAME}.onnx'

Build the model
---------------

Our model will classify the IPs in the *demo.ecommerce* table into three
supposed interest groups: IA, UA, MU.

.. note::

    For simplicity it has been assumed that the number of clusters is 3.
    It is appropriate to use other methods such as the
    `Elbow method <https://en.wikipedia.org/wiki/Elbow_method_(clustering)>`_
    or the
    `Silhouette method <https://en.wikipedia.org/wiki/Silhouette_(clustering)>`_
    to determine the optimal number of clusters in a dataset.

To build and train the model we are going to use the existing data in the table
itself, and to get it we need to create an access to the Devo API to be able to
launch queries.

With the `Devo Python SDK <https://github.com/DevoInc/python-sdk>`_,
among other features, we can execute queries against the Devo platform easily
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

.. note::

    Refer to `Query API <https://docs.devo.com/space/latest/95128275>`_
    to learn more about the Devo Query API.

Now we can extract and prepare the data for our model.

.. code-block::

    query = '''from demo.ecommerce.data where isnotnull(clientIpAddress)
    select
        hour(eventdate) as hour,
        minute(eventdate) as minute,
        second(eventdate) as second,
        clientIpAddress,
        userAgent
    group every 8h by clientIpAddress
    select
        str(clientIpAddress) as sourceIp,
        float4(size(collectcompact(hour))) as unique_hours,
        float4(size(collectcompact(minute))) as unique_mins,
        float4(size(collectcompact(second))) as unique_seconds,
        float4(size(collectcompact(userAgent))) as unique_user_agents,
        float4(avg(bytesTransferred)) as bytestransferred
    '''

    response = api.query(
        query=query,
        dates={'from': 'today() - 2 * day()', 'to': 'today() - 1 * day()'}
    )

    raw_data = pd.DataFrame(
        response,
        columns=[
            'sourceIp',
            'unique_hours',
            'unique_mins',
            'unique_seconds',
            'unique_user_agents',
            'bytestransferred',
        ],
    )

.. note::

    Refer to `Build a query using LINQ
    <https://docs.devo.com/space/latest/95191261/Build+a+query+using+LINQ>`_
    to learn more about queries.

With the data already prepared, it is time to create and train the model. We
use the
`sklearn.cluster.KMeans <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans>`_
class.

.. code-block::

    train_data = raw_data.select_dtypes(include=np.number).to_numpy()

    model = KMeans(
        n_clusters=3,
        init='k-means++',
        verbose=0,
        max_iter=300,
        random_state=42
    ).fit(train_data)

Transform to ONNX
-----------------

Let's now transform the model to ``ONNX`` format.

For that we use the
`skl2onnx.to_onnx <https://onnx.ai/sklearn-onnx/api_summary.html?highlight=to_onnx#skl2onnx.to_onnx>`_
function of the `sklearn-onnx <https://onnx.ai/sklearn-onnx/index.html>`_ library.

.. code-block::

    onnx_model = to_onnx(
        model,
        train_data.astype(np.float32),
        target_opset=13,
    )

Some transformations need to be made to the model output in order to be able to
properly consume it in the Devo platform.

.. code-block::

    # Output: scores (discarded)
    _ = onnx_model.graph.output.pop(1)

    # Output: label (discarded)
    _ = onnx_model.graph.output.pop(0)

    # Last output should be float to work in Devo
    cast_node = helper.make_node(
        'Cast',
        inputs=['label'],
        outputs=['label_cast'],
        name='output_label_cast',
        to=TensorProto.FLOAT,
    )
    onnx_model.graph.node.append(cast_node)
    onnx_model.graph.output.append(
        helper.make_tensor_value_info(
            name='label_cast',
            elem_type=TensorProto.FLOAT,
            shape=[-1],
        )
    )

    # Expand last dimension, so it has two dimensions: batch and item
    # It's required only for the kmeans in sklearn, other algorithms
    # like linear regression do not require this conversion
    onnx_model = onnx.compose.expand_out_dim(onnx_model, dim_idx=1)
    onnx_model = update_model_dims.update_inputs_outputs_dims(
        onnx_model,
        {'X': [-1, 5]},
        {'label_cast': [-1, 1]},
    )

Finally we save the model in a file.

.. code-block::

    with open(MODEL_FILE, 'wb') as fp:
        fp.write(onnx_model.SerializeToString())

Register the model
------------------

Once the model has been converted and saved, it must be registered on the
Devo platform in order to exploit it. For this we will use the ML Model Manager
Client.

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

Classifying
-----------

We use ``mlevalmodel(...)`` operator available in the Devo query engine capable
of evaluating machine learning models to classify IPs with the previous model.

A query that might be worthwhile would be something like this.

.. code-block::

    query = f'''from demo.ecommerce.data where isnotnull(clientIpAddress)
    select
        hour(eventdate) as hour,
        minute(eventdate) as minute,
        second(eventdate) as second,
        clientIpAddress,
        userAgent
    group every 8h by clientIpAddress
    select
        str(clientIpAddress) as sourceIp,
        float4(size(collectcompact(hour))) as unique_hours,
        float4(size(collectcompact(minute))) as unique_mins,
        float4(size(collectcompact(second))) as unique_seconds,
        float4(size(collectcompact(userAgent))) as unique_user_agents,
        float4(avg(bytesTransferred)) as bytestransferred,
        at(mlevalmodel(
            "{DOMAIN}",
            "{MODEL_NAME}",
            [unique_hours, unique_mins, unique_seconds, unique_user_agents, bytestransferred]), 0) as label,
        ifthenelse(label = 0.0, "IU", ifthenelse(label = 1.0, "AU", "MU")) as type
    '''

Using the `api` access to Devo previously created we can fetch the results.

.. code-block::

    response = api.query(
        query=query,
        dates={'from': 'today() - 1 * day()'}
    )

    for row in response:
        print("IP:", row['sourceIp'], "type", row['type'])

.. note::

    The intention of the tutorial is only to demonstrate how to convert a model
    to ``ONNX`` and upload it to the DEVO platform, not to create a valid
    and optimal clustering model.
