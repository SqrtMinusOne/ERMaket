# python manage.py --log hierarchy generate --xml ../xml/examples/philosophy.xml --schema phil --admin admin --path ../xml/examples_hierarchy/philosophy.xml
python manage.py --log hierarchy merge --target ../xml/examples_hierarchy/philosophy.xml
python manage.py --log db generate --xml ../xml/examples/philosophy.xml --schema phil --folder models/philosophy --no-system
python manage.py --log db create
