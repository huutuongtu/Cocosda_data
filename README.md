# Cocosda_data

Download file .mp4 from youtube and convert file .mp4 to file .wav, we run code: </br>
python3 crawl.py --url_playlist=url_playlist_youtube --save_dir=directory_save_file

VAD file wav run code: </br>
python silero-VAD.py --folder_file_wav=folder_contain_file_wav --savedir=directory_save_file

After VAD, we run like this to cosine pair wav: </br>
python3 cosine_pair.py --wav_dir=dir_to_foler_wav --file_csv=file_csv_save_min_cosine_and_path_of_wav</br>
So, after cosine_pair.py, we have csv file save all min cosine and path of wav after VAD </br>
We listen random some wavs and choose thresh hold min cosine to remove all wav file smaller than thresh hold </br>
Use: python3 --remove.py --file_csv=file_csv_save_min_cosine_and_path_of_wav --threshold=thresh_hold_we_choose
