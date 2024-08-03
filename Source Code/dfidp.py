real_folder_path=r"/Users/rupesh/Downloads/Celeb df/Real/"
fake_folder_path=r"/Users/rupesh/Downloads/Celeb df/Fake"
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision
import seaborn as sns
# Define constants
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 25
EPOCHS = 10
def load_images(folder_path):
  images = []
  labels = []
  for filename in os.listdir(folder_path):
    if filename.startswith("real"):
      label = 0  # Real images
    elif filename.startswith("fake"):
      label = 1  # Fake images
    else:
      continue  # Skip files that are not real or fake images
    img = load_img(os.path.join(folder_path, filename), target_size=IMAGE_SIZE)
    img_array = img_to_array(img) / 255.0
    images.append(img_array)
    labels.append(label)
  return np.array(images), np.array(labels)
  
X_real, y_real = load_images(real_folder_path)
X_fake, y_fake = load_images(fake_folder_path)

X_real, y_real = load_images(real_folder_path)
X_fake, y_fake = load_images(fake_folder_path)
X = np.concatenate([X_real, X_fake], axis=0)
y = np.concatenate([y_real, y_fake], axis=0)
# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state
# Create CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation=’relu’, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1],
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation=’relu’),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation=’relu’),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation=’relu’),
    Dropout(0.5),
    Dense(1, activation=’sigmoid’)
])
# Compile model
model.compile(optimizer=’adam’, loss=’binary_crossentropy’, metrics=[’accuracy’])
# Train model
model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(X_
# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss}, Test accuracy: {accuracy}")
# Make predictions
predictions = model.predict(X_test)
#load and process image
image_path = r"/Users/rupesh/Downloads/Celeb df/train/fake_0.jpg"
img = load_img(image_path, target_size=IMAGE_SIZE)
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
# Use the trained model to make predictions
prediction = model.predict(img_array)
# Make predictions on the test set
y_pred = (predictions > 0.5).astype(int)
# Calculate confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)
# Calculate accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
# Calculate recall (sensitivity) score
recall = recall_score(y_test, y_pred)
print(f"Recall (Sensitivity): {recall:.4f}")
# Calculate precision score
precision = precision_score(y_test, y_pred)
print(f"Precision: {precision:.4f}")
# Plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()
# Interpret the prediction
if prediction[0][0] < 0.5:
  print("The image is classified as real.")
else:
  print("The image is classified as fake.")
