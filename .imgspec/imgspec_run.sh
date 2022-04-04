imgspec_dir=$(cd "$(dirname "$0")" ; pwd -P)
pge_dir=$(dirname ${imgspec_dir})

mkdir output
tar_file=$(ls input/*tar.gz)
#echo $tar_file
base=$(basename $tar_file)
#echo $base
output_dir=${base%.tar.gz}
#echo $output_dir
mkdir output/$output_dir

tar -xzvf $tar_file -C input

for a in `python get_paths_from_granules.py`;
   do
       python ${pge_dir}/run_mdn.py $a output/$output_dir;
  done

cd output
tar -czvf $output_dir.tar.gz $output_dir
rm -r $output_dir
