from pathlib import Path

# `cwd`: current directory is straightforward
cwd = Path.cwd()
print(cwd)

# `mod_path`: According to the accepted answer and combine with future power
# if we are in the `helper_script.py`
mod_path = Path(__file__).parent
print(mod_path)
# OR if we are `import helper_script`
#mod_path = Path(helper_script.__file__).parent
print(mod_path)
# `src_path`: with the future power, it's just so straightforward
#relative_path_1 = 'same/parent/with/helper/script/'
relative_path_1 = '../screeners/'
relative_path_2 = '../positions/'
src_path_1 = (mod_path / relative_path_1).resolve()
print(src_path_1)
src_path_2 = (mod_path / relative_path_2).resolve()
print(src_path_2)