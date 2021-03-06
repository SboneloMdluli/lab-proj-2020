import sys
from matplotlib import pyplot
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

training_dir = '/content/drive/My Drive/spectrograms/train_data'

validation_dir = '/content/drive/My Drive/spectrograms/validation'

testing_dir = '/content/drive/My Drive/spectrograms/test_data'

num_epochs = 10
datagen = ImageDataGenerator ( 1 / 255 )

batch_size = 10

train_data = datagen.flow_from_directory ( training_dir, target_size=(256, 256), batch_size=10, class_mode='binary' )
val_data = datagen.flow_from_directory ( validation_dir, target_size=(256, 256), batch_size=10, class_mode='binary' )
test_data = datagen.flow_from_directory ( testing_dir, target_size=(256, 256), batch_size=10, class_mode='binary' )


# define cnn model
def define_model() :
    # load model
    model = VGG16 ( include_top=False, input_shape=(224, 224, 3) )
    # mark loaded layers as not trainable
    for layer in model.layers :
        layer.trainable = False
    # add new classifier layers
    flat1 = Flatten ( ) ( model.layers[-1].output )
    class1 = Dense ( 128, activation='relu', kernel_initializer='he_uniform' ) ( flat1 )
    output = Dense ( 1, activation='sigmoid' ) ( class1 )
    # define new model
    model = Model ( inputs=model.inputs, outputs=output )
    # compile model
    opt = SGD ( lr=0.001, momentum=0.9 )
    model.compile ( optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'] )
    return model


# define model
model = define_model ( )
# create data generator
datagen = ImageDataGenerator ( featurewise_center=True )
# specify imagenet mean values for centering
datagen.mean = [123.68, 116.779, 103.939]
# prepare iterator
train_it = datagen.flow_from_directory ( training_dir,
                                         class_mode='binary', batch_size=64, target_size=(224, 224) )
test_it = datagen.flow_from_directory ( testing_dir,
                                        class_mode='binary', batch_size=64, target_size=(224, 224) )
# fit model
history = model.fit_generator ( train_it, steps_per_epoch=len ( train_it ),
                                validation_data=test_it, validation_steps=len ( test_it ), epochs=10, verbose=1 )

# save model
model.save ( 'AMTclassification.h5' )
# evaluate model
_, acc = model.evaluate_generator ( test_it, steps=len ( test_it ), verbose=0 )
print ( '> %.3f' % (acc * 100.0) )


# Analytics and Perfromance matrix

def summarize_diagnostics(history) :
    # plot loss
    pyplot.subplot ( 211 )
    pyplot.title ( 'Cross Entropy Loss' )
    pyplot.plot ( history.history['loss'], color='blue', label='train' )
    pyplot.plot ( history.history['val_loss'], color='orange', label='test' )
    # plot accuracy
    pyplot.subplot ( 212 )
    pyplot.title ( 'Classification Accuracy' )
    pyplot.plot ( history.history['accuracy'], color='blue', label='train' )
    pyplot.plot ( history.history['val_accuracy'], color='orange', label='test' )
    # save plot to file
    filename = sys.argv[0].split ( '/' )[-1]
    pyplot.savefig ( filename + '_plot.png' )
    pyplot.close ( )


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range ( len ( acc ) )

plt.plot ( epochs, acc, 'bo', label='Training acc' )
plt.plot ( epochs, val_acc, 'b', label='Validation acc' )
plt.title ( 'Training and validation accuracy' )
plt.legend ( )

plt.figure ( )

plt.plot ( epochs, loss, 'bo', label='Training loss' )
plt.plot ( epochs, val_loss, 'b', label='Validation loss' )
plt.title ( 'Training and validation loss' )
plt.legend ( )