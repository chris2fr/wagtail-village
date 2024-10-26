set -e
IFS=$'\n'
commands=$(cat <<EOF
cd /home/wagtail/wagtail-lesgv/
sudo -u wagtail -g users git pull
# sudo -u wagtail -g users /home/wagtail/venv/bin/pip install -r /home/wagtail/wagtail-lesgv/requirements.txt
sudo -u wagtail -g users /home/wagtail/venv/bin/python  /home/wagtail/wagtail-lesgv/manage.py makemigrations
sudo -u wagtail -g users /home/wagtail/venv/bin/python  /home/wagtail/wagtail-lesgv/manage.py migrate
sudo -u wagtail -g users /home/wagtail/venv/bin/python  /home/wagtail/wagtail-lesgv/manage.py collectstatic --noinput
cd
systemctl restart wagtail
EOF
)
for command in $commands
do
  echo "----------------------------------------------------------------------------------------"
  echo " DO $command"
  echo "-' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' '--' "
  eval $command
  echo "-. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. .--. "
  echo "DONE $command"
  echo "========================================================================================"
done
