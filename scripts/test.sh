python -m ermaket.manage --log db drop -y
python -m ermaket.manage --log db clear
python -m ermaket.manage --log db generate --xml ./xml/examples/task_management.xml --schema er1
python -m ermaket.manage --log db drop -y
python -m ermaket.manage --log db create
python -m ermaket.manage db fake --all --num 100 --fake
python -m ermaket.manage --log system roleadd --name admin --reset-pass --sql --link-schema er1 --link-entity User --register-all
python -m ermaket.manage --log system useradd --login admin --password password --role admin
python -m ermaket.manage --log hierarchy drop
python -m ermaket.manage --log hierarchy generate --xml ./xml/examples/task_management.xml --schema er1 --admin admin --system
python -m ermaket.manage --log scripts discover
