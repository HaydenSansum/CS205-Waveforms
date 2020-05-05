from file_transformer import file_transformer
from song_transform_functions import song_converter, song_digitizer

ft = file_transformer('../../songs')
ft.set_input_path('mp3')
ft.set_output_path('test')

ft.apply_operation(song_converter, ft._input_folders, 'mp3', 'wav')

ft.set_input_path('test')
ft.set_output_path('test_clean')

ft.apply_operation(song_digitizer, ft._input_folders, 'wav', 'wav')
