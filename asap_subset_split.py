
from glob import glob
from tqdm import tqdm
import pandas as pd
import os
import numpy as np


def asap_subset_split(maestro_dir:str, asap_dir:str, asap_subset:str):

    # wav_paths = glob(asap_dir + "/**/*.wav", recursive=True)

    csv_path = maestro_dir + '/maestro-v2.0.0.csv'
    asap_meta_path = "dataset/asap-dataset/metadata.csv"
    df = pd.read_csv(csv_path, header=0)
    df_asap = pd.read_csv(asap_meta_path, header=0)


    df = df[df["split"] == asap_subset]

    maestro_subset_midi_paths = set([x for x in df["midi_filename"]])

    wav_paths_to_tran = []

    midis = df_asap["maestro_midi_performance"].tolist()
    audios = df_asap["audio_performance"].tolist()
    for i in range(len(midis)):
        p_midi_path = midis[i]
        audio_path = audios[i]
        if p_midi_path is np.nan or audio_path is np.nan:
            continue
        assert p_midi_path.startswith(r"{maestro}/")
        p_midi_path = p_midi_path[len(r"{maestro}/"):]
        
        if p_midi_path in maestro_subset_midi_paths:
            abs_wav_path = os.path.join(asap_dir, audio_path)
            if os.path.exists(abs_wav_path):
                wav_paths_to_tran.append(audio_path)

    wav_paths_to_tran.sort()
    with open(asap_dir + "/subset_%s.txt"%asap_subset, "w", encoding="utf-8") as f:
        f.write("\n".join(wav_paths_to_tran) + "\n")
    

###################


maestro_dir = "/n/work1/wei/datasets/maestro-v2.0.0"
asap_dir = "dataset/asap-dataset"
    
asap_subset_split(maestro_dir=maestro_dir, asap_dir=asap_dir, asap_subset="train")
asap_subset_split(maestro_dir=maestro_dir, asap_dir=asap_dir, asap_subset="test")
asap_subset_split(maestro_dir=maestro_dir, asap_dir=asap_dir, asap_subset="validation")
    


