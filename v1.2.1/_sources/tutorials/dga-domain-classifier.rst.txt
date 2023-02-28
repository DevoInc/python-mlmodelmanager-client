DGA domain classifier
=====================

This tutorial shows how to perform real-time `DGA` domain classification using
a machine learning model for logs stored in the `Devo <https://www.devo.com>`_
platform.

Domain generation algorithms, `DGA`, are algorithms seen in various families of
malware that are used to periodically generate a large number of domain names
that can be used as rendezvous points with their command and control servers.

For example, an infected computer could create thousands of domain names such
as: www.<gibberish>.com and would attempt to contact a portion of these with
the purpose of receiving an update or commands. See
`DGA on Wikipedia <https://en.wikipedia.org/wiki/Domain_generation_algorithm>`_
to learn more about domain generation algorithms.

We are going to develop a simple machine learning model capable of classifying
malicious domains in the *demo.ecommerce.data* table. We will use the Machine
Learning `H2O <https://h2o.ai/>`_ framework to build and train our model,
the Machine Learning Model Manager Client to register it on the Devo platform,
and the `Devo Python SDK <https://github.com/DevoInc/python-sdk>`_ framework to
evaluate and classify in real time the domains in the table using a query.

.. note::

    `The tutorial is available as a Jupyter notebook
    <https://github.com/DevoInc/python-mlmodelmanager-client/blob/main/notebooks/dga-domain-classifier.ipynb>`_.

Build the model
---------------

Let's start by installing the required packages.

.. code-block:: bash

    $ pip install devo-sdk
    $ pip install devo-mlmodelmanager
    $ pip install h2o

Then the needed imports.

.. code-block::

    import os
    import h2o

    from h2o.estimators import H2OGradientBoostingEstimator
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
    NAME = 'dga_classifier'

    # The description of the models
    DESCRIPTION = 'DGA domain classifier'

    # The path where model file will be stored
    MODELS_PATH = '~/models'

    # The URL of a dataset to build the model
    DATASET_URL = "https://devo-ml-models-public-demos.s3.eu-west-3.amazonaws.com/legit_dga/dataset.csv"

    VOWELS = "aeiouAEIOU"

We use the `h2o <https://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/index.html>`_
library to create a model capable of detecting whether a domain is malicious or
not and this `dataset
<https://devo-ml-models-public-demos.s3.eu-west-3.amazonaws.com/legit_dga/dataset.csv>`_
, which has the form: *host;domain;class;subclass.*

.. code-block:: text

    host;domain;class;subclass
    000directory.com.ar;000directory;legit;legit
    000webhost.com;000webhost;legit;legit
    001fans.com;001fans;legit;legit
    ...
    1002n0q11m17h017r1shexghfqf.net;1002n0q11m17h017r1shexghfqf;dga;newgoz
    1002ra86698fjpgqke1cdvbk5.org;1002ra86698fjpgqke1cdvbk5;dga;newgoz
    1008bnt1iekzdt1fqjb76pijxhr.org;1008bnt1iekzdt1fqjb76pijxhr;dga;newgoz
    100bestbuy.com;100bestbuy;legit;legit
    ...

In the dataset preparation we will add the columns ``length``, ``entropy`` and
``vowel_proportion`` for each domain, and also the flag ``malicious`` indicating
if it is a DGA domain according to the ``class`` column value.

As a result we will have a model saved in a file in `~/models`.

.. code-block::

    h2o.init()

    # import dataset
    domains = h2o.import_file(DATASET_URL, header=1)

    # Prepare dataset
    domains = domains[~domains['subclass'].isna()]
    domains['length'] = domains['domain'].nchar()
    domains['entropy'] = domains['domain'].entropy()
    domains['vowel_proportion'] = 0
    for v in VOWELS:
        domains['vowel_proportion'] += domains['domain'].countmatches(v)
    domains['vowel_proportion'] /= domains['length']
    domains['malicious'] = domains['class'] != 'legit'
    domains['malicious'] = domains['malicious'].asfactor()

    # split dataset
    train, valid = domains.split_frame(ratios=[.8], seed=1234)

    # create and train the model
    model = H2OGradientBoostingEstimator(model_id=NAME)
    model.train(
        x=['length', 'entropy', 'vowel_proportion'],
        y='malicious',
        training_frame=train,
        validation_frame=valid
    )

    # save the model
    os.makedirs(MODELS_PATH, exist_ok=True)
    model.download_mojo(path=MODELS_PATH)

    h2o.cluster().shutdown()

.. note::

    The aim of this tutorial is to show the integration of the ML Model
    Manager Client into the machine learning process not the development of
    an optimal and accurate machine learning model.

Register the model
------------------

Once the model has been developed and saved, it must be registered on the
Devo platform in order to exploit it. For this we will use the ML Model Manager
Client.

.. code-block::

    # create the mlmm client
    client = create_client_from_token(DEVO_MLMM_URL, TOKEN)

    # register the model
    client.add_model(
        NAME,
        engines.H2O,
        os.path.join(MODELS_PATH, f"{NAME}.zip"),
        description=DESCRIPTION,
        force=True
    )

.. note::

    Refer to :ref:`user's guide <User's Guide>` of this documentation to learn
    more about the ML Model Manager Client.

So far we have everything ready to exploit our model.

Classify domains
----------------

One way to evaluate a model is is by querying a table and the
``mlevalmodel(...)`` operator available in the Devo query engine capable
of evaluating machine learning models.

We are going to use the *demo.ecommerce.data* table, which contains the
``referralUri`` field, from which we can extract the domain we want to check.

A query that might be worthwhile would be something like this.

.. code-block::

    query = f'''from demo.ecommerce.data
      select split(referralUri, "/",2) as domain,
      float(length(domain)) as length,
      shannonentropy(domain) as entropy,
      float(countbyfilter(domain, "{VOWELS}")) as vowel_proportion,
      mlevalmodel("{DOMAIN}", "{NAME}", length, entropy, vowel_proportion) as class
    '''

.. note::

    Refer to `Build a query using LINQ
    <https://docs.devo.com/space/latest/95191261/Build+a+query+using+LINQ>`_
    to learn more about queries.

Well, now we just need to create an access to the Devo API and launch the
query. With the `Devo Python SDK <https://github.com/DevoInc/python-sdk>`_,
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
        print(row)

.. note::

    Refer to `Query API <https://docs.devo.com/space/latest/95128275>`_
    to learn more about the Devo Query API.
