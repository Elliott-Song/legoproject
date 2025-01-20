# convert all .obj files in a directory to .gltf files
# usage: ./objs_to_gltfs.sh <input_dir> <output_dir>

# check if input and output directories are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "usage: ./objs_to_gltfs.sh <input_dir> <output_dir>"
    exit 1
fi

# check if input directory exists
if [ ! -d "$1" ]; then
    echo "input directory does not exist"
    exit 1
fi

# check if output directory exists
if [ ! -d "$2" ]; then
    echo "output directory does not exist"
    exit 1
fi

# convert all .obj files in input directory to .gltf files in output directory using obj2gltf (use quotes in case name has spaces)
for obj in $1/*.obj; do
    gltf=$(basename "$obj" .obj).gltf
    obj2gltf -i "$obj" -o "$2/$gltf"
done

exit 0