Changelog
=========

1.x
---

1.0
~~~


* Added support for Python ``3.6``, ``3.7`` and ``3.8``; in the opposite, dropped support for old ones (``3.4`` and lower)
* Dropped support for older ``Django`` versions (the oldest one we supporting is ``1.10``)
* A new configuration format allowing create a number of different schemas;
* Get rid off the 3rd party dependency: ``selectel-api``;
* Using ``tox`` and ``pytest`` utilities when developing and testing;
* Using ``poetry`` as package management and deploying tool, so ``setup.py`` is no longer needed;
* All the development utils configs (such as ``.rccoverage``, ``tox.ini`` and so on) also moved in the only ``setup.cfg`` file
* License is MIT


0.3x
----

0.3.1
~~~~~

Released at 2016-03-13

* Fix static storage settings

0.3.0
~~~~~

Released at 2016-02-07

* Drop older python verions support (vv 3.2, 3.3)
* Drop older Django version support (1.6)
* Use tox for testing


0.2x
----

0.2.2
~~~~~

2015-05-23

* Update django head versions

0.2.1
~~~~~

2015-05-02

* Update head django version


0.2.0
~~~~~

2015-04-04

* 5ac502a 2014-10-03 | init? [Mikhail Porokhovnichenko]
