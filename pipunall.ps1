pip freeze > uninstall.txt
pip uninstall -r uninstall.txt
Remove-item "uninstall.txt"
pip install -r requirements.txt
