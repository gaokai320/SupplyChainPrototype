from collections import defaultdict

'''
some packages' import name are the same.
tensorflow:
dxl, tech-pi_dxlearn, Hong-Xiang_dxdata
dxl, Hong-Xiang_dxfunction, Hong-Xiang_dxdata
musket_core, petrochenko-pavel-a_musket_core, musket-ml_musket_core
nlp_datasets, naivenmt_datasets, luozhouyang_nlp-datasets
pythia, glotzerlab_pythia, ChristianSch_PyPythia
coreir, Kuree_pycoreir, leonardt_pycoreir
dragonfly, ladybug-tools_dragonfly-core, dragonfly_dragonfly
dragonfly, mrob95_Breathe, dragonfly_dragonfly
lad, svidovich_lad, mirca_lad
picard, thejohnfreeman_picard, jakebian_picard
delira, justusschock_delira_cycle_gan_pytorch, delira-dev_delira
minos, iqbal-lab-org_minos, guybedo_minos

pytorch:
delira, justusschock_delira_cycle_gan_pytorch, delira-dev_delira
rotest, UnDarkle_pytest-rotest, gregoil_rotest
freesia, AuraiProject_freesia, gitlab.com_lgwilliams_freesia
'''

tensorflow_project_files = ['tensorflow_layer2_project_filtered', 'tensorflow_layer3_project_filtered', 'tensorflow_layer4_project_filtered', 'tensorflow_layer5_project_filtered', 'tensorflow_layer6_project_filtered']
tensorflow_package_files = ['tensorflow_layer1_package_name', 'tensorflow_layer2_package_name', 'tensorflow_layer3_package_name', 'tensorflow_layer4_package_name', 'tensorflow_layer5_package_name']


tensorflow_package_names = {}
for tensorflow_package_file in tensorflow_package_files:
    with open(tensorflow_package_file) as f:
        for line in f:
            import_name, _, repo_name = line.strip('\n').split(';')
            if import_name != '' and import_name not in tensorflow_package_names:
                tensorflow_package_names[import_name] = repo_name
tensorflow_project_upstream = defaultdict(list)
for tensorflow_project_file in tensorflow_project_files:
    with open(tensorflow_project_file) as f:
        for line in f:
            repo, upstream = line.split(';')[:2]
            tensorflow_project_upstream[repo].append(tensorflow_package_names[upstream])

with open('data/tensorflow_new_sc', 'w') as f:
    for k, v in tensorflow_project_upstream.items():
        f.write(k + ';' + ','.join(v) + '\n')

torch_project_files = ['torch_layer2_project_filtered', 'torch_layer3_project_filtered', 'torch_layer4_project_filtered', 'torch_layer5_project_filtered', 'torch_layer6_project_filtered']
torch_package_files = ['torch_layer1_package_name', 'torch_layer2_package_name', 'torch_layer3_package_name', 'torch_layer4_package_name', 'torch_layer5_package_name']
torch_package_names = {}
for torch_package_file in torch_package_files:
    with open(torch_package_file) as f:
        for line in f:
            import_name, _, repo_name = line.strip('\n').split(';')
            if import_name != '' and import_name not in torch_package_names:
                torch_package_names[import_name] = repo_name
            elif import_name != '' and import_name in torch_package_names:
                print(f'{import_name}, {repo_name}, {torch_package_names[import_name]}')
torch_project_upstream = defaultdict(list)
for torch_project_file in torch_project_files:
    with open(torch_project_file) as f:
        for line in f:
            repo, upstream = line.split(';')[:2]
            torch_project_upstream[repo].append(torch_package_names[upstream])

with open('data/torch_new_sc', 'w') as f:
    for k, v in torch_project_upstream.items():
        f.write(k + ';' + ','.join(v) + '\n')