set -e
function run() {
    cd /Users/bubu/mycode/kdd2014/shell
    mkdir -p ../$1
    python single.py $1
    cd ../vw_shell/
    sh debug.sh $1 debug
}
#run essay
#run given
#run resource
#run project
run user
