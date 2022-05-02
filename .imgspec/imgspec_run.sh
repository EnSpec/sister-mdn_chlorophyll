imgspec_dir=$(cd "$(dirname "$0")" ; pwd -P)
pge_dir=$(dirname ${imgspec_dir})

source activate sister

mkdir output
tar_file=$(ls input/*tar.gz)
#echo $tar_file
base=$(basename $tar_file)
#echo $base
scene_id=${base%.tar.gz}

if  [[ $scene_id == "ang"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-18)_aqchla
elif [[ $scene_id == "PRS"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-38)_aqchla
elif [[ $scene_id == "f"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-16)_aqchla
elif [[ $scene_id == "DESIS"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-44)_aqchla
fi

mkdir output/$out_dir

tar -xzvf $tar_file -C input

# Resample uncertainty and reflectance
python ${pge_dir}/run_mdn.py input/*/*rfl output/$out_dir

cd output
tar -czvf $out_dir.tar.gz $out_dir
rm -r $out_dir
