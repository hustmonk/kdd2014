set -e
echo $#
if [ $# -ne 2 ]; then
    exit
fi

#vw path
vw=~/local/vowpal_wabbit-7.6/vowpalwabbit/vw
workspace="../"$1"/"

function train(){
    train_file=$1
    test_file=$2
    ${vw} ${workspace}${train_file} -c -k --passes 300 -b 24 -f ${workspace}rotten.model.vw
    ${vw} ${workspace}${test_file} -t -i ${workspace}rotten.model.vw -r ${workspace}rotten.rawpreds.txt
}

if [ "$2" == "train" ]; then
    train_file="train.txt"
    test_file="test.txt"
    train ${train_file} ${test_file}
    python out.py ${workspace} >${workspace}sub.csv
elif [ "$2" == "debug" ]; then
    python split.py  ${workspace}
    train_file="train.txt1"
    test_file="train.txt2"
    train ${train_file} ${test_file}
    python auc.py ${workspace} >${workspace}auc.txt
fi
