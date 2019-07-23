echo "Start downloading chromedriver..."

currentDir=`pwd`
[[ -f /usr/bin/chromedriver ]] && sudo rm /usr/bin/chromedriver || echo "clean start"

# prepare
mkdir -p tools
cd tools

# download
# wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/75.0.3770.90/chromedriver_linux64.zip
# extract
unzip chromedriver_linux*

# grant permission
chmod +x chromedriver

# ship to path
sudo mv chromedriver /usr/bin

# clean
rm chromedriver_linux*.zip

cd $currentDir

echo "Finished downloading chromedriver"
