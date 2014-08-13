set -e
python type.py >type.dict
function run() {
    cd ../shell
    mkdir -p ../$1
    python single.py $1
    #cd ../vw_shell/
    #sh run_model.sh $1 debug
}
run essay
run given
run resource
run project
run user

mkdir -p ../result_data
python multi.py

cd ../vw_shell/
sh run_model.sh result_data train
