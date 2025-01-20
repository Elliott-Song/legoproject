# Remove all spaces from filenames in a directory

# check if directory is provided
if [ -z "$1" ]; then
    echo "usage: ./remove_spaces.sh <directory>"
    exit 1
fi

# check if directory exists
if [ ! -d "$1" ]; then
    echo "directory does not exist"
    exit 1
fi

# remove spaces from filenames in directory
for file in "$1"/*; do
    newfile=$(echo "$file" | tr -d ' ')
    mv "$file" "$newfile"
done