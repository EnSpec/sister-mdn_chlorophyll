imgspec_dir=$(cd "$(dirname "$0")" ; pwd -P)
pge_dir=$(dirname ${imgspec_dir})

rm ${pge_dir}/MDN/Weights/HICO/*
wget -P ${pge_dir}/MDN/Weights/HICO https://github.com/EnSpec/sister-mdn_chlorophyll/raw/master/Weights/HICO/45313342cb628c8cf45b6e2e29f4dc9a780ee1d403bdb98461e28fcb13ad9ce3.zip

mkdir output
tar_file=$(ls input/*tar.gz)
#echo $tar_file
base=$(basename $tar_file)
#echo $base
scene_id=${base%.tar.gz}

if  [[ $scene_id == "ang"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-18)_chla
elif [[ $scene_id == "PRS"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-38)_chla
elif [[ $scene_id == "f"* ]]; then
    out_dir=$(echo $scene_id | cut -c1-16)_chla
fi

#echo $out_dir
mkdir output/$out_dir

tar -xzvf $tar_file -C input

for a in `python ${imgspec_dir}/get_paths_from_granules.py`;
   do
       python ${pge_dir}/run_mdn.py $a output/$out_dir;
  done

cd output
tar -czvf $output_dir.tar.gz $out_dir
rm -r $output_dir
