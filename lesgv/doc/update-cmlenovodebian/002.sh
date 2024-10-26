for i in "lesgv"
do
  echo $i
  rm /home/mannchri/wagtail/wagtail-lesgv/$i/*.py
  cp -a /mnt/d/work/wagtail/wagtail-lesgv/$i/*.py /home/mannchri/wagtail/wagtail-lesgv/$i/
done