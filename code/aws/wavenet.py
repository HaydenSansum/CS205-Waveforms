import numpy as np
import keras

def create_wavenet(n_layers, n_song_channels, filter_sizes, num_stacks, bias=True, residual=False):
    '''
    Build and return an untrained wavenet model using Keras layers
    inputs:
        n_window - int - must be in the series 2^n, should match the input size of the data
        n_song_channels - int - number of output channels for the song, usually 256
        filter_sizes - list - must be length 4, consists of: [n_filter_atrous, n_filter_skip, n_relu1, n_relu2]
    '''
    assert len(filter_sizes) == 4, "Error: must have 4 different filter sizes"

    n_window = (2 ** (n_layers)) * num_stacks

    # Get the three different specifications for filter size
    n_filter_atrous = filter_sizes[0]
    n_filter_skip = filter_sizes[1]
    n_filter_out = n_song_channels
    n_relu1 = filter_sizes[2]
    n_relu2 = filter_sizes[3]
    

    def add_wavenet_layer(input_layer, dilation, skips, n_filter_atrous=n_filter_atrous, n_filter_skip=n_filter_skip, skip=False, residual=False, bias=True):
        '''
        Building block for creating WAVENET - uses a Gated unit which consists of a causal dilated tanh and sigmoid
        multiplied together. This is then collected together so it can be passed out as a skip connect. Also
        each block can have a residual layer to speed training.
        inputs:
            input layer - keras.Layer - the preceeding layer of the model 
            n_filter_atrous - int - number of filters to use for the two interal convolutional layers
            n_filter_skip - int - number of filters for the resulting output skip connection
            dilation - int - the dilation vlaue (number of nodes to skip) generally increments by 2^n each layer
            skips - list - list of the current skip connections
            skip - bool - Whether to include the output of the current layer in the skip outputs
            residual - bool - whether to allow for a residual pass through of the input in the current layer
        '''    
        conv_sig = keras.layers.Conv1D(filters=n_filter_atrous, kernel_size=2, strides=1, padding="causal",
                                            dilation_rate=dilation, activation='sigmoid', use_bias=bias)(input_layer)

        conv_tanh = keras.layers.Conv1D(filters=n_filter_atrous, kernel_size=2, strides=1, padding="causal",
                                            dilation_rate=dilation, activation='tanh', use_bias=bias)(input_layer)

        multiply_layer = keras.layers.Multiply()([conv_sig, conv_tanh])
        
        collect_layer = keras.layers.Conv1D(filters=n_filter_skip, kernel_size=1, padding='same', activation=None)(multiply_layer)

        if skip == True:
            skips.append(collect_layer)

        if residual == True:
            resulting_layer = keras.layers.Add()([input_layer, collect_layer])
        else:
            resulting_layer = collect_layer

        return(resulting_layer, skips)


    # ======= BUILD THE MODEL ========
    model_input = keras.layers.Input(shape=(n_window, 1))
    skips = []

    # Add a single WAVENET layer
    out_layer = model_input
    #out_layer, skips = add_wavenet_layer(model_input, dilation = 1, skips=skips, skip=False, residual=False, bias=bias)

    #Add layers (based on the size of the window)
    for j in range(num_stacks):
        for i in range(n_layers):
            dil_val = 2**(i)
            out_layer, skips = add_wavenet_layer(out_layer, dilation=dil_val, skips=skips, skip=True, bias=bias, residual=residual)

    # Combine skip layers and final output layer
    sum_skips = keras.layers.Add()(skips)
    #combined_output = keras.layers.Add()([out_layer, sum_skips])

    # Final two relu layers
    relu1 = keras.layers.Conv1D(filters=n_relu1, kernel_size=1, padding='same', activation='relu')(sum_skips)
    relu2 = keras.layers.Conv1D(filters=n_relu2, kernel_size=1, padding='same', activation='relu')(relu1)

    # Softmax prediction layer
    final_output = keras.layers.Conv1D(filters=n_filter_out, kernel_size=1, padding='same', activation='softmax')(relu2)
    
    wavenet_model = keras.Model(model_input, final_output) 
    
    return wavenet_model