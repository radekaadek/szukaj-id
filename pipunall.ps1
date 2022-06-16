$file = '.\requirements.txt'
pip freeze > uninstall.txt
pip uninstall -r uninstall.txt
Remove-item "uninstall.txt"
if ((Test-Path -Path $file -PathType Leaf)) {
    pip install -r $file
}