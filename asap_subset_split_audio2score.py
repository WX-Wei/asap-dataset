import os
import shutil

def get_subset_dirs(subset_list_path):
    with open(subset_list_path) as f:
        lines = f.readlines()
        subset_dirs = [line.strip() for line in lines]
        
    return set(subset_dirs)

if __name__ == "__main__":
    dataset_dir = "dataset/asap-dataset"
        
    idx_list = []
    audio_paths = []
    annotation_paths = []
    audio_list_path = dataset_dir + '/audio_list.txt'
    lines = open(audio_list_path).readlines()
    for line in lines:
        idx, path = line.strip().split(" ")
        idx_list.append(idx)
        audio_paths.append(path)
    
    subsets = ["train", "validation", "test", "all"]
    

    for subset in subsets:
        subset_audio_list = []
        subset_idx_list = []
        subset_dirs = get_subset_dirs(dataset_dir + '/ASAP_midi2score_' + subset + '.txt')
        for idx, path in zip(idx_list, audio_paths):
            if subset != "all" and os.path.dirname(path) not in subset_dirs:
                continue
            subset_audio_list.append(path)
            subset_idx_list.append(idx)
        with open(dataset_dir + '/subset_' + subset + '.tsv', 'w') as f:
            for idx, path in zip(subset_idx_list, subset_audio_list):
                f.write(f"{idx}\t{path}\n")
            