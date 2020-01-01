.. _install:

.. |PATH| raw:: html

    https://raw.githubusercontent.com/back-to/ipk/master/build/

.. |br| raw:: html

  <br />

Installation
============

Source code
-----------

There are a few different methods to do this,
`pip <https://pip.readthedocs.io/en/latest/installing/>`_ the Python package
manager, or by checking out the latest code with
`Git <https://git-scm.com/downloads>`_.

The commands listed here will also upgrade any existing version of LiveProxy.

.. rst-class:: table-custom-layout

==================================== ===========================================
Version                              Installing
==================================== ===========================================
`Latest release (pip)`_              .. code-block:: console

                                        # pip install -U liveproxy
`Development version (pip)`_         .. code-block:: console

                                        # pip install -U git+https://github.com/back-to/liveproxy.git

`Development version (git)`_         .. code-block:: console

                                        $ git clone git://github.com/back-to/liveproxy.git
                                        $ cd liveproxy
                                        # python setup.py install
==================================== ===========================================

.. _Latest release (pip): https://pypi.org/project/liveproxy/
.. _Development version (pip): https://github.com/back-to/liveproxy
.. _Development version (git): https://github.com/back-to/liveproxy

Dependencies
^^^^^^^^^^^^

To install LiveProxy from source you will need these dependencies.

.. rst-class:: table-custom-layout

==================================== ===========================================
Name                                 Notes
==================================== ===========================================
`Python`_                            At least version **2.7** or **3.6**.
`python-setuptools`_

**Automatically installed by the setup script**
--------------------------------------------------------------------------------
`python-streamlink`_                 At least version **1.2.0**.
==================================== ===========================================

.. _Python: https://www.python.org/
.. _python-setuptools: https://pypi.org/project/setuptools/
.. _python-streamlink: https://pypi.org/project/streamlink/

Kodi
----

  LiveProxy can be used as a **service proxy** for Kodi **IPTV Simple PVR**

  Download `repository.back-to`_

  Install *service.liveproxy*

  .. Note:: A Kodi restart is recommended.

.. _repository.back-to: https://github.com/back-to/repo/raw/master/repository.back-to/repository.back-to-5.0.0.zip


Enigma2
-------

  The E2 version will run the command ``liveproxy --host 0.0.0.0`` |br|
  which can be used for local testing without the receiver.

  The build files can be found at https://github.com/back-to/ipk

opkg files
^^^^^^^^^^

  At the begin you will install the packages from ``opkg``

  .. code-block:: bash

    opkg install python-pkgutil
    opkg install python-futures
    opkg install python-singledispatch
    opkg install python-six
    opkg install python-requests
    opkg install python-pycrypto

download files
^^^^^^^^^^^^^^

  You will have to download all required files, |br|
  for this example all the files will be saved in ``/tmp``

  The best way is to use the terminal, |br|
  from the terminal you can use ``wget URL`` to download the files |br|
  and ``cd /tmp`` to get into the example direction.

  All these files are required.

  - \ |PATH|\ python-backports.shutil-get-terminal-size_1.0.0_all.ipk
  - \ |PATH|\ python-backports.shutil-which_3.5.1_all.ipk
  - \ |PATH|\ python-iso3166_1.0_all.ipk
  - \ |PATH|\ python-iso639_0.4.5_all.ipk
  - \ |PATH|\ python-isodate_0.6.0_all.ipk
  - \ |PATH|\ python-socks_1.7.1_all.ipk
  - \ |PATH|\ python-websocket_0.47.0_all.ipk
  - \ |PATH|\ python-streamlink_1.2.0.50_all.ipk
  - \ |PATH|\ python-liveproxy_0.3.0_all.ipk

install
^^^^^^^

  For the install after the download,
  you will have to use ``opkg install PATH_IPK``

  .. note::

    Install python-streamlink and python-liveproxy as the last packages

  .. hint::

    You can use the **TAB** key, to autocomplete names |br| |br|
    *opkg install /tmp/py* |br|
    **TAB** will be *opkg install /tmp/python-* |br| |br|
    *opkg install /tmp/python-so* |br|
    **TAB** will be *opkg install /tmp/python-socks_1.7.1_all.ipk*

after install
^^^^^^^^^^^^^

  You can test your Streamlink installation in your terminal.

  Type

  ::

    streamlink -l debug

  it should output some information about Streamlink and your system.

service
^^^^^^^

  Now that Streamlink works, you will have to install the service script.

  .. note::

      This will only work for receiver with *init.d*

  **download**

    - \ |PATH|\ enigma2-liveproxy-server_1.0.0_all.ipk

  **install**

    ::

      opkg install /tmp/enigma2-liveproxy-server_1.0.0_all.ipk

  **start the server**

    ::

      update-rc.d liveproxy-server defaults

Known issues
^^^^^^^^^^^^

SystemTimeWarning
^^^^^^^^^^^^^^^^^

  This issue comes up if your receiver starts without a satellite signal.

  ::

    /usr/lib/python2.7/site-packages/requests/packages/urllib3/connection.py:303:
    SystemTimeWarning: System time is way off (before 2014-01-01).
    This will probably lead to SSL verification errors SystemTimeWarning

  To solve this, you need to install **Network Time Protocol (NTP)** service

  After the install you might need to run

  ::

    update-rc.d ntpupdate.sh defaults
