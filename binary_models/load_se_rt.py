from binary_models.taxonomy_info import tax_dict
import cobra

from micom.workflows import build, build_database
from micom import load_pickle
from concerto.helpers.load_model_from_git import load_model_from_git
import pathlib
import pandas as pd

path = pathlib.Path(__file__).parent

model_folder = path.joinpath('models_se_rt').__str__()
_db_path = path.joinpath('db_se_rt').__str__()
print(pathlib.Path(model_folder).__str__())

models = ['Rhodosporidium', 'Synechococcus']
m_names = ['Rhodo_Toru.xml', 'syn_elong.xml']


def dowload_models():
    sbml_models = []
    for model, name in zip(models, m_names):
        m = load_model_from_git(model)
        sbml_models.append(m)
        cobra.io.write_sbml_model(m, name)
    return sbml_models


def create_tax():
    sbml_models = dowload_models()
    for i in sbml_models:
        model_info = {
            'reactions': len(i.reactions),
            'metabolites': len(i.metabolites)
        }
        tax_dict[i.id].update(model_info)
        print(i.id, len(i.reactions), len(i.metabolites))

    tax = pd.DataFrame(tax_dict).T.reset_index(names='id')
    return tax


def create_database():
    manifest_file_path = path.joinpath(
        '..', 'Manifest_Files', 'man_se_rt.csv'
    ).__str__()
    db = pd.read_csv(manifest_file_path)
    db['file'] = m_names
    build_database(db, _db_path)


def prepare_files():
    create_database()
    tax = create_tax()
    manifest = build(
        tax,
        out_folder=model_folder,
        model_db=_db_path,
        cutoff=0.0001,
        threads=1,
        solver='gurobi'
    )
    return manifest


def load_community_model(prep_files=False):
    if prep_files:
        manifest = prepare_files()
    else:
        manifest = pd.read_csv(
            pathlib.Path(model_folder).joinpath('manifest.csv')
        )
    f_path = pathlib.Path(model_folder).joinpath('One.pickle').__str__()
    community = load_pickle(f_path)
    return community, manifest
