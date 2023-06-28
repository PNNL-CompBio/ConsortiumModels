import cobra
import pandas as pd
from micom.workflows import build, build_database
from concerto.helpers.load_model_from_git import load_model_from_git
from binary_models.taxonomy_info import tax_dict


def create_database(f_names, manifest_path, db_path):
    db = pd.read_csv(manifest_path)
    db['file'] = f_names
    build_database(db, db_path)


def download_model(model, name):
    m = load_model_from_git(model)
    cobra.io.write_sbml_model(m, name)
    return m


def create_tax(m_names, f_names):
    taxomony_copy_dict = dict()

    for i in m_names:
        taxomony_copy_dict[i] = tax_dict[i]

    for m, f_name in zip(m_names, f_names):
        model = download_model(model=m, name=f_name)
        model_info = {
            'reactions': len(model.reactions),
            'metabolites': len(model.metabolites),
            'file': f_name
        }
        taxomony_copy_dict[m].update(model_info)

    return pd.DataFrame(taxomony_copy_dict).T.reset_index(names='id')


def prepare_files(m_names, f_names, manifest_path, db_path, model_folder,
                  path):
    f_names = [path.joinpath(f_name).__str__() for f_name in f_names]
    tax = create_tax(m_names, f_names)
    create_database(f_names, manifest_path, db_path)
    manifest = build(
        tax,
        out_folder=model_folder,
        model_db=db_path,
        cutoff=0.0001,
        threads=4,
        # solver='glpk'
    )
    return manifest
