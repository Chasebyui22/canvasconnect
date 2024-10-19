from PIL import Image
import os

# Function to resize images
def resize_image(input_path, output_dir, sizes):
    # Open the original image
    with Image.open(input_path) as img:
        for size in sizes:
            # Resize image
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            # Construct the output path
            base_name = os.path.basename(input_path)
            name, ext = os.path.splitext(base_name)
            resized_img_path = os.path.join(output_dir, f"{name}_{size[0]}x{size[1]}{ext}")
            # Save the resized image
            resized_img.save(resized_img_path)
            print(f"Saved: {resized_img_path}")

# Main function
def main():
    input_image_path = r"C:\CollegeFoldersAndFiles\Clubs and Projects\CanvasConnect\canvasconnect\CCBrowserExtension\Icon_Images\CanvasConnect.png"  # Use raw string for Windows paths
    output_directory = r"C:\CollegeFoldersAndFiles\Clubs and Projects\CanvasConnect\canvasconnect\CCBrowserExtension"  # Use raw string for Windows paths
    sizes = [(16, 16), (48, 48), (128, 128)]  # List of sizes

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Resize and save images
    resize_image(input_image_path, output_directory, sizes)

if __name__ == "__main__":
    main()
