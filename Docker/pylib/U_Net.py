from tensorflow import keras


def conv_block(input, num_filters):
    x = keras.layers.Conv2D(num_filters, 3, padding="same")(input)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Activation("relu")(x)

    x = keras.layers.Conv2D(num_filters, 3, padding="same")(x)
    x = keras.layers.BatchNormalization()(x)
    x = keras.layers.Activation("relu")(x)

    return x


def encoder_block(input, num_filters):
    x = conv_block(input, num_filters)
    p = keras.layers.MaxPool2D((2, 2))(x)
    return x, p


def decoder_block(input, skip_features, num_filters):
    x = keras.layers.Conv2DTranspose(
        num_filters, (2, 2), strides=2, padding="same")(input)
    x = keras.layers.Concatenate()([x, skip_features])
    x = conv_block(x, num_filters)
    return x


def build_unet(input_shape):
    inputs = keras.layers.Input(input_shape)
    f = [16, 32, 64, 128, 256]
    # f = [64, 128, 256, 512, 1024]

    s1, p1 = encoder_block(inputs, f[0])
    s2, p2 = encoder_block(p1, f[1])
    s3, p3 = encoder_block(p2, f[2])
    s4, p4 = encoder_block(p3, f[3])

    b1 = conv_block(p4, f[4])

    d1 = decoder_block(b1, s4, f[3])
    d2 = decoder_block(d1, s3, f[2])
    d3 = decoder_block(d2, s2, f[1])
    d4 = decoder_block(d3, s1, f[0])

    outputs = keras.layers.Conv2D(
        1, 1, padding="same", activation="sigmoid")(d4)

    model = keras.models.Model(inputs, outputs, name="U-Net")
    return model
