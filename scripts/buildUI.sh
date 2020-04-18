while ! [[ -d .git ]]; do
    cd ..
    if [[ "$PWD" == "/" ]]; then
        echo "Can't find the project root";
        exit 127
    fi
done

if ! [[ -d src/ui/ui_compiled ]]; then
    mkdir -p src/ui/ui_compiled/;
fi

rm -rf src/ui/ui_compiled/*

for filename in src/ui/ui_source/*.ui; do
    echo Converting ${filename:3:-3}.py;
    pyuic5 ${filename} >> src/ui/ui_compiled/${filename:17:-3}.py;
done;
