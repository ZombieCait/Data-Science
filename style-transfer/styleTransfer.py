from IPython.display import Image, display
Image('image/mill.jpg')
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import PIL.Image
import vgg16

vgg16.data_dir = 'vgg16/'
#vgg16.maybe_download()

def load_image(filename, max_size=None):
    image=PIL.Image.open(filename)

    if max_size is not None:
        factor = max_size / np.max(image.size)
        size=np.array(image.size) * factor
        size=size.astype(int)
        image = image.resize(size, PIL.Image.LANCZOS)

    return np.float32(image)

def save_image(image, filename):
    image = np.clip(image, 0.0, 255.0)
    image= image.astype(np.uint8)

    with open(filename, 'wb') as file:
        PIL.Image.fromarray(image).save(file, 'jpeg')


def plot_image_big(image):
    image = np.clip(image, 0.0, 255.0)
    image = image.astype(np.uint8)
    display(PIL.Image.fromarray(image))


def plot_images(content_image, style_image, mixed_image):
    fig, axes = plot.subplots(1, 3, figsize=(10, 10))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    smooth = True
    #interpolation style
    if smooth:
        interpolation = 'sinc'
    else:
        interpolation = 'nearest'

        # Note that the pixel-values are normalized to
        # the [0.0, 1.0] range by dividing with 255.
        ax = axes.flat[0]
        ax.imshow(content_image / 255.0, interpolation=interpolation)
        ax.set_xlabel("Content")

        # Plot the mixed-image.
        ax = axes.flat[1]
        ax.imshow(mixed_image / 255.0, interpolation=interpolation)
        ax.set_xlabel("Mixed")

        # Plot the style-image
        ax = axes.flat[2]
        ax.imshow(style_image / 255.0, interpolation=interpolation)
        ax.set_xlabel("Style")

        # Remove ticks from all the plots.
        for ax in axes.flat:
            ax.set_xticks([])
            ax.set_yticks([])

        plot.show()

#Loss Functions

def mean_squared_error(a, b): #content image and feather map(result oflayer that we chosee)
    return tf.reduce_mean(tf.square(a-b))#need positiv - square

#layer_ids - indexes for layer
def create_content_loss(session, model, content_image, layer_ids):

    #key - image, value- content image
    feed_dict = model.create_feed_dict(image=content_image)

    layers = model.get_layer_tensors(layer_ids)
    values=session.run(layers, feed_dict=feed_dict)
    with model.graph.as_default():
        layer_losses =[]
        for value, layer  in zip(values, layers):
            value_const =  tf.constant(value)
            loss=mean_squared_error(layer, value_const)
            layer_losses.append(loss)
        total_loss=tf.reduce_mean(layer_losses)
    return total_loss


#gram matrix - matrix products of the additional matrix and transpote matrix
def gram_matrix(tensor):
    shape =tensor.get_shape()
    #outputs of each layers
    num_channel = int(shape[3])
    matrix = tf.reshape(tensor, shape=[-1, num_channel])
    gram=tf.matmul(tf.transpose(matrix), matrix)
    return gram

#style loss
#calculate squared error for gram matrix
def create_style_loss(session, model, style_image, layer_ids):
    feed_dict = model.create_feed_dict(image=style_image)

    layers = model.get_layer_tensors(layer_ids)

    with model.graph.as_default():
        gram_layers=[gram_matrix(layer) for layer in layers]
        values=session.run(gram_layers, feed_dict=feed_dict) #how featchers are correlate
        layer_losses=[]
        for value, gram_layer in zip(values, gram_layers):
            value_const=tf.constant(value)
            loss = mean_squared_error(gram_layer, value_const)
            layer_losses.append(loss)

        total_loss=tf.reduce_mean(layer_losses)
    return  total_loss
#total variation denoise loss
def create_denoise_loss(model):
    loss = tf.reduce_sum(tf.abs(model.input[:, 1:, :, :] - model.input[:, :-1, :, :])) + \
           tf.reduce_sum(tf.abs(model.input[:, :, 1:, :] - model.input[:, :, :-1, :]))

    return loss

#style_transfer
def style_transfer(content_image, style_image,
                   content_layer_ids, style_layer_ids,
                   weight_content=1.5, weight_style=10.0,
                   weight_denoise=0.3,
                   num_iterations=120, step_size=10.0):
    # Create an instance of the VGG16-model. This is done
    # in each call of this function, because we will add
    # operations to the graph so it can grow very large
    # and run out of RAM if we keep using the same instance.
    model = vgg16.VGG16()

    # Create a TensorFlow-session.
    session = tf.InteractiveSession(graph=model.graph)

    # Print the names of the content-layers.
    print("Content layers:")
    print(model.get_layer_names(content_layer_ids))
    print()

    # Print the names of the style-layers.
    print("Style layers:")
    print(model.get_layer_names(style_layer_ids))
    print()

    # Create the loss-function for the content-layers and -image.
    loss_content = create_content_loss(session=session,
                                       model=model,
                                       content_image=content_image,
                                       layer_ids=content_layer_ids)

    # Create the loss-function for the style-layers and -image.
    loss_style = create_style_loss(session=session,
                                   model=model,
                                   style_image=style_image,
                                   layer_ids=style_layer_ids)

    # Create the loss-function for the denoising of the mixed-image.
    loss_denoise = create_denoise_loss(model)

    # Create TensorFlow variables for adjusting the values of
    # the loss-functions. This is explained below.
    adj_content = tf.Variable(1e-10, name='adj_content')
    adj_style = tf.Variable(1e-10, name='adj_style')
    adj_denoise = tf.Variable(1e-10, name='adj_denoise')

    # Initialize the adjustment values for the loss-functions.
    session.run([adj_content.initializer,
                 adj_style.initializer,
                 adj_denoise.initializer])

    # Create TensorFlow operations for updating the adjustment values.
    # These are basically just the reciprocal values of the
    # loss-functions, with a small value 1e-10 added to avoid the
    # possibility of division by zero.
    update_adj_content = adj_content.assign(1.0 / (loss_content + 1e-10))
    update_adj_style = adj_style.assign(1.0 / (loss_style + 1e-10))
    update_adj_denoise = adj_denoise.assign(1.0 / (loss_denoise + 1e-10))

    # This is the weighted loss-function that we will minimize
    # below in order to generate the mixed-image.
    # Because we multiply the loss-values with their reciprocal
    # adjustment values, we can use relative weights for the
    # loss-functions that are easier to select, as they are
    # independent of the exact choice of style- and content-layers.
    loss_combined = weight_content * adj_content * loss_content + \
                    weight_style * adj_style * loss_style + \
                    weight_denoise * adj_denoise * loss_denoise

    # Use TensorFlow to get the mathematical function for the
    # gradient of the combined loss-function with regard to
    # the input image.
    gradient = tf.gradients(loss_combined, model.input)

    # List of tensors that we will run in each optimization iteration.
    run_list = [gradient, update_adj_content, update_adj_style, \
                update_adj_denoise]

    # The mixed-image is initialized with random noise.
    # It is the same size as the content-image.
    mixed_image = np.random.rand(*content_image.shape) + 128

    for i in range(num_iterations):
        # Create a feed-dict with the mixed-image.
        feed_dict = model.create_feed_dict(image=mixed_image)

        # Use TensorFlow to calculate the value of the
        # gradient, as well as updating the adjustment values.
        grad, adj_content_val, adj_style_val, adj_denoise_val \
            = session.run(run_list, feed_dict=feed_dict)

        # Reduce the dimensionality of the gradient.
        grad = np.squeeze(grad)

        # Scale the step-size according to the gradient-values.
        step_size_scaled = step_size / (np.std(grad) + 1e-8)

        # Update the image by following the gradient.
        mixed_image -= grad * step_size_scaled

        # Ensure the image has valid pixel-values between 0 and 255.
        mixed_image = np.clip(mixed_image, 0.0, 255.0)

        # Print a little progress-indicator.
        print(". ", end="")

        # Display status once every 10 iterations, and the last.
        if (i % 10 == 0) or (i == num_iterations - 1):
            print()
            print("Iteration:", i)

            # Print adjustment weights for loss-functions.
            msg = "Weight Adj. for Content: {0:.2e}, Style: {1:.2e}, Denoise: {2:.2e}"
            print(msg.format(adj_content_val, adj_style_val, adj_denoise_val))

            # Plot the content-, style- and mixed-images.
            plot_images(content_image=content_image,
                        style_image=style_image,
                        mixed_image=mixed_image)

    print()
    print("Final image:")
    plot_image_big(mixed_image)

    # Close the TensorFlow session to release its resources.
    session.close()

    # Return the mixed-image.
    return mixed_image

content_filename='image/willy_wonka_new.jpg'
content_image = load_image(content_filename, max_size=None)

style_filename='style/style5.jpg'
style_image=load_image(style_filename, max_size=300)

content_layer_ids = [4]
style_layer_ids = list(range(13))

img = style_transfer(content_image=content_image,
                     style_image=style_image,
                     content_layer_ids=content_layer_ids,
                     style_layer_ids=style_layer_ids,
                     weight_content=1.5,
                     weight_style=10.0,
                     weight_denoise=0.3,
                     num_iterations=60,
                     step_size=10.0)

