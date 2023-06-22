def test_growth_se_rt():
    from binary_models.load_se_rt import load_community_model, model_folder
    # first time running, add prep_files=True
    # or if there are any model updates, or if you aren't sure but want to be
    community, manifest = load_community_model(prep_files=False)
    result = community.optimize(fluxes=True)
    assert (result.members.growth_rate.loc['Rhodosporidium'] > 0) & \
           (result.members.growth_rate.loc['Synechococcus'] > 0)
