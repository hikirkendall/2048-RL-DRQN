from ai.dfnn import Layer, DFCNN
import tensorflow as tf
import numpy as np

def expect_equal(value1, value2):
    # value1, value2 are numpy.ndarray (or like)
    if np.array_equal(value1, value2):
        print "Passed!"
    else:
        print "Failed!"

graph = tf.Graph()

with graph.as_default():

    sample_data = tf.constant([[6., 7., 8., 9., 10.], [1., 2., 3., 4., 5.]])
    layer_nn = Layer(5, 3)

    layer = Layer(5, 1)
    layer_clone = layer.clone()

    value = layer(sample_data)
    cvalue = layer_clone(sample_data)

    nn = DFCNN([5, 3, 1])
    nn_clone = nn.clone()

    nnvalue = nn(sample_data)
    nncvalue = nn_clone(sample_data)

with tf.Session(graph=graph) as session:
    session.run(tf.initialize_all_variables())
    _value,_cvalue, _nnvalue, _nncvalue = session.run([value, cvalue, nnvalue, nncvalue])

    print "#Layer: Cloning At Initialization: "
    expect_equal(_value, _cvalue)

    print "#NN: Cloning At Initialization:"
    expect_equal(_nnvalue, _nncvalue)

    # changing the weigths of a layer after initialization
    layer.weights = layer.weights * 2

    layer_clone = layer.clone()

    value2 = layer(sample_data)
    cvalue2 = layer_clone(sample_data)

    # changing a layer in the neural network after initialization
    nn.layers[0] = layer_nn

    nn_clone = nn.clone()

    nnvalue2 = nn(sample_data)
    nncvalue2 = nn_clone(sample_data)

    _value2, _cvalue2, _nnvalue2, _nncvalue2 = session.run([value2, cvalue2, nnvalue2, nncvalue2])

    print "#Layer: Cloning After Initialization: "
    expect_equal(_value2, _cvalue2)

    print "#NN: Cloning After Initialization:"
    expect_equal(_nnvalue2, _nncvalue2)