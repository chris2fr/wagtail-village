set -e
source /home/mannchri/wagtail/venv/bin/activate
startdir=`pwd`
workdir=/home/mannchri/wagtail/wagtail-lesgv
scriptdir=/home/mannchri/wagtail/wagtail-lesgv/lesgv/doc
for command in $(seq -f "%03g" 1 8)
do
  echo "----------------------------------------------------------------------------------------"
  echo " DO $command `cat $scriptdir/update-cmlenovodebian/$command.sh`"
  echo "-' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' "
  cd $workdir
  source $scriptdir/update-cmlenovodebian/$command.sh
  echo "-. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. "
  echo "DONE update-cmlenovodebian/$command.sh"
  echo "========================================================================================"
done
cd $startdir


