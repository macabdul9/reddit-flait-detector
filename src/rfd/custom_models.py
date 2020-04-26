from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, GRU, Conv1D
from keras.layers import Bidirectional, GlobalMaxPool1D, GlobalMaxPooling1D, GlobalAveragePooling1D, MaxPooling1D
from keras.layers import Input, Embedding, Dense, Conv2D, MaxPool2D, concatenate
from keras.layers import Reshape, Flatten, Concatenate, Dropout, SpatialDropout1D
from keras.optimizers import Adam
from keras.models import Model, Sequential
from keras.engine.topology import Layer
from keras import initializers, regularizers, constraints, optimizers, layers
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.initializers import *
from keras.optimizers import *
import keras.backend as K
from keras.callbacks import *

def BiLSTM(vocabulary_size, max_len, n_classes=11, trainable=True, embedding_matrix=None):
    """
        Function to create BiLSTM Network
        Parameters:
            vocabulary_size: size of the vocabulary
            max_len: max len of the sequence
            embedding_matrix: pretrained embedding matrix if trainable is false  
        Returns: BiLSTM compiled model (ready to be trained)
    """
    model = Sequential()

    # if trainable we will have to train the emedding otherwise we will use pretrained embeddings ie: Glove, Word2Vec
    if trainable:
        model.add(Embedding(vocabulary_size, 100, input_length=max_len, name="embedding_1"))
    else:
        model.add(Embedding(vocabulary_size, 100, input_length=max_len, weights=[embedding_matrix], trainable=False, name="embedding_1"))
    model.add(Dropout(0.2, name="dropout_1"))
    model.add(Conv1D(64, 5, activation='relu', name="conv1d_1")) # conv layer reduces the training time
    model.add(MaxPooling1D(pool_size=4, name="maxpool_1"))
    model.add(Bidirectional(LSTM(100, dropout=0.2, recurrent_dropout=0.2, name="LSTM_module_1"), name="BiLSTM_module"))
    model.add(Dense(n_classes, activation='softmax', name="output"))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def CNN(vocabulary_size, max_len, n_classes=11,  trainable=True, embedding_matrix=None, filter_sizes = [1,2,3,5],  num_filters = 64
):
    """
        Function to create CNN network for text classification (using pretrained embeddings)
        Params:
            vocabulary_size: size of the vocabulary
            max_len: max len of the sequence
            embedding_matrix: pretrained embedding matrix if trainable is false
            filter_size: kernel size 
            num_filters: no. of kernel units
        Returns: Compiled CNN model

    """
    
    inp = Input(shape=(max_len, ))

    # if trainable we will have to train the emedding otherwise we will use 
    # pretrained embeddings ie: Glove, Word2Vec.

    if trainable:
        x = Embedding(vocabulary_size, 100, trainable=trainable)(inp)
    else:
        x = Embedding(vocabulary_size, 100, weights=[embedding_matrix], trainable=trainable)(inp)
    #    x = SpatialDropout1D(0.4)(x)
    x = Reshape((max_len, 100, 1))(x)
    
    conv_0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], 100),
                                 kernel_initializer='he_normal', activation='tanh')(x)
    conv_1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], 100),
                                 kernel_initializer='he_normal', activation='tanh')(x)
    conv_2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], 100), 
                                 kernel_initializer='he_normal', activation='tanh')(x)
    conv_3 = Conv2D(num_filters, kernel_size=(filter_sizes[3], 100),
                                 kernel_initializer='he_normal', activation='tanh')(x)
    
    maxpool_0 = MaxPool2D(pool_size=(max_len - filter_sizes[0] + 1, 1))(conv_0)
    maxpool_1 = MaxPool2D(pool_size=(max_len - filter_sizes[1] + 1, 1))(conv_1)
    maxpool_2 = MaxPool2D(pool_size=(max_len - filter_sizes[2] + 1, 1))(conv_2)
    maxpool_3 = MaxPool2D(pool_size=(max_len - filter_sizes[3] + 1, 1))(conv_3)
        
    z = Concatenate(axis=1)([maxpool_0, maxpool_1, maxpool_2, maxpool_3])   
    z = Flatten()(z)
    z = Dropout(0.1)(z)
        
    outp = Dense(11, activation="softmax")(z)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


def dot_product(x, kernel):
    """
    Wrapper for dot product operation, in order to be compatible with both
    Theano and Tensorflow
    Args:
        x (): input
        kernel (): weights
    Returns:
    """
    if K.backend() == 'tensorflow':
        return K.squeeze(K.dot(x, K.expand_dims(kernel)), axis=-1)
    else:
        return K.dot(x, kernel)
    

class AttentionWithContext(Layer):
    """
    Attention operation, with a context/query vector, for temporal data.
    Supports Masking.
    Follows the work of Yang et al. [https://www.cs.cmu.edu/~diyiy/docs/naacl16.pdf]
    "Hierarchical Attention Networks for Document Classification"
    by using a context vector to assist the attention
    # Input shape
        3D tensor with shape: `(samples, steps, features)`.
    # Output shape
        2D tensor with shape: `(samples, features)`.
    How to use:
    Just put it on top of an RNN Layer (GRU/LSTM/SimpleRNN) with return_sequences=True.
    The dimensions are inferred based on the output shape of the RNN.
    Note: The layer has been tested with Keras 2.0.6
    Example:
        model.add(LSTM(64, return_sequences=True))
        model.add(AttentionWithContext())
        # next add a Dense layer (for classification/regression) or whatever...
    """

    def __init__(self,
                 W_regularizer=None, u_regularizer=None, b_regularizer=None,
                 W_constraint=None, u_constraint=None, b_constraint=None,
                 bias=True, **kwargs):

        self.supports_masking = True
        self.init = initializers.get('glorot_uniform')

        self.W_regularizer = regularizers.get(W_regularizer)
        self.u_regularizer = regularizers.get(u_regularizer)
        self.b_regularizer = regularizers.get(b_regularizer)

        self.W_constraint = constraints.get(W_constraint)
        self.u_constraint = constraints.get(u_constraint)
        self.b_constraint = constraints.get(b_constraint)

        self.bias = bias
        super(AttentionWithContext, self).__init__(**kwargs)

    def build(self, input_shape):
        assert len(input_shape) == 3

        self.W = self.add_weight(shape=(input_shape[-1], input_shape[-1],),
                                 initializer=self.init,
                                 name='{}_W'.format(self.name),
                                 regularizer=self.W_regularizer,
                                 constraint=self.W_constraint)
        if self.bias:
            self.b = self.add_weight(shape=(input_shape[-1],),
                                     initializer='zero',
                                     name='{}_b'.format(self.name),
                                     regularizer=self.b_regularizer,
                                     constraint=self.b_constraint)

        self.u = self.add_weight(shape=(input_shape[-1],),
                                 initializer=self.init,
                                 name='{}_u'.format(self.name),
                                 regularizer=self.u_regularizer,
                                 constraint=self.u_constraint)

        super(AttentionWithContext, self).build(input_shape)

    def compute_mask(self, input, input_mask=None):
        # do not pass the mask to the next layers
        return None

    def call(self, x, mask=None):
        uit = dot_product(x, self.W)

        if self.bias:
            uit += self.b

        uit = K.tanh(uit)
        ait = dot_product(uit, self.u)

        a = K.exp(ait)

        # apply mask after the exp. will be re-normalized next
        if mask is not None:
            # Cast the mask to floatX to avoid float64 upcasting in theano
            a *= K.cast(mask, K.floatx())

        # in some cases especially in the early stages of training the sum may be almost zero
        # and this results in NaN's. A workaround is to add a very small positive number ε to the sum.
        # a /= K.cast(K.sum(a, axis=1, keepdims=True), K.floatx())
        a /= K.cast(K.sum(a, axis=1, keepdims=True) + K.epsilon(), K.floatx())

        a = K.expand_dims(a)
        weighted_input = x * a
        return K.sum(weighted_input, axis=1)

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[-1]


def BiLSTM_Attn(vocabulary_size, max_len, embedding_matrix=None, n_classes=11, trainable=True ):
    inp = Input(shape=(max_len,))

    if trainable:
        x = Embedding(vocabulary_size, 100)(inp)
    else:
        x = Embedding(vocabulary_size, 100, weights=[embedding_matrix], trainable=trainable)(inp)
    x = Dropout(0.2)(x)
    x = Conv1D(64, 5, activation='relu')(x)
    x = MaxPooling1D(pool_size=4)(x)
    x = Bidirectional(LSTM(128, return_sequences=True))(x)
    x = Bidirectional(LSTM(64, return_sequences=True))(x)
    x = AttentionWithContext()(x)
    x = Dense(64, activation="relu")(x)
    x = Dense(11, activation="softmax")(x)
    model = Model(inputs=inp, outputs=x)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
