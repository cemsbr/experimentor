Quick example
=============

This example shows how to run SSH commands in serial and in parallel.

.. literalinclude:: quick_example.py
   :language: python

Output (with all clocks synchronized)::

  Serial execution
  ================
  58 Hello by vm0
  00 Hello by vm1
  01 Hello by vm2

  Parallel execution
  ==================
  02 Hello by vm2
  02 Hello by vm0
  02 Hello by vm1
