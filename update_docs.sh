# remember to call with . ./update_docs so aliases work
make clean
python3 docs/generate_docs.py
make html
/bin/cp -R build/html/* .