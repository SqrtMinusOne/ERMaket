rm ./xml/examples_hierarchy/philosophy.xml
python -m ermaket.manage --log hierarchy generate --xml ./xml/examples/philosophy.xml --schema phil --admin admin --path ./xml/examples_hierarchy/philosophy.xml
python -m ermaket.manage --log hierarchy merge --target ./xml/examples_hierarchy/philosophy.xml
python -m ermaket.manage --log db generate --xml ./xml/examples/philosophy.xml --schema phil --folder ./ermaket/models/philosophy --no-system
python -m ermaket.manage --log db create
python -m ermaket.manage --log db drop --schema phil -y
python -m ermaket.manage --log db create
python -m ermaket.manage --log db load --folder ../ERMaket_Data/Datasets/Philosophy/ --schema phil
