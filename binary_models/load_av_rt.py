from micom import load_pickle
import pathlib
import pandas as pd
import binary_models.helpers as helpers

_suffix = 'av_rt'
m_names = ['Azotobacter', 'Rhodosporidium']
f_names = ['azo_vine.xml', 'rhodo_toru.xml']

path = pathlib.Path(__file__).parent

model_folder = path.joinpath(f'models_{_suffix}').__str__()
_db_path = path.joinpath(f'db_{_suffix}').__str__()
_mani_path = path.joinpath('Manifest_Files', f'man_{_suffix}.csv').__str__()


def load_community_model(prep_files=False):
    mani_exists = pathlib.Path(model_folder).joinpath('manifest.csv').exists()
    if prep_files or not mani_exists:
        manifest = helpers.prepare_files(
            m_names, f_names, _mani_path, _db_path, model_folder
        )
    else:
        manifest = pd.read_csv(
            pathlib.Path(model_folder).joinpath('manifest.csv')
        )
    f_path = pathlib.Path(model_folder).joinpath('One.pickle').__str__()
    community = load_pickle(f_path)
    return community, manifest
