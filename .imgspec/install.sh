run_dir=$('pwd')
imgspec_dir=$(cd "$(dirname "$0")" ; pwd -P)
pge_dir=$(dirname ${imgspec_dir})

conda create -y --name sister python=3.8
source activate sister

cd $pge_dir
python setup.py install

rm ${pge_dir}/MDN/Weights/HICO/*
wget -P ${pge_dir}/MDN/Weights/HICO https://github.com/EnSpec/sister-mdn_chlorophyll/raw/master/MDN/Weights/HICO/45313342cb628c8cf45b6e2e29f4dc9a780ee1d403bdb98461e28fcb13ad9ce3.zip
