(how-to-test-plugins)=
# How to test QIIME 2 plugins

This document is a placeholder at the moment. 

Briefly, QIIME 2 provides a test harness to simplify a few of the more repetitive parts of testing. 
This is the `TestPluginBase` class (`qiime2.plugin.testing.TestPluginBase`). 

## Examples
Pending full documentation, here are some references where you can see how aspects of QIIME 2 plugins can be tested:
- [Formats](https://github.com/qiime2/q2-types/blob/master/q2_types/feature_data/tests/test_format.py)
- [Semantic Types](https://github.com/qiime2/q2-types/blob/master/q2_types/feature_data/tests/test_type.py)
- [Transformers](https://github.com/qiime2/q2-types/blob/master/q2_types/feature_data/tests/test_transformer.py)
- [Plugin registration](https://github.com/qiime2/q2-vsearch/blob/master/q2_vsearch/tests/test_plugin_setup.py) - note that testing of plugin registration doesn't require the use of the `TestPluginBase` class. 

You can see an example of all of these in one place [in the q2-sapienns test suite](https://github.com/gregcaporaso/q2-sapienns/tree/07d9686224de41075990b5af705f41d44f48b249/q2_sapienns/tests).
You can learn about the q2-sapienns plugin [here](https://github.com/gregcaporaso/q2-sapienns/blob/main/README.md).  

