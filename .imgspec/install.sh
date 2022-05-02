run_dir=$('pwd')
imgspec_dir=$(cd "$(dirname "$0")" ; pwd -P)
pge_dir=$(dirname ${imgspec_dir})

# Need to do custom install to prevent dependency errors
conda create -y --name sister python=3.8

cd $pge_dir
python setup.py install

rm ${pge_dir}/MDN/Weights/HICO/*
wget -P ${pge_dir}/MDN/Weights/HICO https://github.com/EnSpec/sister-mdn_chlorophyll/raw/master/Weights/HICO/45313342cb628c8cf45b6e2e29f4dc9a780ee1d403bdb98461e28fcb13ad9ce3.zip

