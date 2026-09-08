"""Core acceptance tests.

Modules are independent so they can be sharded across processes. Anything that
must exercise the *installed* product (wheel, console script, entry-point
discovery, packaged resources) lives in ``test_installed_product`` so the build
happens once.
"""
