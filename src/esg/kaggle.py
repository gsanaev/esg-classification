import kagglehub
import os
import shutil


def _move_files(source_path: str, destination: str, replace: bool = False) -> None:
    """
    Moves files from the source path to the destination directory.
    Args:
        source_path (str): The path where the files are currently located.
        destination (str): The directory where the files will be moved.
        replace (bool): If False, existing files won't be overwritten. If True, files will be replaced.
    Returns:
        None
    """
    data_dir = os.path.join(os.getcwd(), destination)
    os.makedirs(data_dir, exist_ok=True)
    
    files = os.listdir(source_path)
    for file_name in files:
        full_file_name = os.path.join(source_path, file_name)
        destination_file = os.path.join(data_dir, file_name)
        
        if os.path.isfile(full_file_name):
            # Check if file already exists in destination
            if os.path.exists(destination_file) and not replace:
                print(f"File already exists, skipping: {file_name}")
                continue
            
            print(f"Moving file: {full_file_name} to {data_dir}")
            shutil.move(full_file_name, data_dir)
    
    print(f"Files moved to '{destination}' directory.")


def load_from_kaggle(dataset_link: str, destination: str = "data/raw", create_subfolder=False, replace: bool = False) -> list[str]:
    """
    Loads a dataset from Kaggle and moves it to the specified destination directory.
    Args:
        dataset_link (str): The Kaggle dataset link in the format 'username/dataset-name' 
        
        destination (str): The directory where the dataset will be saved. Defaults to the dataset name.
        
        create_subfolder (bool): If True, creates a subfolder with the dataset name in the destination directory.
        
        replace (bool): If False, existing files/directories won't be overwritten. If True, they will be replaced.
    Returns:
        List [str]: A list of file names that were moved to the destination directory.
    """
    # If the final CSV already exists and replace=False, skip download
    target_csv = os.path.join(os.getcwd(), destination, "esg_kaggle.csv")
    if os.path.exists(target_csv) and not replace:
        print(f"File already exists, skipping download (replace=False): {target_csv}")
        return [os.path.basename(target_csv)]

    # Determine final destination path
    if create_subfolder:
        final_destination = os.path.join(destination, dataset_link.split("/")[-1])
    else:
        final_destination = destination
    
    full_destination_path = os.path.join(os.getcwd(), final_destination)
    
    # If destination exists and replace is True, remove it first
    if os.path.exists(full_destination_path) and replace:
        print(f"Removing existing destination directory: {final_destination}")
        shutil.rmtree(full_destination_path)
    
    # Ensure destination directory exists
    os.makedirs(full_destination_path, exist_ok=True)
    
    # Download the dataset
    print(f"Downloading dataset from Kaggle: {dataset_link}")
    path = kagglehub.dataset_download(dataset_link, force_download=True)
    
    print(f"Loading dataset from {path} to {final_destination}")
    _move_files(path, final_destination, replace)

    # Rename the first CSV found to esg_kaggle.csv
    moved_files = os.listdir(full_destination_path)
    csv_candidates = [f for f in moved_files if f.lower().endswith(".csv")]

    if not csv_candidates:
        print("No CSV file found after download.")
        return moved_files

    src_csv = os.path.join(full_destination_path, csv_candidates[0])
    dst_csv = os.path.join(full_destination_path, "kaggle_esg.csv")

    if os.path.exists(dst_csv) and replace:
        os.remove(dst_csv)

    if not os.path.exists(dst_csv):
        os.rename(src_csv, dst_csv)
    # else: if replace=False and dst exists, we keep existing esg_kaggle.csv

    return os.listdir(full_destination_path)


if __name__ == "__main__":
    # Example call: pass the Kaggle dataset identifier (not the full URL)
    files = load_from_kaggle("shriyashjagtap/esg-and-financial-performance-dataset")
    print("Destination files:", files)
