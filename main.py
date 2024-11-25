import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt
import numpy as np


# Function to select and display image
def select_image():
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Load and display the selected image
        img = cv2.imread(file_path)

        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the image in the GUI
        img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        input_label.config(image=img_tk)
        input_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Process the image and display results
        process_and_display_results(img)


# Function to process image and display results
def process_and_display_results(img):
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

    # Display processed images using Matplotlib
    display_processed_images(img, img_gray, thresh)

    # Perform contour detection
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # Draw contours on the original image
    image_contours = cv2.drawContours(image=img.copy(), contours=contours, contourIdx=-1, color=(255, 0, 0),
                                      thickness=2, lineType=cv2.LINE_AA)

    # Convert image with contours to RGB for display
    image_contours_rgb = cv2.cvtColor(image_contours, cv2.COLOR_BGR2RGB)

    # Display the image with contours using Matplotlib
    display_contours(image_contours_rgb)


# Function to display processed images using Matplotlib
def display_processed_images(original, gray, thresh):
    plt.figure(figsize=(14, 6))

    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(original)
    plt.title('Original Image')
    plt.axis('off')

    # Grayscale image
    plt.subplot(1, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')

    # Thresholded image
    plt.subplot(1, 3, 3)
    plt.imshow(thresh, cmap='gray')
    plt.title('Thresholded Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


# Function to display image with contours using Matplotlib
def display_contours(image_contours):
    plt.figure(figsize=(8, 6))
    plt.imshow(image_contours)
    plt.title('Contours')
    plt.axis('off')
    plt.show()


# Create the main application window
root = tk.Tk()
root.title("Counter Line Detection")

# Create a button to select an image
btn_select = tk.Button(root, text="Select Image", command=select_image)
btn_select.pack()

# Create labels to display the input and output images
input_label = tk.Label(root)
input_label.pack()

# Run the main event loop
root.mainloop()
