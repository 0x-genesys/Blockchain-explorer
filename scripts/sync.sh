#python manage.py runscript -v2 migrate_data --script-args $1 $2
python manage.py runscript -v2 sync_last_mined_blocks --script-args true
