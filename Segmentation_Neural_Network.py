# activate tensorflow
from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)

# load pima indians dataset
train_dataset = numpy.loadtxt("combined_csv_6.csv", delimiter=",")
# split into input (X) and output (Y) variables
train_X = train_dataset[:,0:23]
train_Y = train_dataset[:,23]

test_dataset = numpy.loadtxt("test_csv_6.csv", delimiter=",")
test_X = test_dataset[:,0:23]
test_Y = test_dataset[:,23]

# create model
model = Sequential()
model.add(Dense(36, input_dim=23, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# Fit the model
model.fit(train_X, train_Y, epochs=100, batch_size=10)

# evaluate the model
scores = model.evaluate(test_X, test_Y, verbose=1)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))