for i in "lesgv/doc/" "lesgv/settings/" "lesgv/static/" "lesgv/templates/" "search/"
do
  echo $i
  rsync -a /mnt/d/work/wagtail/wagtail-lesgv/$i /home/mannchri/wagtail/wagtail-lesgv/$i
done