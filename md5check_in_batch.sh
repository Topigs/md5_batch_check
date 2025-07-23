help_docs=$(cat << EOF
Usage:
    $BASH_SOURCE <DIRECTORY> <FILE EXTENSION> <REFERENCE>
EOF
)

[[ $# -ne 3 || $1 == "-h" || $1 == "--help" ]] && echo "$help_docs" && exit 1

files_dir=$1
file_ext=$2
hash_ref=$3
tmp_file=/tmp/tmp_${RANDOM}.txt
ls ${files_dir}/*${file_ext} | xargs -n1 -P$(nproc) md5sum >| $tmp_file

declare -A md5
declare -A ref
while read hash fp; do md5[$(basename $fp)]=$hash; done < $tmp_file
while read hash fp; do ref[$(basename $fp)]=$hash; done < $hash_ref

dash_line="-----------------------------------------------"
for fn in ${!ref[@]}; do
    if [[ ${md5[$fn]} == ${ref[$fn]} ]]; then stat=OK; else stat=FAIL; fi
    printf "%*s " 40 $fn
    echo $dash_line $stat
done

rm -f $tmp_file
