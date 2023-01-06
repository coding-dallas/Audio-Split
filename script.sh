search_dir=$1
echo $search_dir
for entry in "$search_dir"/*
do
	filename=$(basename "$entry")
	echo "$filename" >> ${search_dir}'.txt'
done
