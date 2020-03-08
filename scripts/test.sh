python manage.py --log db generate --xml ../xml/example.xml --schema er1
python manage.py --log db drop -y
python manage.py --log db create
python manage.py db fake --all --num 50 --fake
python manage.py --log system useradd --login admin --password password --role admin
python manage.py --log hierarchy drop
python manage.py --log hierarchy generate --xml ../xml/example.xml --schema er1 --admin admin --system
