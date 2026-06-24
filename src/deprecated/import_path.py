from pathlib import Path


# formatting path for input and output folders 
# `cwd`: current directory is straightforward
cwd = Path.cwd()
mod_path = Path(__file__).parent


rel_path_db = '../../db/'
rel_path_gen = '../../gen/'
rel_path_gen_lst = '../../gen/listing'
rel_path_usr = '../../usr/'
rel_path_usr_lst = '../../usr/listing'
src_path_db = (mod_path / rel_path_db).resolve()
src_path_gen = (mod_path / rel_path_gen).resolve()
src_path_usr = (mod_path / rel_path_usr).resolve()
src_path_lst = (mod_path / rel_path_lst).resolve()