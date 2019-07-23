echo "Start downloading gecko browser..."

currentDir=`pwd`

# prepare
mkdir -p tools
cd tools

# download
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz

# extract
tar -xvzf geckodriver*

# grant permission
chmod +x geckodriver

# ship to path
sudo mv geckodriver /usr/bin

# clean
rm geckodriver-*.gz

cd $currentDir

echo "Finished downloading gecko browser"
